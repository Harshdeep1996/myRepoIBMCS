import requests
import json
from json import dumps
from random import choice
from string import ascii_uppercase, ascii_lowercase

#Printing all the databases and logging in through - Could have done through sessions as well!
auth = ('harshcs1996','Harsh1996')
response = requests.get('https://harshcs1996.cloudant.com/_all_dbs',auth=auth)

#Printing the result as json 
print(response.text)

#Creating a database - Can we checked through response code and for loop
print "Enter the database name : "
database_name = raw_input()

response = requests.put('https://harshcs1996.cloudant.com/%s'%database_name,auth=auth)
if response.status_code == requests.codes.ok:
	print "Database has been made in Cloudant user account!"
response.raise_for_status() #Raising an error if response code is wrong and hence database won't be created!

#Uploading 1 document to the new database\
my_header = {'Content-Type': 'application/json'}
data = '{"key1":"value1"}'
#Need to always put header when sending data, as it might not match the server
response = requests.post('https://harshcs1996.cloudant.com/%s'%database_name,headers=my_header,auth=auth,data=data)
print response.status_code

#Putting multiple document in a single request 
# 1. VIA CURL - url -u harshcs1996 https://harshcs1996.cloudant.com/harshdeep5/_bulk_docs -X POST -H "Content-Type: application/json" -d '{"docs":[{"key1":"value1"},{"key2":"value2"}]}'
#docs is the parameter for the use of multiple documents

#Random key value generator
listName = []
for x in xrange(500):
	#dict = {os.urandom(15):'harsh'}
	dict = {(''.join(choice(ascii_uppercase + ascii_lowercase) for i in range(12))):'1'} #import
	listName.append(dict)

#print listName

#Putting through 500 documents in the database
dataNew = {'docs':listName}
responseNew = requests.post('https://harshcs1996.cloudant.com/%s/_bulk_docs'%database_name,headers=my_header,auth=auth,data=dumps(dataNew))
print responseNew.status_code

#Counting the total number of documents in a database
response = requests.get('https://harshcs1996.cloudant.com/%s'%database_name,auth=auth)
print "Total number of documents : %s" %response.json()['doc_count'] #Variable


