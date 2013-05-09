# qbofile.py
# Python file containing variables for formatted sections of a QBO file.

import sys, traceback
import os
from datetime import datetime
import logging
import qboconst

class qbo:

	__transactions = list()
	__document = None
	__isValid = None

	def __init__(self):
		self.__HEADER = qboconst.HEADER
		self.__FOOTER = qboconst.FOOTER
		self.__DATE_START = qboconst.DATE_START
		self.__DATE_END = qboconst.DATE_END
		self.__BANKTRANLIST_START = qboconst.BANKTRANLIST_START
		self.__BANKTRANLIST_END = qboconst.BANKTRANLIST_END
		self.__TRANSACTION_START = qboconst.TRANSACTION_START
		self.__TRANSACTION_END = qboconst.TRANSACTION_END
		self.__isValid = True
	
	def getHEADER(self):
		return self.__HEADER

	def getFOOTER(self):
		return self.__FOOTER

	def getDATE_START(self):
		return self.__DATE_START

	def getDATE_END(self):
		return self.__DATE_END
	
	def getBANKTRANLIST_START(self):
		return self.__BANKTRANLIST_START

	def getBANKTRANLIST_END(self):
		return self.__BANKTRANLIST_END

	def getTRANSACTION_START(self):
		return self.__TRANSACTION_START

	def getTRANSACTION_END(self):
		return self.__TRANSACTION_END
	
	def validateTransaction(self, status, date_posted, txn_type, to_from_flag, txn_amount, name):

		if status != 'Completed':
			#log status failure
			raise Exception("Transaction status [" + status + "] invalid.")

		if type(datetime.strptime(str(date_posted), '%b %d, %Y')) is not datetime:
			#log date type not valid
			raise Exception("Transaction posted date [" + date_posted + "] invalid.")

		if str(txn_type) not in ('Payment','Refund','Withdrawal'):
			#log invalid txn_type
			raise Exception("Transaction type [" + str(txn_type) + "] not 'Payment', 'Refund', or 'Withdrawal'.")

		if to_from_flag not in ('To', 'From'):
			#log invalid to_from_flag
			raise Exception("Transaction 'To/From' field [" + to_from_flag + "] invalid.")

		#logical test of txn_type and to_from_flag
		if ((txn_type == 'Refund' and to_from_flag != 'To') or (txn_type == 'Payment' and to_from_flag != 'From')):
			#log logic failure
			raise Exception("Transaction type inconsistent with 'To/From' field.")

		if len(name) == 0 or not name:
			#log empty name paramter
			raise Exception("Transaction name empty or null.")

		return True

	def addTransaction(self, status, date_posted, txn_type, to_from_flag, txn_amount, name):
		
		try:
			self.validateTransaction(status, date_posted, txn_type, to_from_flag, txn_amount, name)
		except:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
			print ''.join('!! ' + line for line in lines)
			logging.info(''.join('!! ' + line for line in lines))
			raise Exception

		transaction = ""

		rec_date = datetime.strptime(str(date_posted), '%b %d, %Y')
		rec_date = rec_date.strftime('%Y%m%d%H%M%S') + '.000[-5]'

		__DATE_POSTED = '<DTPOSTED>' + rec_date
		__MEMO = '<MEMO>' + str(txn_type)

		if str(txn_type) == 'Payment':
			__TRANSACTION_TYPE = '<TRNTYPE>CREDIT'
		elif (str(txn_type) == 'Refund' and str(to_from_flag) == 'To') or (str(txn_type) == 'Withdrawal'):
			__TRANSACTION_TYPE = '<TRNTYPE>DEBIT'

		__TRANSACTION_AMOUNT = '<TRNAMT>' + str(txn_amount).replace('$','')
		__TRANSACTION_NAME = '<NAME>' + str(name)
		__FITID = '<FITID>' + rec_date + str(1000+len(self.__transactions))[1:]

		transaction = ("" + self.__TRANSACTION_START + "\n"
						"" + __TRANSACTION_TYPE + "\n"
						"" + __DATE_POSTED + "\n"
						"" + __TRANSACTION_AMOUNT + "\n"
					   "" + __FITID + "\n"
					   "" + __TRANSACTION_NAME + "\n"
					   "" + __MEMO + "\n"
					   "" + self.__TRANSACTION_END + "\n")

		self.__transactions.append(transaction)
		logging.info("Transaction [" + str(self.getCount())  + "] Accepted.")
		return True

	def getCount(self):
		return len(self.__transactions)

	def isValid(self):
		if self.getCount() == 0:
			self.__isValid = False
		return self.__isValid

	def getDocument(self):
		self.Build()
		return self.__document

	def Build(self):
		if not self.isValid():
			logging.info("Error: QBO document is not valid.")
			raise Exception("Error: QBO document is not valid.")

		self.__document = ("" + self.__HEADER + "\n"
					"" + self.__BANKTRANLIST_START + "\n"
					"" + self.__DATE_START + "\n"
					"" + self.__DATE_END + "\n")

		for txn in self.__transactions:
			self.__document = self.__document + str(txn)
		
		self.__document = self.__document + ("" + self.__BANKTRANLIST_END + "\n"
							   "" + self.__FOOTER + "")
			
	def Write(self, filename):

		try:

			with open(filename, 'w') as f:
				f.write(self.getDocument())

			return True

		except:
			#log io error
			exc_type, exc_value, exc_traceback = sys.exc_info()
			lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
			print ''.join('!! ' + line for line in lines)
			logging.info('qbo.Write() method: '.join('!! ' + line for line in lines))
			return False
