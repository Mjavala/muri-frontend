# Db Write Service

This is a sub-guide on installing and using the database write service. If the DO one click app was used, then the first thing after cloning the repo would be to install pip:

```
# Ubuntu 18.04
sudo  apt install python3-pip
...
The following packages then need to be installed:

pip3 install paho-mqtt
pip3 install python-dotenv
pip3 install pytz
pip3 install asyncpg
```


For the logging and historical flights services, MQTT and Postgres passwords should be stored in dedicated config files. It is recommended to store these outside of your repo and point to the directory using ``dotenv_path`` as shown below:

```python
from os.path import join, dirname
from dotenv import load_dotenv
import os
dotenv_path = join(dirname(__file__), "{YOUR_DIR/.env")
load_dotenv(dotenv_path)
```
Now, the configuration file must be created, here is a sample in which the keys work directly with the repo setup.
```

sample environment file:
...

DB_USER = 'postgres'
DB_PASSWORD = ***
DB_NAME = 'postgres'
DB_HOST = '0.0.0.0'

MQTT_USER = '***'
MQTT_PASS = '********'
MQTT_HOST = '****'
MQTT_PORT = ********
```

The ``dotenv_path`` will have to be edited manually unless the config file is created with the default directry ``/root/muri/.env``.

## Service config
The database write module is set up as a microservice, this section shows how to set it up via systemctl.  
For each service there is a folder called ``service-script`` with a ``.service`` fil insidee. Out of the box, these files are configured to set up the service. However your paths may be different, so be sure to check that the service file points to the right directory.  
For each file, create a symlink to the ``/etc/systemd/system/`` folder, like so:

``ln -s target_path link_path``

The service then needs to be started:
```
systemctl start {SERVICE}
```

To check whether the service is working succesfully you can run this command:
```
systemctl status {SERVICE}
``` 
