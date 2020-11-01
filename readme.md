# Hasura & Postgres setup
Recommended setup is via the Digital Ocean [one-click-app](https://marketplace.digitalocean.com/apps/hasura-graphql).
This will spin up a a docker environment containing all components necessary to work with hasura.

## Docker compose file

## Setting up SSL

## Importing an existing database

### Useful Docker commands
-  docker exec -it [img] psql -U postgres (connect to postgres)
-  docker-compose start/stop
-  docker inspect [img]
-  docker logs [img]