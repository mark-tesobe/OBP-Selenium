# Script for picking up OBP challenge OTP from imap account
# ©2021 TESOBE GmbH

import imaplib
import email


def get_otp(host, username=None, password=None):
	if host == 'DUMMY':
		return "123"

	imap = imaplib.IMAP4(host)
	imap.starttls()

	imap.login(username, password)

	imap.select('Inbox')

	tmp, data = imap.sort('REVERSE DATE', 'UTF-8', 'ALL')
	for num in data[0].split():
		tmp, data = imap.fetch(num, '(RFC822)')
		msg = email.message_from_bytes(data[0][1]).get_payload()
		# OTP has to be the first integer in the mail body for this to work
		otp = [int(s) for s in msg.split() if s.isdigit()][0]
		break
	imap.close()
	return otp
