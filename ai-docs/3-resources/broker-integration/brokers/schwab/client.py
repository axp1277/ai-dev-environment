import requests
from typing import Dict, List, Optional
from loguru import logger
from src.brokers.schwab.auth import SchwabAuth
from src.brokers.schwab.models import *

class SchwabClient:
    def __init__(self):
        self.auth = SchwabAuth()
        self.base_url = "https://api.schwabapi.com"
        self.market_data_url = f"{self.base_url}/marketdata/v1"
        self.trader_url = f"{self.base_url}/trader/v1"

    def _request(self, method: str, endpoint: str, base_url: Optional[str] = None, **kwargs) -> requests.Response:
        url = f"{base_url or self.market_data_url}/{endpoint}"
        headers = kwargs.get('headers', {})
        headers.update(self.auth.get_auth_headers())
        kwargs['headers'] = headers
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code == 401:
                self.auth.refresh_tokens()
                headers.update(self.auth.get_auth_headers())
                response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise

    async def connect(self) -> bool:
        try: self.get_options_chain("SPY", strike_count=1); return True
        except: return False

    def get_options_chain(self, symbol: str, contract_type: str = "ALL", strike_count: Optional[int] = None, include_underlying_quote: bool = True, strategy: str = "SINGLE", interval: Optional[float] = None, strike: Optional[float] = None, range: Optional[str] = None, from_date: Optional[str] = None, to_date: Optional[str] = None, volatility: Optional[float] = None, underlying_price: Optional[float] = None, interest_rate: Optional[float] = None, days_to_expiration: Optional[int] = None, exp_month: Optional[str] = None, option_type: Optional[str] = None) -> OptionChainResponse:
        params = {'symbol': symbol, 'contractType': contract_type, 'includeQuotes': str(include_underlying_quote).lower(), 'strategy': strategy}
        params.update({k: v for k, v in {'strikeCount': strike_count, 'interval': interval, 'strike': strike, 'range': range, 'fromDate': from_date, 'toDate': to_date, 'volatility': volatility, 'underlyingPrice': underlying_price, 'interestRate': interest_rate, 'daysToExpiration': days_to_expiration, 'expMonth': exp_month, 'optionType': option_type}.items() if v is not None})
        data = self._request('GET', 'chains', params=params).json()
        data.setdefault('underlying', {'symbol': symbol, 'price': data.get('underlyingPrice', 0), 'change': 0, 'percentChange': 0})
        return OptionChainResponse(**data)

    def get_quotes(self, symbols: List[str], fields: Optional[List[str]] = None, indicative: bool = False) -> Dict[str, QuoteResponse]:
        params = {'symbols': ','.join(symbols), 'indicative': str(indicative).lower()}
        params.update({'fields': ','.join(fields or [])})
        data = self._request('GET', 'quotes', params=params).json()
        return {s: QuoteResponse(**d) for s, d in data.items()}

    def get_expiration_chain(self, symbol: str) -> ExpirationChainResponse:
        return ExpirationChainResponse(**self._request('GET', 'expirationchain', params={'symbol': symbol}).json())

    def get_price_history(self, symbol: str, period_type: str = "day", period: Optional[int] = None, frequency_type: Optional[str] = None, frequency: Optional[int] = None, start_date: Optional[int] = None, end_date: Optional[int] = None, need_extended_hours_data: bool = False, need_previous_close: bool = True) -> PriceHistoryResponse:
        params = {'symbol': symbol, 'periodType': period_type, 'needExtendedHoursData': str(need_extended_hours_data).lower(), 'needPreviousClose': str(need_previous_close).lower()}
        params.update({k: v for k, v in {'period': period, 'frequencyType': frequency_type, 'frequency': frequency, 'startDate': start_date, 'endDate': end_date}.items() if v is not None})
        return PriceHistoryResponse(**self._request('GET', 'pricehistory', params=params).json())

    def get_futures_price_history(self, symbol: str, period_type: str = "day", period: Optional[int] = None, frequency_type: str = "minute", frequency: int = 5, start_date: Optional[int] = None, end_date: Optional[int] = None, need_extended_hours_data: bool = True, need_previous_close: bool = True) -> PriceHistoryResponse:
        params = {'symbol': symbol, 'periodType': period_type, 'frequencyType': frequency_type, 'frequency': frequency, 'needExtendedHoursData': str(need_extended_hours_data).lower(), 'needPreviousClose': str(need_previous_close).lower()}
        params.update({k: v for k, v in {'period': period, 'startDate': start_date, 'endDate': end_date}.items() if v is not None})
        return PriceHistoryResponse(**self._request('GET', 'pricehistory', params=params).json())

    def get_orders(self, from_entered_time: str, to_entered_time: str, account_number: Optional[str] = None, max_results: Optional[int] = 3000, status: Optional[str] = None) -> List[Order]:
        params = {'fromEnteredTime': from_entered_time, 'toEnteredTime': to_entered_time, 'maxResults': max_results or 3000}
        data = self._request('GET', 'orders', base_url=self.trader_url, params=params).json()
        return [Order(**{**d, 'accountNumber': str(d['accountNumber'])}) for d in data]

    def get_account_numbers(self) -> List[AccountNumberInfo]:
        return [AccountNumberInfo(**account) for account in self._request('GET', 'accounts/accountNumbers', base_url=self.trader_url).json()]

    def get_accounts(self, include_positions: bool = True) -> List[AccountInfo]:
        account_numbers = {acc.accountNumber: acc.hashValue for acc in self.get_account_numbers()}
        data = self._request('GET', 'accounts', base_url=self.trader_url, params={'fields': 'positions'} if include_positions else {}).json()
        return [AccountInfo(**account_data) for account_data in data]

    def place_order(self, account_number: str, symbol: str, quantity: float, instruction: str = "BUY", order_type: str = "MARKET", session: str = "NORMAL", duration: str = "DAY") -> PlaceOrderResponse:
        order_request = {"session": session, "duration": duration, "orderType": order_type, "complexOrderStrategyType": "NONE", "quantity": quantity, "orderStrategyType": "SINGLE", "orderLegCollection": [{"orderLegType": "EQUITY", "legId": 1, "instrument": {"symbol": symbol, "assetType": "EQUITY"}, "instruction": instruction, "quantity": quantity, "quantityType": "SHARES"}]}
        try:
            response = self._request('POST', f'accounts/{account_number}/orders', base_url=self.trader_url, json=order_request)
            return PlaceOrderResponse(orderId=response.headers.get('Location', '').split('/')[-1], location=response.headers.get('Location', ''), correlationId=response.headers.get('Schwab-Client-CorrelId', ''))
        except requests.exceptions.HTTPError as e:
            try: error_data = e.response.json(); error_message = error_data.get('message', str(e)) + (f"\nErrors: {', '.join(error_data.get('errors', []))}" if error_data.get('errors') else '')
            except: error_message = str(e)
            raise Exception(f"Failed to place order: {error_message}")

    def get_open_positions(self, symbol: Optional[str] = None) -> List[Position]:
        accounts = self.get_accounts(include_positions=True)
        return [p for a in accounts for p in (a.securitiesAccount.positions or [])]