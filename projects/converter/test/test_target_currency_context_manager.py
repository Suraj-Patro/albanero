import decimal
import unittest


class TestTargetCurrencyContextManager(unittest.TestCase):
    def test_target_currency_sum(self):
        from app.currency import Currency
        from app.cash import Cash

        result = self._execute_sut(
            Currency.EUR, lambda: Cash("10", Currency.PLN) + Cash("15", Currency.PLN)
        )

        assert result.currency == Currency.EUR
        assert result.amount == decimal.Decimal("5.4945")

    def test_target_currency_sub(self):
        from app.currency import Currency
        from app.cash import Cash

        result = self._execute_sut(
            Currency.USD, lambda: Cash("1", Currency.EUR) - Cash("4.55", Currency.PLN)
        )

        assert result.currency == Currency.USD
        assert result.amount == decimal.Decimal("0.0000")

    def test_context_manger_should_clean(self):
        from app.currency import Currency
        from app.cash import Cash

        result = self._execute_sut(
            Currency.USD, lambda: Cash("1", Currency.EUR) + Cash("4.55", Currency.PLN)
        )

        assert result.currency == Currency.USD
        assert result.amount == decimal.Decimal("2.3932")

        after_exit = Cash("1", Currency.EUR) + Cash("4.55", Currency.PLN)
        assert after_exit.currency == Currency.EUR
        assert after_exit.amount == decimal.Decimal("2.0000")

    def test_readme_example(self):
        from app.currency import Currency
        from app.cash import Cash

        value = self._execute_sut(
            Currency.EUR, lambda: Cash("10", Currency.PLN) + Cash("12", Currency.PLN)
        )

        assert value.currency == Currency.EUR
        assert value.amount < 22

    def setUp(self):
        from app.cash import TargetCurrency

        self._sut = TargetCurrency

    def _execute_sut(self, currency, cash_operation):
        with self._sut(currency):
            return cash_operation()
