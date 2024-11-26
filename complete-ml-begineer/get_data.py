import logging
from enum import Enum
import pandas as pd
from druid import druid_db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 


class TSFreq(Enum):
    PT1M = '1T'
    PT5M = '5T'
    PT3M = '3T'
    PT15M = '15T'

class TrafficScope:
    def __init__(self,
                 country=None,
                 bu=None,
                 channel=None,
                 os_=None,
                 ) -> None:
        self.Country = country
        self.BU = bu
        self.Channel = channel
        self.OS = os_

    def to_sql_where_clause(self) -> str:
        # TODO: write test case for this
        non_none_items = {key: value for key, value in self.__dict__.items() if
                          value is not None}
        # filters = ' AND '.join([f'"{key}" = \'{value}\'' for key, value in non_none_items.items()])
        # return filters
        filters = []
        for key, value in non_none_items.items():
            # key = str(key).lower()
            if isinstance(value, list):
                # If it's a list, use IN clause
                value_str = ', '.join([f'\'{item}\'' for item in value])
                filters.append(f'"{key}" IN ({value_str})')
            else:
                # If it's a single value, use equality
                filters.append(f'"{key}" = \'{value}\'')

        # TODO: what happens if filters are empty ?
        return ' AND '.join(filters)
    
    def to_sql_where_clause_redshift(self) -> str:
        # TODO: write test case for this
        non_none_items = {key: value for key, value in self.__dict__.items() if
                          value is not None}
        # filters = ' AND '.join([f'"{key}" = \'{value}\'' for key, value in non_none_items.items()])
        # return filters
        filters = []
        for key, value in non_none_items.items():
            key = str(key).lower()
            if isinstance(value, list):
                # If it's a list, use IN clause
                value_str = ', '.join([f'\'{item}\'' for item in value])
                filters.append(f'"{key}" IN ({value_str})')
            else:
                # If it's a single value, use equality
                filters.append(f'"{key}" = \'{value}\'')

        # TODO: what happens if filters are empty ?
        return ' AND '.join(filters)

    def exclude_none(self):
        # return [value for value in self.__dict__.values() if value is not None]
        return [value if not isinstance(value, list) else 'WEB' for value in
                self.__dict__.values() if value is not None]

    def get_str(self) -> str:
        return ' '.join(self.exclude_none())

    # def __repr__(self):
    #     return self.to_sql_where_clause()


class QueryParamsBase:
    def __init__(self) -> None:
        pass

class QueryParams(QueryParamsBase):
    # TODO: python has typed argument declaration, can't we use it here for brevity ?
    def __init__(self,
                 delta: int,
                 delta_unit: str,
                 scope: TrafficScope,
                 grain: TSFreq = TSFreq.PT15M
                 ) -> None:
        self.delta = delta
        self.delta_unit = delta_unit
        self.grain = grain
        self.scope = scope

class QueryExecutionError(Exception):
    """Exception raised for errors during query execution."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def execute_query_dev_(query_template: str,
                       params: QueryParams,
                       ts: str):
    try:
        # temporary hotfix need to check why params.scope is coming as
        # as  TrafficScope object in one detect() and as str in next
        # for view data

        if not isinstance(params.scope, str):
            sc = params.scope.to_sql_where_clause()
        else:
            sc = params.scope

        if isinstance(params.grain, TSFreq):
            params.grain = params.grain.name
        elif isinstance(params.grain, str):
            params.grain = params.grain

        if not isinstance(params, dict):
            q_params = params.__dict__
        else:
            raise TypeError("query params required in format")
        q_params['st_'] = ts
        q_params['scope'] = sc
        print(query_template.format(**q_params))
        res = druid_db.execute_query(query_template.format(**q_params))
        
        logger.debug("query res:")
        # logger.debug(res)
        logger.debug(type(res))

        if isinstance(res, list):
            df =  pd.DataFrame(res[1:], columns=res[0])
            logger.debug("queryyy res")
            logger.debug(df.columns)
            # logger.debug(df.head(5).to_string())

            return df 
        elif isinstance(res, pd.DataFrame):
            logger.debug("DF RETURNED")
            # raise requests.exceptions.Timeout 
            return res
        else:
            # logger.info("EROR KARO")
            return res
        
    except Exception as e:

        logger.info("ERROR Timeout")
        raise logger.info(f"Query Timed Out, detail: {e}")
    