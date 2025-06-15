#!/bin/sh

supervisorctl reread
supervisorctl add ckan_gather_consumer
supervisorctl add ckan_fetch_consumer
supervisorctl start ckan_gather_consumer
supervisorctl start ckan_fetch_consumer

service supervisor start

echo "*/15 * * * * ckan -c ${CKAN_INI} harvester run" >> /etc/crontab
echo "0 5 * * * ckan -c ${CKAN_INI} harvester clean-harvest-log" >> /etc/crontab