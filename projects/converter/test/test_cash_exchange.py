import decimal
import unittest


class CashExchangeTestCase:
    def test_convert_to_same_currency(self):
        from app.cash import Cash

        cash = self._execute_sut(target_currency=self._cash.currency)

        assert isinstance(cash, Cash)
        assert cash == self._cash
        assert id(cash) == id(self._cash)

    def test_convert_to_other_currency(self):
        from app.cash import Cash
        from app.currency import Currency

        cash = self._execute_sut(target_currency=Currency.PLN)

        assert isinstance(cash, Cash)
        assert cash.amount == decimal.Decimal("455.0000")
        assert cash.currency == Currency.PLN

    def _execute_sut(self, target_currency):
        raise NotImplementedError


class TestCashExchangeTo(CashExchangeTestCase, unittest.TestCase):
    def setUp(self):
        from app.cash import Cash
        from app.currency import Currency

        self._cash = Cash("100", Currency.EUR)
        self._sut = self._cash.to

    def _execute_sut(self, target_currency):
        return self._sut(target_currency)
