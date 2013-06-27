#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

from httplib2 import Http
from urllib.parse import urlencode
import json
import argparse

ap = argparse.ArgumentParser(description='Prints the status of a t411.me user.')
ap.add_argument('-u', '--user', required=True, help='Your t411 username')
ap.add_argument('-p', '--pass', required=True, help='Your t411 password')

args = vars(ap.parse_args())

user = args['user']
password = args['pass']

url_base = 'http://api.t411.me'
url_auth = url_base + '/auth'
url_profile = url_base + '/users/profile/'

HTTP_OK = '200'

credentials = { 'username': user, 'password': password }
headers = { 'Content-type': 'application/x-www-form-urlencoded' } 

h = Http()
ans, rawdata = h.request( url_auth, 'POST', urlencode(credentials), headers ) 

if ans['status'] == HTTP_OK:
	data = json.loads(rawdata.decode('utf-8'))
	try:
		token = data['token']
		#print(token)
		headers['Authorization'] = token
		
		#print(headers)
		ans, rawdata = h.request( url_profile + data['uid'], headers=headers)
		
		if ans['status'] == HTTP_OK:
			data = json.loads(rawdata.decode('utf-8'))
		
			name = data['username']
			dl = int(data['downloaded']) / pow(1024, 3)
			ul = int(data['uploaded']) / pow(1024, 3)
			r = ul/dl
		
			print('User       : %s' % name)
			print('Downloaded : %.1f GiB' % dl)
			print('Uploaded   : %.1f GiB' % ul)
			print('Ratio      : %.2f' % r)
			
		else:
			print(ans)
			
	except:
		print(data['error'])

else:
	print(ans)