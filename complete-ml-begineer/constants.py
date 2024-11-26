import logging
from pathlib import Path
import os
from config_handler import app_configs
###############################################################################


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

##druid config
druid:dict = app_configs.get('druid')
DRUID_USER = druid.get('user')
DRUID_PASSWORD =  druid.get('password')

mysql:dict = app_configs.get('mysql')
endpoint=mysql.get('host')
username= mysql.get('username')
PASSWORD= mysql.get('password')
dbname=mysql.get('dbname')


DATABASE_URL = f'mysql+mysqlconnector://{username}:{PASSWORD}@{endpoint}/{dbname}'

tz_mapping = {
              "latam":'America/Lima',
              "ind":'Asia/Kolkata',
              "mys":'Asia/Kuala_Lumpur',
              "sgp":'Asia/Singapore',
              "idn":'Asia/Jakarta',
              "UTC":None
              }

##redshift config
redshift:dict = app_configs.get('redshift')
RD_DRIVER= redshift.get('driver')
RD_HOST =redshift.get('host')
RD_PORT = redshift.get('port')

##redshift anomaly database config
ANOMALYDB = redshift.get('dbname')
AD_USER=redshift.get('user')
AD_PWD=redshift.get('password')

##spaces webook
WEBHOOK_URL_TEST = 'https://chat.googleapis.com/v1/spaces/AAAAi5pVgTg/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=-49RoDiTZGmZwR1TgsU8PiBIlVVyMEM0HIT8RQfHWpE'
WEBHOOK_URL_RIG = 'https://chat.googleapis.com/v1/spaces/AAAAMrv_pFs/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=6qSfI4KcpDimB02nrd48rAPcJRkI5udnAeZBk2J8770'

##smtp server config
smtp:dict = app_configs.get('smtp')
SMTP_HOST = smtp.get('host')
SMTP_STARTTLS = smtp.get('SMTP_STARTTLS')
SMTP_SSL = smtp.get('SMTP_SSL')
SMTP_USER = smtp.get('user')
SMTP_PORT = smtp.get('port')
SMTP_PASSWORD = smtp.get('password')

##smtp sending config
SMTP_MAIL_FROM = "superalert@redbus.in"
SMTP_FROM_NAME='alerts'

## email configuration at levl of smtp
SMTP_TO_EMAILS=['anubhav.s@redbus.com',]
SMTP_ERROR_EMAIL = ['anubhav.s@redbus.com','tanushree.hr@redbus.com']
# SMTP_ERROR_EMAIL = ['anubhav.s@redbus.com',]
#Email service default params
SMTP_MAIL_SUBJECT= 'testing alert'
SMTP_PLAIN_BODY= "testing"

##model registry default params 
REG_TYPE = 'REMOTE'
# REG_URL = 'http://127.0.0.1:8000'
REG_URL = 'http://10.5.40.167:6002'

##locations
UTILS_DIR = Path(__file__).parent.resolve()
ROOT_DIR = Path(UTILS_DIR).parent.resolve()
# LOG_DIR = Path(ROOT_DIR,'logs')

RESOURCE_DIR  = Path(ROOT_DIR,'resources')
OUTPUT_DIR  = Path(UTILS_DIR,'output')
TEMPLATE_DIR = Path(RESOURCE_DIR,'templates')

def setup_logs_directory():
    LOG_DIR = Path(ROOT_DIR,'logs')
    LOG_DIR = Path('/var','log','adservicepp')
    if not os.path.exists(LOG_DIR):
        try:
            os.makedirs(LOG_DIR)
            return LOG_DIR
        except PermissionError:
            logger.exception(f"Unable to create directory {LOG_DIR}. Trying locally",)

            LOG_DIR = Path(ROOT_DIR,'logs')
            if not os.path.exists(LOG_DIR):
                try:
                    os.makedirs(LOG_DIR)
                    return LOG_DIR
                except Exception as e:
                    logger.exception(f"Unable to create directory {LOG_DIR}. %s",e)
    else:
        return LOG_DIR
    

# LOG_DIR  = setup_logs_directory()

logger.info("Sending alerts to configured Emails as: %s",SMTP_TO_EMAILS)
# logger.info("Log directory %s",LOG_DIR)
# print(LOG_DIR.__str__())