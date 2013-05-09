import os
import unittest
import qbo
import qboconst
import csvprovider
from datetime import date

class csvtoqboTest(unittest.TestCase):

	def testInit(self):
		myQbo = qbo.qbo()
		self.assertEquals(myQbo.getHEADER(), qboconst.HEADER)
		self.assertEquals(myQbo.getFOOTER(), qboconst.FOOTER)
		self.assertEquals(myQbo.getDATE_START(), qboconst.DATE_START)
		self.assertEquals(myQbo.getDATE_END(), qboconst.DATE_END)
		self.assertEquals(myQbo.getBANKTRANLIST_START(), qboconst.BANKTRANLIST_START)
		self.assertEquals(myQbo.getBANKTRANLIST_END(), qboconst.BANKTRANLIST_END)
		self.assertEquals(myQbo.getTRANSACTION_START(), qboconst.TRANSACTION_START)
		self.assertEquals(myQbo.getTRANSACTION_END(), qboconst.TRANSACTION_END)


	def testAddTransaction(self):
		myQbo = None
		myQbo = qbo.qbo()

		status = 'Completed'
		date_posted = str(date.today().strftime('%b %d, %Y'))
		memo = 'AddTransactionTest'
		txn_type = 'Payment'
		to_from_flag = 'From'
		txn_amount = '1.00'
		name = 'TestBuy'

		self.assertEquals(myQbo.addTransaction(status, date_posted, txn_type, to_from_flag, txn_amount, name), True)
		self.assertEquals(myQbo.getCount(), 1)

	def testBuild(self):
		myQbo = None
		myQbo = qbo.qbo()

		status = 'Completed'
		date_posted = str(date.today().strftime('%b %d, %Y'))
		memo = 'AddTransactionTest'
		txn_type = 'Payment'
		to_from_flag = 'From'
		txn_amount = '1.00'
		name = 'TestBuy'

		self.assertEquals(myQbo.addTransaction(status, date_posted, txn_type, to_from_flag, txn_amount, name), True)
		self.assertEquals(len(myQbo.getDocument()), 1136)

	def testWrite(self):
		myQbo = None
		myQbo = qbo.qbo()
	
		status = 'Completed'
		date_posted = str(date.today().strftime('%b %d, %Y'))
		memo = 'AddTransactionTest'
		txn_type = 'Payment'
		to_from_flag = 'From'
		txn_amount = '1.00'
		name = 'TestBuy'

		self.assertEquals(myQbo.addTransaction(status, date_posted, txn_type, to_from_flag, txn_amount, name), True)
		self.assertEquals(myQbo.Write('./csvtoqbo-test.qbo'), True)
		statinfo = os.stat('./csvtoqbo-test.qbo')
		self.assertEquals(statinfo.st_size, 1280)

	def testUnknownProvider(self):
		try:		
			self.assertRaises(Exception, provider.provider('not-amazon'))
		except:
			pass

	def testProviderName(self):
		myProvider = csvprovider.csvprovider('amazon')
		self.assertEquals(myProvider.getID(), 'amazon')
		
	def testProviderGetters(self):
		myProvider = csvprovider.csvprovider('amazon')
		myDict = {'Status' : 'Completed',
						'Date' : 'May 8, 2013',
						'Type' : 'Payment',
						'To/From' : 'From',
						'Amount' : '1.00',
						'Name' : 'TestBuy'}
		self.assertEquals(myProvider.getStatus(myProvider,myDict), 'Completed')
		self.assertEquals(myProvider.getDatePosted(myProvider,myDict), 'May 8, 2013')
		self.assertEquals(myProvider.getTxnType(myProvider, myDict), 'Payment')
		self.assertEquals(myProvider.getToFrom(myProvider, myDict), 'From')
		self.assertEquals(myProvider.getTxnAmount(myProvider, myDict), '1.00')
		self.assertEquals(myProvider.getTxnName(myProvider, myDict), 'TestBuy')

if __name__ == '__main__':
    unittest.main()
