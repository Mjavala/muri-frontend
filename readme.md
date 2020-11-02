# Python services setup
On a fresh install of the hasura [one-click-app](https://marketplace.digitalocean.com/apps/hasura-graphql) from Digital Ocean,  
you'll need to install pip:
```
sudo  apt install python3-pip
```

and then, the following modules are needed:
```
pip3 install paho-mqtt
pip3 install python-dotenv
pip3 install pytz
pip3 install asyncpg

# Config

For the logging and historical flights services, MQTT and Postgres passwords should be stored in dedicated config files.
In order to read these files in python:

```python
from os.path import join, dirname
from dotenv import load_dotenv
import os
dotenv_path = join(dirname(__file__), "{YOUR_DIR/.env")
load_dotenv(dotenv_path)

...

USER = os.getenv("DB_USER")
PW = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_NAME")
HOST = os.getenv("DB_HOST")

...

sample environment file:
DB_USER = 'postgres'
DB_PASSWORD = ***
DB_NAME = 'postgres'
DB_HOST = '0.0.0.0'

MQTT_USER = '***'
MQTT_PASS = '********'
MQTT_HOST = '****'
MQTT_PORT = ********

```

The ``dotenv_path`` will have to be edited manually once this script is pulled from gitlab. It defaults to ``/root/muri/.env``.

## Docker-compose config
In order to connect to from the python script to the postgres instance in the container, the ``docker-compose.yaml`` file needs to be modified.
Below is a sample docker-compose file set up to accept local connections. It also shows optional security config. 

```
/etc/hasura
```


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

Change the ``POSTGRES_PASSWORD``, uncommenting ``HASURA_GRAPHQL_ADMIN_SECRET`` and set a password for the console.  
Add the ``ports`` section in the postgres service.

# Hasura & Postgres config
Recommended setup is via the Digital Ocean [one-click-app](https://marketplace.digitalocean.com/apps/hasura-graphql).
This will spin up a a docker environment containing all components necessary to work with hasura.  
The first thing to do would be to test that the hasura console has been set up well.  
You can do this by navigating to:

```
http://<your_droplet_ip>/console
```


From here, your postgres instance is ready to import an existing configuration. If you are creating your own custom tables, follow this [tutorial](https://hasura.io/docs/1.0/graphql/core/deployment/deployment-guides/digital-ocean-one-click.html). 

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
If you are doing a VPS to VPS transfer, this guide will show you how to do it via scp/ssh. You'll need to set up a target server.  
Both a custom or one click app VPS will work here.

### SSH config
SSH communication will need to be set up in order to transfer the data dump.  
From the server with the data, generate a new ssh key pair via this command:

``
ssh-keygen
``
Set up a password and a custom name for your key if desired. From here, you'll want to copy the public key to the ``authorized_keys`` file in the target server. To do so, you can run the following commands:

``
cat {key.pub}
``
Copy the output to your clipboard, either manually or with software like [xclip](https://stackoverflow.com/questions/5130968/how-can-i-copy-the-output-of-a-command-directly-into-my-clipboard)

On the target server, the authorized keys folder should be located at ``/root/.ssh``. Once in the directory, copy the contents into the file.  

Finally restart the ssh service with this command:
```
sudo service ssh restart
```

You can then test that the ssh setup works by ssh'ing into the target server:

```
ssh -i ~/.ssh/{YOUR_KEY} {YOUR_USER}@{YOUR_SERVER_IP_OR_DOMAIN}
```

### Scp data transfer

If the source of the data is inside an existing VPS droplet within a docker container, start by dumping the data with the following command:
```
docker exec -t {YOUR_IMAGE_ID} pg_dumpall -c -U postgres | gzip > {YOUR_DIR}/dump_$(date +"%Y-%m-%d_%H_%M_%S").gz
```
Note that this also zips the dump file.

With the ssh configured correctly run the following command:

```
scp -i ~/.ssh/{KEY} {DIR}/dump_{DATE}.gz {USER}@{SERVER_IP}:~{/DESTINATION}
```
The zipped dump file should now be at ``SERVER_IP`` at whatever ``DESTINATION`` was selected (default root).

Now the file should be unzipped:
```
gzip -d {FILE}
```

The dump file can now be uploaded to the postgres instance. To do so, you'll need the postgres container id. It can found and copied using:
```
docker ps
```
The following command then copies the data:
```
cat {DUMP_FILE} | docker exec -i {CONTAINER_ID} psql -U postgres
```
Note that using a different database/user combo than the default results in errors not covered here.  

### Hasura console setup
Once you've copied the data to the empty postgres instance on the target server, hasura must be configured to track the new tables.
Go to the console at your domain or target server ip address and click on the data panel.

![navigation data panel](hasura_data_panel.png)

From there, you should see a section labeled *Untracked tables or views*.

![Untracked views](hasura_track_panel.png)

Click Track all and your hasura/postgres service is ready for data ingestion.

### Useful Docker commands
-  docker exec -it [img] psql -U postgres (connect to postgres)
-  docker-compose start/stop
-  docker inspect [img]
-  docker logs [img]