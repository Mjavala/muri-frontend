This repository contains four services: 
- The logging service for filtered MQTT data from the IRISS live MQTT broker
- Postgresql12 Database
- The database write service 
- The hasura console  

The Hasura Console is simply an GraphQL wrapper over SQL and a database live console. The custom endpoint makes it easy to make external queries. This readme and other docs in this repo will take you through the entire setup; beyond that there is also a guide on working with hasura and setting up a disaster recovery system with multiple points of failure.   
In order to save time on server configuration and docker containerization, we recommend using the Digital Ocean [one-click-app](https://marketplace.digitalocean.com/apps/hasura-graphql) as a starting point. 

# Hasura Configuration
If you used the one click app to deploy your hasura/postgres instances you should have docker preinstalled with the hasura console, caddy webserver and database running as containers.
The default docker-compose configuration can be changed, the file located at ``/etc/hasura``.  
Example:

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
    ports:
    - "127.0.0.1:5342:5342
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
There are several changes that need to be made to the default configuration.  
- For best security practices, change ``POSTGRES_PASSWORD`` and update ``HASURA_GRAPHQL_DATABASE_URL`` to reflect changes.
- In order to secure this console and your database endpoint, uncomment ``HASURA_GRAPHQL_ADMIN_SECRET`` and set the password.
- by default the docker containers allow no external communication. In order to be able to write data to the postgres instance we will need to open up a port to listen to local calls:
```yaml
...
    ports:
  - "127.0.0.1:5342:5342"
...
```

After going to your domain or IP address in a browser, you should see the password request to get into the console. From inside you can perform CRUD operations on the data and familiarize yourself with GraphQL via the built in playground.
After these changes have been made, you can update the containers with the following command:
```
docker-compose up -d
```

## Hasura Console
As for using the hasura console, you can create tables and databases:

![navigation data panel](db_arch_hasura.png)

Play with the data via GraphQL and SQL:

![navigation data panel](raw_sql.png)
![navigation data panel](graph_hasura.png)

And much [more](https://hasura.io/docs/1.0/graphql/core/index.html).

### Setting up HTTPS/SSL
You may have noticed that the Hasura console only works via http and not HTTPS, lets fix that. Note that this tutorial is via Caddy, however Hasura works with other webservers like Nginx and Apache.  
To add SSL, you'll need to point a [domain](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars) you own to your droplet ip. It can't be done via just an IP address.

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
If you'd like to make any further configurations like using a subdomain, read on [here](https://hasura.io/docs/1.0/graphql/core/deployment/enable-https.html). On reloading the console should now be serving via HTTPS.