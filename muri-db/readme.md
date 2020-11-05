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