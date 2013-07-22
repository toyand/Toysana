#!/usr/bin/env python

import sys
import parsedatetime.parsedatetime as pdt
import datetime
import os

from asana import asana
from dateutil.relativedelta import *

def extract_due_date(task_string):
	reverse_list = task_string[:]
	reverse_list.reverse()
	
	main_list = task_string[:]
	
	word = ""
	date_string = ""
	
	# We iterate over the reversed list looking for the word 'by'. When we find it
	# we will have assembled the correct date string and we will also have popped
	# those words off the actual master string so we'll be left with a clean task
	# string to parse
	for word in reverse_list:
		main_list.pop()
		if word == "by":
			break
		
		date_string = word+" "+date_string
		
	# Check if we actually found the word by at all	and if not we just
	# return the original parameters
	if word!="by":
		return None, task_string
		
	try:
		the_date = datetimeFromString(date_string)
		
		return the_date, main_list
	except:
		# If we can't pull a real date, let's just stick it all in Asana
		return None, task_string
		

def make_task(task_string):
	due_date, remainder_string = extract_due_date(task_string)
	
	if due_date==None:
		due_date=datetimeFromString("today")
		
	task_name = " ".join(remainder_string)
	task_name = task_name.capitalize()
	
	try:
		asana_api.create_task(task_name, 
			asana_spaces[0]['id'], 
			assignee=asana_user['id'],
			due_on=due_date.strftime("%Y-%m-%d"))
		print "ADDED task: '%s'" % task_name
	except:
		print "FAILED task add: '%s'" % task_name

def main():	
	make_task(sys.argv[1:])
	
def datetimeFromString(s):
	c = pdt.Calendar()
	result, what = c.parse( s )
	
	dt = None

	# what was returned (see http://code-bear.com/code/parsedatetime/docs/)
	# 0 = failed to parse
	# 1 = date (with current time, as a struct_time)
	# 2 = time (with current date, as a struct_time)
	# 3 = datetime

	if what in (1,2):
		# result is struct_time
		dt = datetime.datetime( *result[:6] )
	elif what == 3:
		# result is a datetime
		dt = result

	if dt is None:
		# Failed to parse
		raise ValueError, ("Don't understand date '"+s+"'")

	return dt	

######## START ##########
if len(sys.argv)==1:
	print "Usage: toysana {task_description} [by {task_date}]"
	sys.exit(1)
try:
	ASANA_KEY = os.environ['ASANA_API_KEY']
	asana_api = asana.AsanaAPI(ASANA_KEY, debug=False)
	asana_spaces = asana_api.list_workspaces()
	asana_user = asana_api.user_info()
except:
	print "FAILED to add task: Could not connect to Asana"
	print "Make sure you have defined the ASANA_API_KEY environment variable"
	sys.exit(-1)
	
main()