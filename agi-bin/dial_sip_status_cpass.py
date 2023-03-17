#!/usr/bin/env python3

import sys
import json
import requests
from asterisk.agi import *
import mysql.connector
import os
import constant as ct
import urllib.parse

#initialising agi
agi = AGI()
agi.verbose("Entering into Python AGI...")
agi.answer()

#receive data from arguments
dial_status = sys.argv[1]
dial_number_action = urllib.parse.unquote(sys.argv[2])
call_id = sys.argv[3]
did_number = sys.argv[4]
caller = sys.argv[5]
account_id = sys.argv[6]
agents = sys.argv[7]

#just verbose received arguments
agi.verbose('DIALSTATUS is %s' % sys.argv[1])

#Post dial status to client
payload={}
#call_data = {"account_id":account_id,"call_id":call_id,"caller":caller,"did_number":did_number,"callee":""}
agent_string = ''
agents=agents.split("&")
for agnt in agents:
    agnt = agnt.split("/")
    agent_string+=agnt[1]+","
agent_string = agent_string.rstrip(',')

dial_status = {"account_id": account_id,"call_id":call_id,"caller":caller,"did_number":did_number,"callee":agent_string,"dial_status":dial_status}
response = requests.request("POST", str(dial_number_action),data=payload,json=dial_status)

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
elif(app=='collect'):
    agi.verbose('App is %s' % app)
    agi.set_variable('app',response['response']['app'])
    agi.set_variable('text',response['response']['text'])
    agi.set_variable('action',response['response']['action'])
    agi.set_variable('timeout',response['response']['timeout'])
    agi.set_variable('attempts',response['response']['attempts'])
    agi.set_variable('numdigits',response['response']['numdigits'])
elif(app=='dial_number'):
    agi.verbose('App is %s' % app)
    agi.set_variable('app',response['response']['app'])
    numbers = response['response']['numbers']
    numbers=numbers.split(",")
    dial_string=''
    trunk_name='kamtrunk'
    for num in numbers:
        dial_string+="PJSIP/"+num+"@"+trunk_name+"&"
    dial_string = dial_string.rstrip('&')
    agi.set_variable('numbers',dial_string)
    agi.set_variable('action',response['response']['action'])
    agi.set_variable('timeout',response['response']['timeout'])
elif(app=='dial_sip'):
    agi.verbose('App is %s' % app)
    agi.set_variable('app',response['response']['app'])
    agents = response['response']['agents']
    agents = agents.split(",")
    dial_string=''
    for agnt in agents:
        dial_string+="PJSIP/"+agnt+"&"
    dial_string = dial_string.rstrip('&')
    agi.set_variable('agents',dial_string)
    agi.set_variable('action',response['response']['action'])
    agi.set_variable('timeout',response['response']['timeout'])
elif(app=='voicemail'):
    agi.verbose('App is %s' % app)
    agi.set_variable('app',response['response']['app'])
    agi.set_variable('text',response['response']['text'])
    agi.set_variable('maxduration',response['response']['maxduration'])
    agi.set_variable('action',response['response']['action'])
    agi.set_variable('errortext',response['response']['errortext'])
    agi.set_variable('successtext',response['response']['successtext'])
