import decimal
import typing

from app.currency import Currency
from app.rates import RATES
from app.exceptions import QuotationError

class ExchangeRateService:
    _rates = RATES

    def update_rate(self, currency: Currency, rate: decimal.Decimal):
        self._rates[currency] = rate

    def get_rate(self, currency: Currency) -> typing.Optional[decimal.Decimal]:
        try:
            return self._rates[currency]
        except KeyError:
            return None

    def quotation(
        self, origin: Currency, target: Currency
    ) -> typing.Optional[decimal.Decimal]:
        """TODO: Part 2"""
        try:
            return self._rates[origin] / self._rates[target]
            # return self.get_rate(origin) / self.get_rate(target)          # not used as additional function call
        # except KeyError:
        except:         # as no / operation defined for decimal and None
            raise QuotationError



exchange_rate_service = ExchangeRateService()
