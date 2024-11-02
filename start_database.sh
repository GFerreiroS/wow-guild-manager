docker run -d \
  --name wow-guild-manager \
  -e POSTGRES_USER="postgres" \
  -e POSTGRES_PASSWORD="password" \
  -e POSTGRES_DB=wow-guild-manager \
  -p 5432:5432 \
  docker.io/postgres && echo "Database container was successfully created"