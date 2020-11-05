# Repo Setup
This repository contains three services: The logging service for filtered MQTT data from the IRISS live MQTT broker, the database write service, and the hasura console.
Beyond that, there is also a guide on working with hasura and setting up a disaster recovery system with multiple points of failure.  
In order to save time on server configuration and docker containerization, we recommend using the Digital Ocean [one-click-app](https://marketplace.digitalocean.com/apps/hasura-graphql) as a starting point.  
The app comes preconfigured with a working Hasura / Postgres instance spun up via a docker-compose file located here:
```
/etc/hasura
```
The File should look similar to this:

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
There are several things to configure here. For best security practices, change ``POSTGRES_PASSWORD`` and update ``HASURA_GRAPHQL_DATABASE_URL`` to reflect changes. Also, since the one click app comes with hasura working out of the gate, it should be available live via your ip address or preconfigured domain. Note that subdomain support is not covered in this guide, and all following steps assume that postgres password and user are default.
After looking up your IP address or domain, you should get to the console where you can perform CRUD operations on the data and familiarize yourself with GraphQL via the built in playground. In order to secure this console and your database endpoint, uncomment ``HASURA_GRAPHQL_ADMIN_SECRET`` and set the password. Now the hasura console should be password protected.  
Finally, by default the docker containers allow no external communication. In order to be able to write data to the postgres instance we will need to open up a port to listen to local calls:
```yaml
...
    ports:
  - "127.0.0.1:5342:5342"
...
```

After these changes have been made, you can update the containers with the following command:
```
docker-compose up -d
```

## Hasura Console
You should now be password protected via hasura, as well as a safe environment for your database instance. As for using the hasura console, you can create tables and databases:

![navigation data panel](db_arch_hasura.png)

Play with the data via GraphQL and SQL:

![navigation data panel](raw_sql.png)
![navigation data panel](graph_hasura.png)

And much [more](https://hasura.io/docs/1.0/graphql/core/index.html).

From here the tutorial goes into optional configuration for the Hasura console, as well as a tutorial on importing data and schemas to our postgres instance and how hasura plays into that. First, you may have noticed that the Hasura console only works via http and not HTTPS, lets fix that. Note that this tutorial is via Caddy, however Hasura works with other webservers like Nginx and Apache.

### Setting up HTTPS/SSL
To add SSL, you'll need to point a domain you own [domain](https://www.digitalocean.com/community/tutorials/how-to-point-to-digitalocean-nameservers-from-common-domain-registrars) to your droplet ip. It can't be done via just an IP address.

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
If you'd like to make any further configurations like using a subdomain, read on [here](https://hasura.io/docs/1.0/graphql/core/deployment/enable-https.html). On reloading the console you should now be serving via HTTPS.

## Importing Data

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





















# Db Write Service

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


Change the ``POSTGRES_PASSWORD``, uncommenting ``HASURA_GRAPHQL_ADMIN_SECRET`` and set a password for the console.  
Add the ``ports`` section in the postgres service.

## Service config
The python package is set up as a microservice, this section shows how to set it up via systemctl.  
For each service there is a folder with a ``.service`` file. Out of the box, these files are configured to set up the service.  
For each file, create a symlink to the ``/etc/systemd/systemctl/`` folder, like so:

``ln -s target_path link_path``

The service then needs to be started:
```
systemctl start {SERVICE}
```

To check whether the service is working succesfully you can run this command:
```
systemctl status {SERVICE}
``` 

# Disaster Recovery / Data Backups
In order to persist data, this section will show you how to backup zipped data dumps into another Digital Ocean droplet as well as to an AWS S3 bucket.  
Multiple services (DO/AWS) are used to introduce another point of failure.  
## Droplet to Droplet backups
Data backups can happen via scp in the same way as described for importing an existing database.  
To automate this process you can set up a cron job with the following file bash file:

```bash
#!/usr/bin/bash

rm -rf /home/data_dump/*

docker exec -t {IMG_ID} pg_dumpall -c -U postgres | gzip > {DUMP_OUTPUT_DIR}/dump_$(date +"%Y-%m-%d_%H_%M_%S").gz

scp -i ~/.ssh/{PRIV_KEY} /{DUMP_OUTPUT_DIR}/* root@{BACKUP_SERVER_IP}:~/{OUTPUT_DIR}
```

Once configured, this can then be setup to happen at a desired intervial via a cronjob:


```
crontab -e
...
0 0 * * 5 /home/backup-script.sh  # Scheduled every Friday & 12AM UTC
```

## Droplet to AWS backups
In order to connect to AWS from your VPS, we will need to use the aws CLI. On most linux systems, this command will work:

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```
More information on this can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)

After installation, run this command to configure AWS. In order to configure the CLI, you'll have to generate a public and secret key tied to your AWS account.  
```
aws configure
```

You should now be able to see if you have any S3 buckets available with:
```
aws s3api list-buckets --query "Buckets[].Name"
```
After Selecting a bucket, you can then copy a folder on your VPS into it:
```
aws s3 cp {path_to_folder} s3://{bucket_name}/ --recursive
```

And that should be it!

### Useful Docker commands
-  docker exec -it [img] psql -U postgres (connect to postgres)
-  docker-compose start/stop
-  docker inspect [img]
-  docker logs [img]