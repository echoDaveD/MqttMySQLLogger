# MqttMySQLLogger
MqttMySQLLogger is an Pytchen Script which listen to one/many Mqtt Topics and write any new message to an MySQL Database.

On the initial run, MqttMySQLLogger will creating following MySQL objects.

`CREATE DATABASE MqttMySQLLogger`
It's the database where the tables will be stored.

`CREATE TABLE CREATE TABLE MqttMySQLLogger.Topic`
It's the table where any topic will be stored once.

`CREATE TABLE CREATE TABLE MqttMySQLLogger.Message`
It's the table where any message to an Topic will be stored with the current timestamp.

