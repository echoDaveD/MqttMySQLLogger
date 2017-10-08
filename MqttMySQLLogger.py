#!/usr/bin/env python
import time

import paho.mqtt.client as mqtt
import pymysql
import ConfigParser, os.path, sys

config_file = os.getcwd() + "/config/config.ini"

# function to save log messages to specified log file
def log(msg):
    # open the specified log file
    file = open(config.get('config', 'logfile_path'),"a")
    # write log message with timestamp to log file
    file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))
    print(msg)
    # close log file
    file.close

# MQQT connection
def on_connect(client, userdata, flags, rc):
    log("[INFO] Connected with rc: " + str(rc))

    if rc>0:
       log("[ERROR] MQTT Connection Error: " + str(rc)) 
       sys.exit()
    else: 
       client.subscribe(config.get('mqtt', 'mqtt_topic'))

# on new MQTT Message
def on_message(client, userdata, msg):
    #log("[INFO] " + msg.topic + ": " + str(msg.payload))
# connect to MySQL DB
    mySQLCon = pymysql.connect( host=config.get('mysql', 'mysql_host'), user=config.get('mysql', 'mysql_user'), passwd=config.get('mysql', 'mysql_psswd'))
    mySQLCursor = mySQLCon.cursor()

# check if databse knows the topic
    mySQLCursor.execute("select topicid from MqttMySQLLogger.Topic where topicname = trim('" + str(msg.topic) + "');")
    result = mySQLCursor.fetchone()
    topicid = 0
    if result == None:
        # insert topic
        mySQLCursor.execute("insert into MqttMySQLLogger.Topic (topicname, topicts) values (Trim('" + str(msg.topic) + "'), current_timestamp)")
        topicid = mySQLCursor.lastrowid
        #log("lastrowid: " + str(topicid) + "     result. " + str(result))
    else:
        topicid = result[0]

# insert the message
    sql = "insert into MqttMySQLLogger.Message (msgtopicid, msgtopic, msgvalue, msgts) values (" + str(topicid) + " , Trim('" + str(msg.topic) + "'), Trim('" + str(msg.payload) + "'),  current_timestamp);"
    #log(sql)
    mySQLCursor.execute(sql)
    mySQLCon.commit()
    mySQLCon.close()

# check if Configfile exists
if not os.path.exists(config_file):
   log("[ERROR] No Configfile found. Please create one!")
   sys.exit()

config = ConfigParser.ConfigParser()
config.read(config_file)


log("[INFO] Configuration File: "+config_file)


# check if Configfile is configured
if not config.getboolean('config', 'configured'):
   log("[ERROR] Setup not complete! Update /config/config.ini then set 'configured' to True to disable this message.")
   sys.exist()

# connect to MySQL DB
mySQLCon = pymysql.connect( host=config.get('mysql', 'mysql_host'), user=config.get('mysql', 'mysql_user'), passwd=config.get('mysql', 'mysql_psswd'))
mySQLCursor = mySQLCon.cursor()

# try to create the Database
try:
    mySQLCursor.execute("CREATE DATABASE MqttMySQLLogger;")
    log("[INFO] Database MqttMySQLLogger created.")
except (pymysql.ProgrammingError, pymysql.DataError, pymysql.IntegrityError, pymysql.NotSupportedError, pymysql.OperationalError, pymysql.InternalError) as error:
    code, message = error.args
# 1007 = Database exists
    if code != 1007:
        log("[MySQL ERROR - CREATE DATABASE]" + str(code) + str(message))
        sys.exit()

# try to create the tables
try:
    mySQLCursor.execute("CREATE TABLE MqttMySQLLogger.Topic (topicid int primary key not null auto_increment, "+ 
                                                            "topicname varchar(255) not null, "+ 
                                                            "topicts timestamp not null default current_timestamp "+ 
                                                            ");")
    log("[INFO] Table Topic created.")
except (pymysql.ProgrammingError, pymysql.DataError, pymysql.IntegrityError, pymysql.NotSupportedError, pymysql.OperationalError, pymysql.InternalError) as error:
    code, message = error.args
# 1050 = Table already exists
    if code != 1050:
        log("[MySQL ERROR - CREATE Topic]" + str(code) + str(message))
        sys.exit()

try:
    mySQLCursor.execute("CREATE TABLE MqttMySQLLogger.Message (msgtopicid int not null, "+ 
                                                              "msgid int primary key not null auto_increment, "+
                                                              "msgtopic varchar(255) not null, "+
                                                              "msgvalue varchar(255) not null, "+ 
                                                              "msgts timestamp not null default current_timestamp, "+
                                                              "foreign key (msgtopicid) REFERENCES Topic(topicid) "+ 
                                                              ");")
    log("[INFO] Table Message created.")
except (pymysql.ProgrammingError, pymysql.DataError, pymysql.IntegrityError, pymysql.NotSupportedError, pymysql.OperationalError, pymysql.InternalError) as error:
    code, message = error.args
# 1050 = Table already exists
    if code != 1050:
        log("[MySQL ERROR - CREATE Message]" + str(code) + str(message))
        sys.exit()

mySQLCon.commit()
mySQLCon.close()

# connect to the MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(config.get('mqtt', 'mqtt_host'), config.get('mqtt', 'mqtt_port'), 60)
client.loop_forever()

