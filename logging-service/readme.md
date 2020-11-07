# Logging Service

This service writes incomming MQTT messages into a VPS directory configured in the ``device_logger.py`` file. By default, the path is ``/home/muri-backend/logging-service/logs``, which must be changed to fit your directory structure.  
If you've already set up a configuration file, you can adjust the directory:
```python
# logging_main.py
dotenv_path = join(dirname(__file__), '/root/muri/.env')
load_dotenv(dotenv_path)
```

The logging service is organized by device ID and subdivded into daily and hourly logs. By default the daily logs are backed up for 7 days, and the hourly logs for 24 hours.

## Extension service
Python's logging service doesn't provide a way to add extensions to log files. If you want your logs to be in a specific format, such as json, use the ``extensions.bash`` file. The way this service works is by checking the last 5 characters in a file. If they are not, then they are added. In order to configure for other extensions, the number of characters needs to be changed to fit your extension. After proper configuration, this can then run as a cronjob.