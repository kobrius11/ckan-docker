# Run any startup scripts provided by images extending this one
if [[ -d "/docker-entrypoint-initdb.d" ]]
then
    for f in /docker-entrypoint-initdb.d/*; do
        case "$f" in
            *.sh)     echo "$0: Running init file $f"; . "$f" ;;
            *.py)     echo "$0: Running init file $f"; python3 "$f"; echo ;;
            *)        echo "$0: Ignoring $f (not an sh or py file)" ;;
        esac
        echo
    done
fi
