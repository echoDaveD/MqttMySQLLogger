# MqttMySQLLogger
MqttMySQLLogger is an Pythen Script which listen to an Mqtt Topic and write any new message to an MySQL Database.

On the initial run, MqttMySQLLogger will creating following MySQL objects.

The database where the tables will be stored.
```sql
CREATE DATABASE MqttMySQLLogger
```

The table where any topic will be stored once.
```sql
CREATE TABLE CREATE TABLE MqttMySQLLogger.Topic
```

The table where any message to an Topic will be stored with the current timestamp.
```sql
CREATE TABLE CREATE TABLE MqttMySQLLogger.Message
```

## System Requirements

You need MySQL-Server, Python and pip on your computer.
```command
apt-get install mysql-server mysql-client
apt-get install -y python-pip python-dev build-essential libffi-dev libssl-dev
```

After that we still need some pip libraries:

Python MQTT lib
```python
pip install paho-mqtt
```

Python MySQL libs
```python
pip install MySQL-python
pip install PyMySQL
```

## Configuration

This Python script can only run if an valid cofig.ini file exists.
Here is the explanation of the config/config.ini entries:

If your configuration is done set `configured` to True.
Set an Path for the `logfile_path`. !Important! User which starts the script must have the permission to write in that file.
This script only logs Errors and messages like "Database is created". The messages from Mqtt are not logged.
```python
[config]
configured=False
logfile_path=/path/to/your/logfile/MqttMySQLLogger.log
```

Put here your Mqtt-Server details like host and port.
Set also the topic you wont to be logged. You can use comman mqtt wildcards, "#" means every message will be logged.
```python
[mqtt]
mqtt_host: localhost
mqtt_port: 1883
mqtt_topic: #
```

And the last point is our MySQL-Server. Set here the required informations.
```python
[mysql]
mysql_host: localhost
mysql_user: YourUser
mysql_psswd: YourPassword
```


## Common MySQL Queries

Drop Database
```sql
drop database MqttMySQLLogger;
```

Select all topics
```sql
select * from MqttMySQLLogger.Topic;
```

Select all messages to one Topic
```sql
select * from MqttMySQLLogger.Message where msgtopicid = 1 order by msgts asc;
select * from MqttMySQLLogger.Message where msgtopic = "YOUR/TOPIC" order by msgts asc;
```


## Autostart on Ubuntu 

To start this script on login with your User just do the following steps

* Open Dash (The First Icon In Sidebar).
* Then type Startup Applications and open that app.
* Here Click the Add Button on the right.
* There fill in the details and in the command area browse for your Python File and click Ok.

you can also start it with an cron or run it es a service.

