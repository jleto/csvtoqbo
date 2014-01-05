#####################################################################
#																	#
#	File: qboconst.py												#
#	Developer: Justin Leto											#
#																	#
#	qboconst.py holds const values for QBO file format				#
#																	#
#	Usage: Called from qbo.py										#
#																	#
#####################################################################

from datetime import date, time

DATE_TODAY = "" + date.today().strftime('%Y%m%d%H%M%S') + ".000[-5]"

HEADER = ("OFXHEADER:100\n"
		"DATA:OFXSGML\n"
		"VERSION:102\n"
		"SECURITY:NONE\n"
		"ENCODING:USASCII\n"
		"CHARSET:1252\n"
		"COMPRESSION:NONE\n"
		"OLDFILEUID:NONE\n"
		"NEWFILEUID:NONE\n\n"		  
		"<OFX>\n"
		"<SIGNONMSGSRSV1>\n"
		"<SONRS>\n"
		"<STATUS>\n"
		"<CODE>0\n"
		"<SEVERITY>INFO\n"
		"<MESSAGE>OK\n"
		"</STATUS>\n"
		"<DTSERVER>" + DATE_TODAY + "\n"
		"<LANGUAGE>ENG\n"
		"<INTU.BID>3000\n"
		"</SONRS>\n"
		"</SIGNONMSGSRSV1>\n"
		"<BANKMSGSRSV1>\n"
		"<STMTTRNRS>\n"
		"<TRNUID>" + DATE_TODAY + "\n"
		"<STATUS>\n"
		"<CODE>0\n"
		"<SEVERITY>INFO\n"
		"<MESSAGE>OK\n"
		"</STATUS>\n"
		"<STMTRS>\n"
		"<CURDEF>USD\n"
		"<BANKACCTFROM>\n"
		"<BANKID>999999999\n"
		"<ACCTID>999999999999\n"
		"<ACCTTYPE>CHECKING\n"
		"</BANKACCTFROM>\n")

FOOTER = ("<LEDGERBAL>\n"
		"<BALAMT>0.00\n"
		"<DTASOF>" + DATE_TODAY + "\n"
		"</LEDGERBAL>\n"
		"<AVAILBAL>\n"
		"<BALAMT>0.00\n"
		"<DTASOF>" +  DATE_TODAY + "\n"
		"</AVAILBAL>\n"
		"</STMTRS>\n"
		"</STMTTRNRS>\n"
		"</BANKMSGSRSV1>\n"
		"</OFX>\n")

DATE_START = "<DTSTART>" +  DATE_TODAY + "\n"

DATE_END = "<DTEND>" +  DATE_TODAY + "\n"

BANKTRANLIST_START = "<BANKTRANLIST>\n"

BANKTRANLIST_END = "</BANKTRANLIST>\n"

TRANSACTION_START = "<STMTTRN>"
TRANSACTION_END = "</STMTTRN>"
