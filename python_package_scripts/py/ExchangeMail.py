
# -*- coding: utf-8 -*-
from exchangelib import *
from exchangelib.folders import *

import AccountConfig

class MailInfo:

    def __init__(self):

        credentials = Credentials(username=AccountConfig.EMAIL_ACCOUNT, password=AccountConfig.EMAIL_PASSWORD)
        self.account = Account(primary_smtp_address=AccountConfig.EMAIL_ADDRESS, credentials=credentials,
                      autodiscover=True, access_type=DELEGATE, locale='da_DK')


    def sendMessage(self, subject, body, recipients):

        m = Message(
            account=self.account,
            subject=subject,
            body=body,
            to_recipients=self.getRecipients(recipients)
        )
        m.send_and_save()


    def getRecipients(self, rec):

        recipients = rec.replace('；', ';').split(';')

        mailboxs = []
        i = 0
        for recipient in recipients:

            recipient = recipient.strip()
            mailboxs.append(Mailbox(email_address=recipient))
            i += 1
        return mailboxs

