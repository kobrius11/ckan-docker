#!/bin/sh

set -ex

# Run any startup scripts provided by images extending this one
if [[ -d "/docker-entrypoint.d" ]]
then
    for f in /docker-entrypoint.d/*; do
        case "$f" in
            *.sh)     echo "$0: Running init file $f"; . "$f" ;;
            *.py)     echo "$0: Running init file $f"; python3 "$f"; echo ;;
            *)        echo "$0: Ignoring $f (not an sh or py file)" ;;
        esac
        echo
    done
fi

# Generate Beaker and JWT secrets from environment variables, if not present let CKAN auto generate them
if [[ -z $BEAKER_SESSION_SECRET || -v $BEAKER_SESSION_SECRET || -z $JWT_ENCODE_SECRET || -v $JWT_ENCODE_SECRET || -z $JWT_DECODE_SECRET || -v $JWT_DECODE_SECRET ]]; then
	echo "Missing BEAKER and JWT environment variables. Autogenerating secrets..."
else
	echo "Setting session secrets from environment variables"
	ckan config-tool $CKAN_INI "beaker.session.secret=$BEAKER_SESSION_SECRET"
	ckan config-tool $CKAN_INI "api_token.jwt.encode.secret=$JWT_ENCODE_SECRET"
	ckan config-tool $CKAN_INI "api_token.jwt.decode.secret=$JWT_DECODE_SECRET"
fi

# Autogenerating Beaker and JWT secrets
if grep -E "beaker.session.secret ?= ?$" $CKAN_INI; then
	echo "Setting secrets in ini file"
	ckan config-tool $CKAN_INI "beaker.session.secret=$(python -c 'import secrets; print(secrets.token_urlsafe())')"
	ckan config-tool $CKAN_INI "WTF_CSRF_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe())')"
	JWT_SECRET=$(python -c 'import secrets; print("string:" + secrets.token_urlsafe())')
	ckan config-tool $CKAN_INI "api_token.jwt.encode.secret=$JWT_SECRET"
	ckan config-tool $CKAN_INI "api_token.jwt.decode.secret=$JWT_SECRET"
fi

# Run the prerun script to init CKAN and create the default admin user
echo "Starting prerun.py to configure CKAN backends..."
python3 prerun.py || {
	echo '[CKAN prerun] FAILED. Exiting...'
	exit 1
}

# Update config for xloader API, use sysadmin API key
# Check if xloader api token is set
if ! grep -q ckanext.xloader.api_token $CKAN_INI; then
	# Generate API key for sysadmin user
	echo "Generating an API key for sysadmin user to use for xloader..."
	SYSADMIN_XLOADER_API_TOKEN=$(ckan -c $CKAN_INI user token add sysadmin xloader -q)
	ckan config-tool $CKAN_INI "ckanext.xloader.api_token=$SYSADMIN_XLOADER_API_TOKEN"
fi

# Check if we are in maintenance mode and if yes serve the maintenance pages
if [ "$MAINTENANCE_MODE" = true ]; then PYTHONUNBUFFERED=1 python maintenance/serve.py; fi

# Run any after prerun/init scripts provided by images extending this one
if [[ -d "${APP_DIR}/docker-afterinit.d" ]]; then
	echo "Found afterinit scripts, initializing:"
	for f in ${APP_DIR}/docker-afterinit.d/*; do
		case "$f" in
		*.sh)
			echo "$0: Running after prerun init file $f"
			. "$f"
			;;
		*.py)
			echo "$0: Running after prerun init file $f"
			python "$f"
			echo
			;;
		*) echo "$0: Ignoring $f (not an sh or py file)" ;;
		esac
		echo
	done
fi

# Check whether http basic auth password protection is enabled and enable basicauth routing on uwsgi respecfully
if [ $? -eq 0 ]; then
	if [ "$PASSWORD_PROTECT" = true ]; then
		if [ "$HTPASSWD_USER" ] || [ "$HTPASSWD_PASSWORD" ]; then
			# Generate htpasswd file for basicauth
			htpasswd -d -b -c $APP_DIR/.htpasswd $HTPASSWD_USER $HTPASSWD_PASSWORD
			# Start uwsgi with basicauth
			uwsgi --ini $APP_DIR/uwsgi.conf --pcre-jit $UWSGI_OPTS
		else
			echo "Missing HTPASSWD_USER or HTPASSWD_PASSWORD environment variables. Exiting..."
			exit 1
		fi
	else
		# Start uwsgi
		echo "Starting UWSGI with '${UWSGI_PROC_NO:-2}' workers"
		uwsgi $UWSGI_OPTS
	fi
else
	echo "Failed...not starting CKAN."
fi