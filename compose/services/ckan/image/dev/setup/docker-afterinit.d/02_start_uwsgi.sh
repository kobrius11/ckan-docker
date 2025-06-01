#!/bin/sh

# Check if we are in maintenance mode and if yes serve the maintenance pages
if [ "$MAINTENANCE_MODE" = true ]; then PYTHONUNBUFFERED=1 python maintenance/serve.py; fi

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