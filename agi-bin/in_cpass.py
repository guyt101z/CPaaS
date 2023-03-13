#!/usr/bin/env python3

import sys
import json
import requests
from asterisk.agi import *
import mysql.connector
import os
import constant as ct

#mysql connection
mydb = mysql.connector.connect(
  host=ct.HOST,
  user=ct.DBUSER,
  password=ct.DBPASSWORD,
  database=ct.DATABASE
)

#initialising agi
agi = AGI()
agi.verbose("Entering into Python AGI...")
agi.answer()

#receive data from arguments
did_number = sys.argv[1]

#just verbose received arguments
agi.verbose('DID is %s' % sys.argv[1])

#get interface_id from the did_number
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM did_number WHERE did_number="+str(did_number))
myresult = mycursor.fetchall()
incoming_url_voice = myresult[0][2]

agi.verbose('URL is %s' % str(incoming_url_voice))

#Here call API to get recording type setting
payload={}
response = requests.request("POST", str(incoming_url_voice),data=payload)

response = json.loads(response.text)
app = response['response']['app']

if(app=='play'):
    agi.verbose('App is %s' % app)
    agi.set_variable('app',response['response']['app'])
    agi.set_variable('url',response['response']['url'])
elif(app=='say'):
    agi.verbose('App is %s' % app)
    agi.set_variable('app',response['response']['app'])
    agi.set_variable('text',response['response']['text'])


