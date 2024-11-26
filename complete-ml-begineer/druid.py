import pandas as pd
import requests
import base64
import requests
import logging
from .enums import SqlResultFormat
from .constants import DRUID_USER, DRUID_PASSWORD

###############################################################################

class DruidError(Exception):
    """ In case data is not returned from druid """
    def __init__(self, message="Druid Error"):
        self.message = message
        super().__init__(self.message)
        
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

def make_bs64(to_encode:str):
    sample_string_bytes = to_encode.encode("ascii")
    base64_bytes = base64.b64encode(sample_string_bytes)
    return base64_bytes.decode("ascii")

def make_basic_auth(user:str,
                    password:str):
    
    base64_string = make_bs64(f'{user}:{password}')
    return f"Basic {base64_string}"

class DruidQueryRequest:
    def __init__(self,
                 url,
                 json,
                 headers,
                 timeout) -> None:
        self.url = url 
        self.json=json
        self.headers=headers
        self.timeout=timeout

class DruidRequest:
    def __init__(self,user,password) -> None:
        self.authkey = None
        self.url = "http://mridruidquery.redbus.com:8888/druid/v2/sql/"
        self.user = user
        self.password = password
        self.headers = None
        self.body=None
        self.timeout_duration = 60
                   

    def get_url(self,):
        return self.url

    def get_body(self,
                 q:str=''):
        return {"query":q,
                "resultFormat" : SqlResultFormat.ARRAY.value,
                "header":True,
                # "sqlTypesHeader" : True
                }

    def get_headers(self,):
        if not self.headers:
            self.headers= { 'Content-Type':"application/json",
                            "Authorization": make_basic_auth(self.user,
                                                        self.password)}
            logger.info("setting header")
        return self.headers

    def _make_request(self,q):
        logger.debug("making request...")
        return DruidQueryRequest(url=self.get_url(),
                                json=self.get_body(q),
                                headers=self.get_headers(),
                                timeout=self.timeout_duration)
        

    def execute_query(self,q:str):
        """takes a (formatted ) query and executes it using druid_db 

        Args:
            q (str): formatted SQL query for execution

        Raises:
            DruidError: errors to catch some possible druid/http exceptions

        Returns:
            _type_: json in the result type described in resultFormat: 
        """

        try:
            # logger.debug("headers: %s",self.headers)
            logger.debug("running query:")
            logger.debug(q)
            query_request = self._make_request(q)
            logger.debug(query_request.__dict__)
            res = requests.post(**query_request.__dict__)
            # res.raise_for_status()
            logger.debug("response.... %s",res)
            
            if res.status_code==200:
                json_data = res.json()
            elif res.status_code==400:
                json_data = res.json()
            else:
                logger.error(f"error fetching data status code: {res.status_code}")

            if isinstance(json_data, list):
                # create df based on sql result format
                return pd.DataFrame(json_data[1:], columns=json_data[0])
            else:
                error = str(json_data.get("error", "Unknown error occurred in database response."))
                error_message = str(json_data.get("errorMessage"))[:100]
                raise DruidError(f"{error} :{error_message}")
        
        except requests.exceptions.Timeout as timeout_exception:
            logger.error(f"Query execution timed out: {timeout_exception}")
            raise timeout_exception(f"Query execution timed out after {self.timeout_duration} seconds") from timeout_exception
        except requests.exceptions.RequestException as e:
            raise DruidError(f"Request failed: {e}")
        except ValueError as e:
            raise DruidError(f"Invalid JSON response: {e}")
        # except Exception as e:
        #     raise DruidError(f"Unexpected error occurred: {e}")



#init a singleton druid request for all use
druid_db = DruidRequest(user=DRUID_USER,
                  password=DRUID_PASSWORD)




# if __name__=='__main__':

#     ## tests

#     from queries.detection_queries import query_bus_cr_
#     params = {"st_":'2023-11-20 12:00:00',"delta":60}
    
#     query_template = query_bus_cr_
    
#     def test_execute_query():
#         rjson = druid_db.execute_query(query_template.format(**params))
#         print(rjson,"PASS")

   
