# csvtoqbo.py
# Python script to convert CSV files of transactions exported from
# various platforms to QBO for import into Quickbooks Online.
#

import sys, traceback
import os
import logging
import csv
import qbo
import csvprovider

if len(sys.argv) <= 1:
	sys.exit("Usage: python %s <options> <csvfiles>\n"
		     "Where possible options include:\n"
			 "   -amazon            Specify csv output is from Amazon Payments.\n"
		     "   --help             Help for using this tool." % sys.argv[0]
			)
elif (sys.argv[1] == '--help'):
	sys.exit("Help for %s not yet implemented." % sys.argv[0])

if sys.argv[1] == '-amazon':
	myProvider = None
	myProvider = csvprovider.csvprovider('amazon')

for arg in sys.argv:
	if sys.argv.index(arg) >  1:
		
		os.remove(arg[:len(arg)-3] + 'log')
		logging.basicConfig(filename=arg[:len(arg)-3] + 'log', level=logging.INFO)
		logging.info("Opening '%s' CSV File" % myProvider.getName())

		try:

			with open(arg, 'r') as csvfile:

				reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
				
				#instantiate the qbo object
				myQbo = None
				myQbo = qbo.qbo()
				txnCount = 0
				for row in reader:
					txnCount = txnCount+1
					sdata = str(row)
					#read in values from row of csv file
					status = myProvider.getStatus(myProvider,row)
					date_posted = myProvider.getDatePosted(myProvider,row)
					txn_type = myProvider.getTxnType(myProvider,row)
					to_from_flag = myProvider.getToFrom(myProvider,row)
					txn_amount = myProvider.getTxnAmount(myProvider,row)
					name = myProvider.getTxnName(myProvider,row)

					#Add transaction to the qbo document
					if myQbo.addTransaction(status, date_posted, txn_type, to_from_flag, txn_amount, name):
						print('Transaction [' + str(txnCount) + '] added successfully!')
						logging.info('Transaction [' + str(txnCount) + '] added successfully!')				

		except:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
			print ''.join('!! ' + line for line in lines)
			logging.info("Transaction [" + str(txnCount) + "] excluded!")

			logging.info('>> Data: ' + str(sdata))

		try:
			filename = arg[:len(arg)-3] + 'qbo'
			if myQbo.Write('./'+ filename):
				print("QBO file written successfully!")
				#log successful write
				logging.info("QBO file %s written successfully!" % filename)
		except:
			#log error			
			exc_type, exc_value, exc_traceback = sys.exc_info()
			lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
			print ''.join('!! ' + line for line in lines)
			logging.info(''.join('!! ' + line for line in lines))
