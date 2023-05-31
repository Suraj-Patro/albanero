import decimal
import unittest

import pytest


class TestExchangeRateServiceQuotation(unittest.TestCase):
    def test_quotation_readme_example(self):
        from app.currency import Currency

        assert self._execute_sut(Currency.PLN, Currency.EUR) == decimal.Decimal(
            "0.2197802197802197802197802198"
        )

    def test_quotation_eur_success(self):
        from app.currency import Currency

        assert self._execute_sut(Currency.EUR, Currency.PLN) == decimal.Decimal("4.55")
        assert self._execute_sut(Currency.PLN, Currency.EUR) == decimal.Decimal(
            "0.2197802197802197802197802198"
        )

    def test_quotation_should_return_decimal(self):
        from app.currency import Currency

        result = self._execute_sut(Currency.PLN, Currency.EUR)

        assert isinstance(result, decimal.Decimal)

    def test_invalid_currency_argument(self):
        from app.currency import Currency
        from app.exceptions import QuotationError

        with pytest.raises(QuotationError):
            assert self._execute_sut(Currency.EUR, "EUR")

    def test_invalid_currency_rate(self):
        from app.currency import Currency
        from app.exceptions import QuotationError

        with pytest.raises(QuotationError):
            assert self._execute_sut(Currency.EUR, Currency.ZAR)

    def setUp(self):
        from app.exchange_rate import ExchangeRateService

        self._sut = ExchangeRateService().quotation

    def _execute_sut(self, origin, target):
        return self._sut(origin, target)
