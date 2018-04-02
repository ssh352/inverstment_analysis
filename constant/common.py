# encoding: UTF-8
from __future__ import print_function
from enum import Enum, IntEnum, unique


@unique
class QUOTE_TYPE(Enum):
    TICK = '0'
    MIN = '1M'
    FIVEMIN = '5M'
    QUARTERMIN = '15M'
    DAILY = '1d'
    SPECIALBAR = '-1'


@unique
class RUN_MODE(IntEnum):
    REALTIME = 0
    BACKTEST = 1


@unique
class EXCHANGE(Enum):
    SHENZHEN_STOCK_EXCHANGE = 'SZ'
    SHANGHAI_STOCK_EXCHANGE = 'SH'

    SHANGHAI_FUTURES_EXCHANGE = 'SHF'
    ZHENGZHOU_COMMODITIES_EXCHANGE = 'CZC'
    DALIAN_COMMODITIES_EXCHANGE = 'DCE'

    CHINA_FINANCIAL_FUTURES_EXCHANGE = 'CFE'

    SHANGHAI_GOLD_EXCHANGE = 'SGE'

    CHINA_SECURITY_INDEX = 'CSI'

    HONGKONG_EXCHANGES_AND_CLEARING_LIMITED = 'HK'


@unique
class ORDER_TYPE(Enum):
    """We recommend use limit order everywhere."""
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    VWAP = "vwap"


@unique
class ORDER_ACTION(Enum):
    """
    buy and sell for long; short and cover for short.
    other 4 actions are automatically generated by EMS."""
    BUY = "Buy"
    SELL = "Sell"
    SHORT = "Short"
    COVER = "Cover"
    SELLTODAY = "SellToday"
    SELLYESTERDAY = "SellYesterday"
    COVERYESTERDAY = "CoverYesterday"
    COVERTODAY = "CoverToday"

    @classmethod
    def is_positive(cls, action):
        return (action == cls.BUY
                or action == cls.COVER
                or action == cls.COVERYESTERDAY
                or action == cls.COVERTODAY)

    @classmethod
    def is_negative(cls, action):
        return (action == cls.SELL
                or action == cls.SHORT
                or action == cls.SELLTODAY
                or action == cls.SELLYESTERDAY)


@unique
class ORDER_STATUS(Enum):
    NEW = "New"
    REJECTED = "Rejected"
    ACCEPTED = "Accepted"
    FILLED = "Filled"
    CANCELLED = "Cancelled"


@unique
class TASK_STATUS(Enum):
    NEW = "New"
    REJECTED = "Rejected"
    ACCEPTED = "Accepted"
    DONE = "Done"
    CANCELLED = "Cancelled"


@unique
class ORDER_TIME_IN_FORCE(Enum):
    FOK = 'fok'
    FAK = 'fak'
    IOC = 'ioc'


@unique
class CALENDAR_CONST(IntEnum):
    TRADE_DAYS_PER_YEAR = 242


@unique
class DATA_TYPE_DEF(Enum):
    EMPTY_STRING = ''
    EMPTY_UNICODE = u''
    EMPTY_INT = 0
    EMPTY_FLOAT = 0.0