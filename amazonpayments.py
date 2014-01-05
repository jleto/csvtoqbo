#concrete provider class for handling amazon payments csv

from abstractprovider import AbstractProvider

class amazonpayments(AbstractProvider):

	__providerID = ''
	__providerName = ''

	def __init__(self):
			self.__providerID = 'amazon'
			self.__providerName = 'Amazon Payments'

	def getID(self):
		return self.__providerID

	def getName(self):		
		return self.__providerName

	@staticmethod
	def getStatus(self,row):
		return row.get('Status')

	@staticmethod
	def getDatePosted(self, row):
		return row.get('Date')

	@staticmethod
	def getTxnType(self,row):
		return row.get('Type')

	@staticmethod
	def getToFrom(self,row):
		return row.get('To/From')

	@staticmethod
	def getTxnAmount(self,row):
		return row.get('Amount')

	@staticmethod
	def getTxnName(self,row):
		return row.get('Name')

