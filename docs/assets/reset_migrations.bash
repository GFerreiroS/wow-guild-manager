rm -R -f ./migrations &&
pipenv run init &&
dropdb -h localhost -U postgres wow-guild-manager || true &&
createdb -h localhost -U postgres wow-guild-manager || true &&
psql -h localhost wow-guild-manager -U postgres -c 'CREATE EXTENSION unaccent;' || true &&
pipenv run migrate &&
pipenv run upgrade
