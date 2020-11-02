# MQTT and postgres config

# Hasura & Postgres setup
Recommended setup is via the Digital Ocean [one-click-app](https://marketplace.digitalocean.com/apps/hasura-graphql).
This will spin up a a docker environment containing all components necessary to work with hasura.  
The first thing to do would be to test that the hasura console has been set up well.  
You can do this by navigating to:

```
http://<your_droplet_ip>/console
```

From here, your postgres instance is ready to import an existing configuration. If you are creating your own custom tables, follow this [tutorial](https://hasura.io/docs/1.0/graphql/core/deployment/deployment-guides/digital-ocean-one-click.html). 

## Security config
This section sets up postgres username password as well as a password for the hasura console.  
This is done via the ``docker-compose.yaml`` file located at:

```
/etc/hasura
```
The file should look like this:
```yaml
version: '3.6'
services:
  postgres:
    image: postgres:12
    restart: always
    volumes:
    - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: {YOUR PASSWORD HERE}   # <------->
  graphql-engine:
    image: hasura/graphql-engine:v1.3.2
    depends_on:
    - "postgres"
    restart: always
    environment:
      # database url to connect
      HASURA_GRAPHQL_DATABASE_URL: postgres://postgres:postgrespassword@postgres:5432/postgres  # STICK TO THE DEFAULT DB
      ## enable the console served by server
      HASURA_GRAPHQL_ENABLE_CONSOLE: "true" # set "false" to disable console
      ## enable debugging mode. It is recommended to disable this in production
      HASURA_GRAPHQL_DEV_MODE: "true"
      ## uncomment next line to set an admin secret
      # HASURA_GRAPHQL_ADMIN_SECRET: myadminsecretkey   # <------->
    command:
    - graphql-engine
    - serve
  caddy:
    image: caddy/caddy
    depends_on:
    - "graphql-engine"
    restart: always
    ports:
    - "80:80"
    - "443:443"
    volumes:
    - ./Caddyfile:/etc/caddy/Caddyfile
    - caddy_certs:/root/.caddy
volumes:
  db_data:
  caddy_certs:
```

Change the ``POSTGRES_PASSWORD``, uncommenting ``HASURA_GRAPHQL_ADMIN_SECRET`` and set a password for the console.

## Setting up SSL
Out of the box, the hasura console serves only via HTTP. To add SSL, you'll need to [point](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars) your domain to your droplet ip.  

From there, go to ``/etc/hasura`` and edit the Caddyfile to reflect the following:

```
{YOUR_DOMAIN_HERE} {
  reverse_proxy graphql-engine:8080
}
```

Then, restart the Caddy docker container:

```
docker-compose restart caddy
```

## Importing an existing database

### Useful Docker commands
-  docker exec -it [img] psql -U postgres (connect to postgres)
-  docker-compose start/stop
-  docker inspect [img]
-  docker logs [img]