from typing import Dict, List, Optional, Any
from pydantic import BaseModel

class Instrument(BaseModel):
    symbol: str; assetType: str; cusip: Optional[str] = None; description: Optional[str] = None
    class Config: extra = "ignore"

class Position(BaseModel):
    shortQuantity: float = 0.0; averagePrice: float; currentDayProfitLoss: float; currentDayProfitLossPercentage: float
    longQuantity: float; settledLongQuantity: float; settledShortQuantity: float = 0.0; agedQuantity: float = 0.0
    instrument: Instrument; marketValue: float; maintenanceRequirement: float; averageLongPrice: float
    averageShortPrice: float = 0.0; taxLotAverageLongPrice: float; taxLotAverageShortPrice: float = 0.0
    longOpenProfitLoss: float; shortOpenProfitLoss: float = 0.0; previousSessionLongQuantity: float
    previousSessionShortQuantity: float = 0.0; currentDayCost: float
    class Config: extra = "ignore"

class Balances(BaseModel):
    availableFunds: Optional[float] = None; availableFundsNonMarginableTrade: Optional[float] = None
    buyingPower: Optional[float] = None; buyingPowerNonMarginableTrade: Optional[float] = None
    dayTradingBuyingPower: Optional[float] = None; dayTradingBuyingPowerCall: Optional[float] = None
    equity: Optional[float] = None; equityPercentage: Optional[float] = None; longMarginValue: Optional[float] = None
    maintenanceCall: Optional[float] = None; maintenanceRequirement: Optional[float] = None; marginBalance: Optional[float] = None
    regTCall: Optional[float] = None; shortBalance: Optional[float] = None; shortMarginValue: Optional[float] = None
    sma: Optional[float] = None; isInCall: Optional[bool] = None; stockBuyingPower: Optional[float] = None; optionBuyingPower: Optional[float] = None

class SecuritiesAccount(BaseModel):
    accountNumber: str; roundTrips: int; isDayTrader: bool; isClosingOnlyRestricted: bool; pfcbFlag: bool
    positions: Optional[List[Position]] = []; initialBalances: Dict[str, Any]; currentBalances: Balances; projectedBalances: Balances

class AccountNumberInfo(BaseModel):
    accountNumber: str; hashValue: str

class AccountInfo(BaseModel):
    securitiesAccount: SecuritiesAccount
    @property
    def accountNumber(self) -> str: return self.securitiesAccount.accountNumber
    @property  
    def hashValue(self) -> str: return self.securitiesAccount.accountNumber
    class Config: extra = "ignore"

class OptionDeliverable(BaseModel):
    symbol: str; quantity: float; assetType: str

class OptionContract(BaseModel):
    putCall: str; symbol: str; description: Optional[str]; exchangeName: Optional[str]; bid: float; ask: float; last: float; mark: float
    bidSize: int; askSize: int; lastSize: Optional[int]; highPrice: Optional[float]; lowPrice: Optional[float]; openPrice: Optional[float]
    closePrice: Optional[float]; totalVolume: int; tradeDate: Optional[str] = None; tradeTimeInLong: Optional[int]; quoteTimeInLong: Optional[int]
    netChange: float; volatility: Optional[float]; delta: Optional[float]; gamma: Optional[float]; theta: Optional[float]; vega: Optional[float]
    rho: Optional[float]; openInterest: int; timeValue: Optional[float]; theoreticalOptionValue: Optional[float]; theoreticalVolatility: Optional[float]
    strikePrice: float; expirationDate: str; daysToExpiration: int; expirationType: str; multiplier: float; settlementType: str
    deliverableNote: Optional[str]; isIndexOption: Optional[bool] = None; percentChange: float; markChange: float; markPercentChange: float
    intrinsicValue: Optional[float]; inTheMoney: bool; mini: bool; nonStandard: bool; pennyPilot: bool; deliverables: Optional[List[OptionDeliverable]] = None
    class Config: extra = "ignore"

class OptionChainResponse(BaseModel):
    symbol: str; status: str; underlying: Optional[Dict] = None; strategy: str; interval: float; isDelayed: bool; isIndex: bool
    interestRate: float; underlyingPrice: float; volatility: float; daysToExpiration: int; numberOfContracts: int
    callExpDateMap: Dict[str, Dict[str, List[OptionContract]]]; putExpDateMap: Dict[str, Dict[str, List[OptionContract]]]
    class Config: extra = "ignore"

class QuoteReference(BaseModel):
    cusip: Optional[str] = None; description: Optional[str] = None; exchange: Optional[str] = None; exchangeName: Optional[str] = None
    otcMarketTier: Optional[str] = None; contractType: Optional[str] = None; daysToExpiration: Optional[int] = None
    expirationDay: Optional[int] = None; expirationMonth: Optional[int] = None; expirationYear: Optional[int] = None
    isPennyPilot: Optional[bool] = None; lastTradingDay: Optional[int] = None; multiplier: Optional[int] = None
    settlementType: Optional[str] = None; strikePrice: Optional[float] = None; underlying: Optional[str] = None; uvExpirationType: Optional[str] = None
    class Config: extra = "ignore"

