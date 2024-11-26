
from enum import Enum
class AlertStatus(str,Enum):
    STARTED = 'STARTED'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'

class Environment(str,Enum):
    LOCAL = 'LOCAL'
    DEV = 'DEV'
    PROD = 'PROD'
    
class EventSrc(str,Enum):
    capi= "CAPI"
    neon= "NEON"

# metrics = ["conversion","dropoff","newuser","uxpercentage"]


class Tables(Enum):
    """ tables used for a service through the dev lifecycle
    while creating a new service that requires new table, create similar 
    enum class. this table is generic for many uses. spv means supervised."""
    
    PROD = 'prod_anomaly_detection_spv'
    DEV = 'dev_anomaly_detection_spv'
    LOCAL = 'test'
    
    

class NEON(str,Enum):
    confirm = "Orders-ConfirmOrder"
    

class CAPI(str,Enum):
    tco = "Tentative-CreateOrder"
    search= "Search-Routes"
    seatlayout= "SeatLayout-ViewSeats"
    custinfo = "Tentative-MpaxAttribute"
    getmpax = "Tentative-GetMpaxAttribute"
    tentative= "Tentative-CreateOrder"
    payment="Payment-MakePayment"
    conclude = "Payment-Conclude"
    getRoutes = "Booking-GetRoutes"
    mpaxpost = "Booking-GetAllMpaxPost"
    createorder = "Order-CreateOrder"
    getorder = "Order-GetOrder"
    paymentinstrument = "Payment-PaymentInstruments" 
    payitems = "Payment-CreatePaymentItems"
    confirmticket = "Order-ConfirmTicket"
    payconclude = "Payment-Conclude"

# print([CAPI[x.name].value for x in CAPI])
# TODO: how do you handle case problems in country code ? is this issue even possible here ?
class Country(str,Enum):
    India = "IND"
    Colombia = "COL"
    Peru = "PER"
    Indonesia = "IDN"
    Malaysia = "MYS"
    Singapore = "SGP"


class Channel(str,Enum):
    app = "MOBILE_APP"
    web = "MOBILE_WEB"

class OS(str,Enum):
    android = "Android"
    ios = "iOS"
    mweb = "MOBILE_WEB"
    web = "WEB_DIRECT"
    # others = "others"
    # all = "all"



class SqlResultFormat(Enum):
    """
    Result formats used in SQL.
    """
    OBJECT = 'object'
    ARRAY = 'array'
    OBJECT_LINES = 'objectLines'
    ARRAY_LINES = 'arrayLines'
    CSV = 'csv'
