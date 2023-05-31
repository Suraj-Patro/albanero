import unittest

import pytest


class TestCurrencyEnum(unittest.TestCase):
    def test_currency_enum_that_exists(self):
        assert self._sut.PLN
        assert self._sut.CZK
        assert self._sut.DKK
        assert self._sut.EUR
        assert self._sut.GBP
        assert self._sut.NOK
        assert self._sut.USD
        assert self._sut.ZAR

    def test_currency_not_exists(self):
        with pytest.raises(AttributeError):
            assert self._sut.JPY

    def setUp(self):
        from app.currency import Currency

        self._sut = Currency

    def _execute_sut(self):
        return self._sut


class TestCurrencyEnumIsMember(unittest.TestCase):
    def test_currency_exists(self):
        assert self._execute_sut("EUR") is True

    def test_currency_not_exists(self):
        assert self._execute_sut("JPY") is False

    def setUp(self):
        from app.currency import Currency

        self._sut = Currency.is_member

    def _execute_sut(self, value):
        return self._sut(value)