class QuoteData(BaseModel):
    askPrice: Optional[float] = None; askSize: Optional[int] = None; askTime: Optional[int] = None; bidPrice: Optional[float] = None
    bidSize: Optional[int] = None; bidTime: Optional[int] = None; closePrice: Optional[float] = None; highPrice: Optional[float] = None
    lastPrice: Optional[float] = None; lastSize: Optional[int] = None; lowPrice: Optional[float] = None; mark: Optional[float] = None
    markChange: Optional[float] = None; markPercentChange: Optional[float] = None; netChange: Optional[float] = None
    netPercentChange: Optional[float] = None; openPrice: Optional[float] = None; quoteTime: Optional[int] = None
    securityStatus: Optional[str] = None; totalVolume: Optional[int] = None; tradeTime: Optional[int] = None; volatility: Optional[float] = None
    openInterest: Optional[int] = None; delta: Optional[float] = None; gamma: Optional[float] = None; theta: Optional[float] = None
    vega: Optional[float] = None; rho: Optional[float] = None; impliedVolatility: Optional[float] = None; theoreticalValue: Optional[float] = None
    class Config: extra = "ignore"

class QuoteFundamental(BaseModel):
    avg10DaysVolume: Optional[float] = None; avg1YearVolume: Optional[float] = None; divAmount: Optional[float] = None
    divFreq: Optional[int] = None; divPayAmount: Optional[float] = None; divYield: Optional[float] = None; eps: Optional[float] = None
    fundLeverageFactor: Optional[float] = None; peRatio: Optional[float] = None
    class Config: extra = "ignore"

class ErrorDetail(BaseModel):
    id: Optional[str] = None; status: Optional[str] = None; title: Optional[str] = None; detail: Optional[str] = None
    class Config: extra = "ignore"

class ErrorResponse(BaseModel):
    errors: Optional[List[ErrorDetail]] = None; invalidSymbols: Optional[List[str]] = None
    class Config: extra = "ignore"

class QuoteResponse(BaseModel):
    assetMainType: Optional[str] = None; assetSubType: Optional[str] = None; symbol: Optional[str] = None; quoteType: Optional[str] = None
    realtime: Optional[bool] = None; ssid: Optional[int] = None; reference: Optional[QuoteReference] = None; quote: Optional[QuoteData] = None
    fundamental: Optional[QuoteFundamental] = None; regular: Optional[Dict[str, Any]] = None; extended: Optional[Dict[str, Any]] = None
    class Config: extra = "ignore"

class ExpirationDate(BaseModel):
    expirationDate: str; daysToExpiration: int; expirationType: str; standard: bool

class ExpirationChainResponse(BaseModel):
    expirationList: List[ExpirationDate]
    class Config: extra = "ignore"

class Candle(BaseModel):
    open: float; high: float; low: float; close: float; volume: int; datetime: int

class PriceHistoryResponse(BaseModel):
    symbol: str; empty: bool; previousClose: Optional[float] = None; previousCloseDate: Optional[int] = None; candles: List[Candle]
    class Config: extra = "ignore"

class OrderLegInstrument(BaseModel):
    symbol: str; assetType: str = "EQUITY"

class OrderLeg(BaseModel):
    orderLegType: str = "EQUITY"; legId: int = 1; instrument: OrderLegInstrument; instruction: str; quantity: float; quantityType: str = "ALL_SHARES"

class OrderRequest(BaseModel):
    session: str = "NORMAL"; duration: str = "DAY"; orderType: str = "MARKET"; complexOrderStrategyType: str = "NONE"
    quantity: float; orderLegCollection: List[OrderLeg]; orderStrategyType: str = "SINGLE"

class OrderActivity(BaseModel):
    activityType: str; executionType: str; quantity: float; orderRemainingQuantity: float; executionLegs: List[Dict[str, Any]]
    class Config: extra = "ignore"

class Order(BaseModel):
    session: str; duration: str; orderType: str; cancelTime: Optional[str] = None; complexOrderStrategyType: str; quantity: float
    filledQuantity: float; remainingQuantity: float; requestedDestination: str; destinationLinkName: Optional[str] = None
    releaseTime: Optional[str] = None; stopPrice: Optional[float] = None; stopPriceLinkBasis: Optional[str] = None
    stopPriceLinkType: Optional[str] = None; stopPriceOffset: Optional[float] = None; stopType: Optional[str] = None
    priceLinkBasis: Optional[str] = None; priceLinkType: Optional[str] = None; price: Optional[float] = None; taxLotMethod: Optional[str] = None
    orderLegCollection: List[OrderLeg]; activationPrice: Optional[float] = None; specialInstruction: Optional[str] = None
    orderStrategyType: str; orderId: int; cancelable: bool; editable: bool; status: str; enteredTime: str; closeTime: Optional[str] = None
    tag: Optional[str] = None; accountNumber: str; orderActivityCollection: Optional[List[OrderActivity]] = []
    replacingOrderCollection: Optional[List[str]] = None; childOrderStrategies: Optional[List[str]] = None; statusDescription: Optional[str] = None
    class Config: extra = "ignore"

class OrderResponse(BaseModel):
    orders: List[Order]
    class Config: extra = "ignore"

class PlaceOrderResponse(BaseModel):
    orderId: str; location: str; correlationId: str
    class Config: extra = "ignore"

def format_option_details(contract: OptionContract) -> str:
    return f"{contract.putCall} {contract.symbol}\nStrike: ${contract.strikePrice:.2f}\nExpiration: {contract.expirationDate}\nBid/Ask: ${contract.bid:.2f}/${contract.ask:.2f}\nVolume: {contract.totalVolume}\nOpen Interest: {contract.openInterest}\nDelta: {contract.delta or 'N/A'}\nIV: {contract.theoreticalVolatility or 'N/A'}"