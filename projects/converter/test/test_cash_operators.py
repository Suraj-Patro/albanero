import decimal
import operator
import unittest


class CashOperatorTestCase(unittest.TestCase):
    @staticmethod
    def assert_result(result, expected_amount, expected_currency):
        from app.cash import Cash

        assert isinstance(result, Cash)
        assert result.amount == expected_amount
        assert result.currency == expected_currency
        assert result == Cash(expected_amount, expected_currency)

    def setUp(self):
        from app.currency import Currency

        self._usd = Currency.USD
        self._eur = Currency.EUR
        self._pln = Currency.PLN


class TestCashAdd(CashOperatorTestCase):
    def test_add_two_cash_instance_same_currency(self):
        from app.cash import Cash

        self._obj1 = Cash("100", self._usd)
        self._obj2 = Cash("28", self._usd)

        result = self._execute_sut()

        self.assert_result(result, decimal.Decimal("128"), self._usd)

    def test_add_negative_amount(self):
        from app.cash import Cash

        self._obj1 = Cash("100", self._usd)
        self._obj2 = Cash("-28", self._usd)

        result = self._execute_sut()

        self.assert_result(result, decimal.Decimal("72"), self._usd)

    def test_add_two_cash_instance_different_currency(self):
        from app.cash import Cash

        self._obj1 = Cash("100", self._pln)
        self._obj2 = Cash("28", self._usd)

        result = self._execute_sut()

        self.assert_result(result, decimal.Decimal("206.4672"), self._pln)

    def test_add_integer_from_right(self):
        from app.cash import Cash

        self._obj1 = Cash("100", self._usd)
        self._obj2 = 15

        result = self._execute_sut()

        self.assert_result(result, decimal.Decimal("115.0000"), self._usd)

    def test_add_integer_from_left(self):
        from app.cash import Cash

        self._obj1 = 15
        self._obj2 = Cash("100", self._usd)

        result = self._execute_sut()

        self.assert_result(result, decimal.Decimal("115.0000"), self._usd)

    def setUp(self):
        super().setUp()

        self._obj1 = None
        self._obj2 = None

    def _execute_sut(self):
        return self._obj1 + self._obj2

    def _execute_sut_sum(self):
        return sum([self._obj1, self._obj2])


class TestCashSubtract(CashOperatorTestCase):
    def test_minus_two_cash_instance_same_currency(self):
        from app.cash import Cash

        self._obj1 = Cash("100", self._usd)
        self._obj2 = Cash("40", self._usd)

        result = self._execute_sut()

        self.assert_result(result, decimal.Decimal("60"), self._usd)

    def test_minus_two_cash_instance_different_currency(self):
        from app.cash import Cash

        self._obj1 = Cash("100", self._pln)
        self._obj2 = Cash("25", self._usd)

        result = self._execute_sut()

        self.assert_result(result, decimal.Decimal("4.9400"), self._pln)

    def setUp(self):
        super().setUp()

        self._obj1 = None
        self._obj2 = None

    def _execute_sut(self):
        return self._obj1 - self._obj2


class TestCashCompare(CashOperatorTestCase):
    def test_equality(self):
        from app.cash import Cash

        assert Cash("100", self._usd) == Cash("100", self._usd)
        assert Cash("100", self._usd) >= Cash("100", self._usd)
        assert Cash("100", self._usd) <= Cash("100", self._usd)

    def test_equality_with_convert(self):
        from app.cash import Cash

        assert Cash("10", self._usd) == (Cash("10", self._usd) @ self._pln)

    def test_lt(self):
        from app.cash import Cash

        assert Cash("10", self._usd) < Cash("120", self._pln)
        assert Cash("10", self._usd) < Cash("11", self._usd)

    def test_gt(self):
        from app.cash import Cash

        assert Cash("10", self._usd) > Cash("20", self._pln)
        assert Cash("10", self._usd) > Cash("9.9999", self._usd)

    def test_arithmetic_negation(self):
        from app.cash import Cash

        cash = Cash("1", self._usd)

        assert -cash == operator.neg(cash) == Cash("-1", self._usd)

    def test_positive(self):
        from app.cash import Cash

        cash = Cash("1", self._usd)

        assert +cash == operator.pos(cash) == Cash("+1", self._usd)

    def test_abs(self):
        from app.cash import Cash

        cash_minus_5 = Cash("-5", self._usd)
        cash_plus_5 = Cash("5", self._usd)
        assert (
            abs(cash_minus_5)
            == operator.abs(cash_minus_5)
            == cash_plus_5
            == abs(cash_plus_5)
        )
