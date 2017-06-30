import base64
import html
import os
import re
import urllib.parse
import urllib.request

from oauth2client import tools

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2017, Stek.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = "Azure Manager"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


class HackpadMailProcessor():
    """
    Process Hackpad Migration emails
    """

    def __init__(self, config, logger):
        """
        Constructor
        :param config: Configuration dict
        :param logger: Python logger
        """

        self._config = config
        self._logger = logger

    def process_emails(self, emails):
        """
        Process Hackpad Mails
        """

        # For each mail, extract sender email, date and download URL
        for email in emails:

            # Initialize data
            url = None
            attachment_path = None
            sender = email['from']
            sender_email_address = self.extract_sender_email(sender=sender)

            # Find url and attachment
            for mail_body in self.extract_email_bodies(email=email):
                url = self.extract_url(text=str(mail_body, encoding='utf-8'))
                if url:
                    # Download Archive
                    attachment_path = self.download_archive(url=url)
                    continue

            job = {
                "from": sender,
                "email_address": sender_email_address,
                "sent_date": "",
                "url": url,
                "attachment": attachment_path
            }

            self._logger.info("Queueing job: %s" % job)

    def extract_sender_email(self, sender):
        """
        Extract the email address from a From email header

        :param sender: The value inside the "From" email header
        :return: The email address
        """
        email_address = None

        match = re.search(r'[\w\.-]+@[\w\.-]+', sender)
        if match:
            email_address = match.group(0)

        return email_address

    def download_archive(self, url):
        """
        Download Archive to a given destination
        :param url: URL of the archive
        """

        # Extract filename
        file_name = urllib.parse.urlsplit(url)[2].replace('/', '_')

        self._logger.info("Downloading file from URL %s" % url)

        # Extract filename
        download_path = "%s/%s" % (self._config['download_directory'], file_name)

        # Ensure the directory exists
        if not os.path.exists(self._config['download_directory']):
            os.makedirs(self._config['download_directory'])

        urllib.request.urlretrieve(url, download_path)

        return download_path

    def extract_email_bodies(self, email):
        """

        :param email:
        :return:
        """
        # Make a list of mail bodies
        mail_bodies = []

        # See if there is a body
        if email['body'] and 'data' in email['body']:
            mail_bodies.append(base64.urlsafe_b64decode(email['body']['data']))

        # See if there are parts
        if email['parts']:
            for part in email['parts']:
                mail_bodies.append(base64.urlsafe_b64decode(part['body']['data']))

        return mail_bodies

    def extract_url(self, text):
        """
        Extract Hackpad Archive URL from a text

        :param text:
        :return: the located URL as a string
        """
        archive_url = None
        r = re.compile('(?<=href=").*hackpad-export.*?(?=")')
        matches = r.findall(text)

        if matches:
            archive_url = html.unescape(matches[0])
            self._logger.info("Located download URL: %s" % archive_url)

        return archive_url