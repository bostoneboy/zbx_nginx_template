#!/usr/bin/python

import urllib2, base64, re, struct, time, datetime, sys, os.path

try:
    import json
except:
    import simplejson as json

# URL to nginx stat (http_stub_status_module)
stat_url = 'http://127.0.0.1/nginx_status'

# Optional Basic Auth
username = ''
password = ''

def get(url, login, passwd):
	req = urllib2.Request(url)
	if login and passwd:
		base64string = base64.encodestring('%s:%s' % (login, passwd)).replace('\n', '')
		req.add_header("Authorization", "Basic %s" % base64string)   
	q = urllib2.urlopen(req)
	res = q.read()
	q.close()
	return res

def parse_nginx_stat(data,x_item):
  # Active connections
  if x_item == 'active_connections':
    value = re.match(r'(.*):\s(\d*)', data[0], re.M | re.I).group(2)
  # Accepts
  elif x_item == 'accepted_connections':
    value = re.match(r'\s(\d*)\s(\d*)\s(\d*)', data[2], re.M | re.I).group(1)
  # Handled
  elif x_item == 'handled_connections':
    value = re.match(r'\s(\d*)\s(\d*)\s(\d*)', data[2], re.M | re.I).group(2)
  # Requests
  elif x_item == 'handled_requests':
    value = re.match(r'\s(\d*)\s(\d*)\s(\d*)', data[2], re.M | re.I).group(3)
  # Reading
  elif x_item == 'header_reading':
    value = re.match(r'(.*):\s(\d*)(.*):\s(\d*)(.*):\s(\d*)', data[3], re.M | re.I).group(2)
  # Writing
  elif x_item == 'body_reading':
    value = re.match(r'(.*):\s(\d*)(.*):\s(\d*)(.*):\s(\d*)', data[3], re.M | re.I).group(4)
  # Waiting
  elif x_item == 'keepalive_connections':
    value = re.match(r'(.*):\s(\d*)(.*):\s(\d*)(.*):\s(\d*)', data[3], re.M | re.I).group(6)
  else:
    value = 'Error'
  print value

data = get(stat_url, username, password).split('\n')
x_item = sys.argv[1]
parse_nginx_stat(data,x_item)

