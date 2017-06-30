#!/usr/bin/env python3

import click
import common
import os
from gmail_reader import GmailReader
from hackpad_mail_processor import HackpadMailProcessor

__author__ = "Dimi Balaouras"
__copyright__ = "Copyright 2017, Stek.io"
__version__ = "0.0.1"
__status__ = "Prototype"
__description__ = "Azure File Storage Backups"
__abs_dirpath__ = os.path.dirname(os.path.abspath(__file__))
__default_config_file__ = "%s/../config/config.yml" % __abs_dirpath__

# If modifying these scopes, delete your previously saved credentials
APPLICATION_NAME = 'Hackpad Gmail Reader'
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CREDENTIALS_DIR = os.path.join(__abs_dirpath__, '.credentials')
CLIENT_SECRET_FILE = os.path.join(CREDENTIALS_DIR, 'client_secret.json')
CREDENTIALS_FILE = os.path.join(CREDENTIALS_DIR, 'hackpad-gmail-reader.json')


@click.command()
@click.option('--config-file', required=False, default=__default_config_file__,
              help='Path to config file')
def start(config_file):
    """
    Start Backup Service
    """
    # Load config
    config = common.load_config_file(config_file)

    # Load logging config
    common.setup_logging_config("%s/../config/" % __abs_dirpath__)

    # Get logger
    logger = common.get_logger("app")

    logger.info("Starting mail parsing...")
    credentials_dir = os.path.join(__abs_dirpath__, '../.credentials')

    # Enhance configuration
    config['credentials_dir'] = os.path.join(credentials_dir, config['client_secret_file'])
    config['client_secret_file'] = os.path.join(credentials_dir, config['client_secret_file'])
    config['credentials_file'] = os.path.join(credentials_dir, config['credentials_file'])

    reader = GmailReader(config=config, logger=logger)
    new_mails = reader.fetch_mails(q=config['gmail_query_string'])

    hackpad_processor = HackpadMailProcessor(config=config, logger=logger)
    hackpad_processor.process_emails(emails=new_mails)


if __name__ == '__main__':
    app = start(obj={})