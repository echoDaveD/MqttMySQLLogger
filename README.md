# MqttMySQLLogger
MqttMySQLLogger is an Pythen Script which listen to an Mqtt Topic and write any new message to an MySQL Database.

On the initial run, MqttMySQLLogger will creating following MySQL objects.

`CREATE DATABASE MqttMySQLLogger`
It's the database where the tables will be stored.

`CREATE TABLE CREATE TABLE MqttMySQLLogger.Topic`
It's the table where any topic will be stored once.

`CREATE TABLE CREATE TABLE MqttMySQLLogger.Message`
It's the table where any message to an Topic will be stored with the current timestamp.

## System Requirements

You need Python and pip on your computer.
`apt-get install -y python-pip python-dev build-essential libffi-dev libssl-dev`

After that we still need some pip libraries:

Python MQTT lib
`pip install paho-mqtt`

Python MySQL libs
`pip install MySQL-python`
`pip install PyMySQL`

## Configuration

This Python script can only run if an valid cofig.ini file exists.
Here is the explanation of the config.ini entries:

`
[config]
configured=False
logfile_path=/path/to/your/logfile/MqttMySQLLogger.log
`
If your configuration is done set `configured` to True.

Set an Path for the `logfile_path`. !Important! Usre which starts the script must have the permission to write in that File.

This script only logs Errors an messages like "Database is created". The Messages from Mqtt will be not logged.

`
[mqtt]
mqtt_host: localhost
mqtt_port: 1883
mqtt_topic: #
`

Put here your Mqtt connection deteils like host and port.
Set also the topic you wont to be logged. You can use the comman mqtt Wildcards, "#" means every message will be logged.

`
[mysql]
mysql_host: localhost
mysql_user: YourUser
mysql_psswd: YourPassword
`

And the last point is our MySQL Server. Set here the required informations.


## Common MySQL Queries

Drop Database
`drop database MqttMySQLLogger;`

Select all topics
`select * from MqttMySQLLogger.Topic;`

Select all messages to one Topic
`select * from MqttMySQLLogger.Message where msgtopicid = 1 order by msgts asc;`
`select * from MqttMySQLLogger.Message where msgtopic = "YOUR/TOPIC" order by msgts asc;`


## Autostart on Ubuntu 16.04 LTS

