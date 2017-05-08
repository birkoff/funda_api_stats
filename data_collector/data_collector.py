import requests
import time
import pymysql.cursors
import os
import boto3

#####################################
#      API Data Collector 			#
# 	(Read below at End of Document)	#
#####################################

## Repository for Funda Data (Mysql)
class DbRepository:
	def __init__(self, db_config):
		self.db = pymysql.connect(host=db_config['DB_HOSTNAME'],
								  port=3306,
								  user=db_config['DB_USERNAME'],
								  password=db_config['DB_PASSWORD'],
								  db=db_config['DB_NAME'],
								  cursorclass=pymysql.cursors.DictCursor)

		self.table = db_config['DB_TABLE']

	def remove_old_items(self, search):
		with self.db.cursor() as cursor:
			cursor.execute("DELETE FROM {0} WHERE search = '{1}'".format(self.table, search))

	def save(self, items):
		for item in items:
			statement = "INSERT INTO {0} (FundaId,MakelaarId,MakelaarNaam,Postcode,Koopprijs,search) VALUES ('{1}', '{2}','{3}','{4}','{5}','{6}');".format(
			self.table, item['id'], item['makelaarId'], item['makelaarNaam'], item['postcode'], item['koopprijs'], item['search'])

			with self.db.cursor() as cursor:
				cursor.execute(statement)
		self.db.commit()

	def __del__(self):
		self.db.close()


## Repository for Funda Data (DynamoDB)
class DynamoDbRepository:
	def __init__(self):
		session = boto3.Session(region_name='eu-west-1')
		self.client = session.client('dynamodb')

	def remove_old_items(self, search):
		pass

	def save(self, items):
		for item in items:
			recordItem = {
				'Id': {"S": item['id']},
				'MakelaarId': {"S": item['makelaarId']},
				'MakelaarNaam': {"S": item['makelaarNaam']},
				'Postcode': {"S": item['postcode']},
				'Koopprijs': {"S": item['koopprijs']},
				'search': {"S": item['search']}
			}

			response = self.client.put_item(
				TableName='listed_objects2',
				Item=recordItem
			)


## Multi Repository MySQL and DynamoDB
class MultiRepository:
	def __init__(self, db_config):
		self.db = DbRepository(db_config)
		self.dynamodb = DynamoDbRepository()

	def remove_old_items(self, search):
		self.db.remove_old_items(search)

	def save(self, items):
		self.db.save(items)
		self.dynamodb.save(items)


## API Handler
class FundaApiHandler:
	PAGESIZE = 25

	def __init__(self, api_key):
		self.api_key = api_key

	def get_request_url(self, search, page):
		return "http://partnerapi.funda.nl/feeds/Aanbod.svc/json/{0}/?type=koop&zo=/{1}/&page={2}&pagesize={3}".format(
			self.api_key, search, page, self.PAGESIZE)

	def is_valid_response(self, response):
		if 'Objects' in response:
			return 1
		return 0

	def get_total_pages_from_response(self, response):
		return response['Paging']['AantalPaginas']

	def get_data_from_response(self, response, search):
		items = []
		for item in response['Objects']:
			data = {}
			data['id'] = item['Id']
			data['makelaarId'] = "{0}".format(item['MakelaarId'])
			data['makelaarNaam'] = item['MakelaarNaam'].encode('utf-8')
			data['postcode'] = "{0}".format(item['Postcode'])
			data['koopprijs'] = "{0}".format(item['Koopprijs'])
			data['search'] = search
			items.append(data)
		return items


class DataCollector:
	MAX_PAGES = 120

	def __init__(self, api, repository):
		self.repository = repository
		self.api = api
		self.total_pages = 1 # init total_pages with 1, later will get the real value

	def search_and_collect(self, search):
		self.remove_old_items(search)
		page = 1

		while page <= self.total_pages:
			if page > self.MAX_PAGES:
				break

			api_items = self.get_items_from_api(search, page)
			self.save_api_items(api_items)

			page += 1
			sleepInSeconds = 1
			print "Sleeping for {0} seconds...".format(sleepInSeconds)
			time.sleep(sleepInSeconds)

		print "Finished"

	def remove_old_items(self, search):
		print "=> Removing Old Items for query: {0}]".format(search)
		self.repository.remove_old_items(search)

	def get_items_from_api(self, search, page):
		requestUrl = self.get_request_url(search, page)
		print "=> Request Page {0}, Total Pages: {1}, URL: {2}".format(page, self.total_pages, requestUrl)

		req = requests.request('GET', requestUrl)
		response = req.json()

		if not self.api.is_valid_response(response):
			return

		self.total_pages = self.get_total_pages_from_response(response)
		items = self.api.get_data_from_response(response, search)
		return items

	def get_request_url(self, search, page):
		return self.api.get_request_url(search, page)

	def get_total_pages_from_response(self, response):
		return self.api.get_total_pages_from_response(response)

	def save_api_items(self, items):
		print items
		try :
			self.repository.save(items)
		except Exception as e:
			print "DB Error: {0}".format(e)

db_config = {}
db_config['DB_HOSTNAME'] = os.environ.get('DB_HOSTNAME')
db_config['DB_USERNAME'] = os.environ.get('DB_USERNAME')
db_config['DB_PASSWORD'] = os.environ.get('DB_PASSWORD')
db_config['DB_NAME'] = os.environ.get('DB_NAME')
db_config['DB_TABLE'] = os.environ.get('DB_TABLE')

api_key = os.environ.get('API_KEY')

dataCollector = DataCollector(FundaApiHandler(api_key), DbRepository(db_config))
dataCollector.search_and_collect('amsterdam')
dataCollector.search_and_collect('amsterdam/tuin')

## NOTE: Below are examples of how can we use different repositories to store the collected data
## We can add another type of API as well

# dataCollector = DataCollector(FundaApi(), DynamoDbRepository())
# dataCollector.search_and_collect('amsterdam')
# dataCollector.search_and_collect('amsterdam/tuin')

# dataCollector = DataCollector(FundaApi(api_key), MultiRepository(db_config))
# dataCollector.search_and_collect('amsterdam')
# dataCollector.search_and_collect('amsterdam/tuin')