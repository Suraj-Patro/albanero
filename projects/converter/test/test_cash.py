import decimal
import unittest
from unittest import mock

import pytest


class TestCash(unittest.TestCase):
    def test_cash_instance_eur(self):
        from app.currency import Currency

        cash = self._execute_sut("13.37", Currency.EUR)

        assert cash
        assert cash._amount == cash.amount == decimal.Decimal("13.37")
        assert cash._currency == cash.currency == Currency.EUR

    def test_cash_instance_pln(self):
        from app.currency import Currency

        cash = self._execute_sut("500", Currency.PLN)

        assert cash
        assert cash._amount == cash.amount == decimal.Decimal("500")
        assert cash._currency == cash.currency == Currency.PLN

    def test_to_string(self):
        from app.currency import Currency

        assert str(self._execute_sut("500", Currency.PLN)) == "500.0000 PLN"
        assert str(self._execute_sut("21.1233", Currency.USD)) == "21.1233 USD"

    def test_invalid_amount(self):
        from app.currency import Currency

        with pytest.raises(decimal.InvalidOperation):
            self._execute_sut("1 3424.2,2", Currency.EUR)

    def test_invalid_currency(self):
        from app.exceptions import InvalidCurrencyError

        with pytest.raises(InvalidCurrencyError):
            self._execute_sut("13.37", mock.Mock(value="JPY"))

    def test_invalid_currency_type(self):
        from app.exceptions import InvalidCurrencyError

        with pytest.raises(InvalidCurrencyError):
            self._execute_sut("13.37", "JPY")

    def setUp(self):
        from app.cash import Cash

        self._sut = Cash

    def _execute_sut(self, amount, currency):
        return self._sut(amount, currency)
