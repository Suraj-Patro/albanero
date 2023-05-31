import decimal

import typing

from app.currency import Currency
from app.exchange_rate import exchange_rate_service
from app.exceptions import ExchangeRateUnknownError, InvalidCurrencyError

CashOrNumber = typing.Union[int, decimal.Decimal, "Cash"]


class Cash:
    __slots__ = "_amount", "_currency"

    def __init__(
        self, amount: typing.Union[str, decimal.Decimal], currency: Currency
    ) -> None:
        if not isinstance(currency, Currency) or not Currency.is_member(currency.value):
            raise InvalidCurrencyError

        self._amount = decimal.Decimal(amount)
        self._currency = currency

    @property
    def amount(self) -> decimal.Decimal:
        return self._amount.quantize(decimal.Decimal("0.0000"))

    @property
    def currency(self) -> Currency:
        return self._currency

    def __repr__(self) -> str:
        return f"{self.amount} {self.currency.name}"

    def __lt__(self, other: CashOrNumber) -> bool:
        amount = self._get_amount(other)
        return self.amount < amount

    def __le__(self, other: CashOrNumber) -> bool:
        amount = self._get_amount(other)
        return self.amount <= amount

    def __gt__(self, other: CashOrNumber) -> bool:
        amount = self._get_amount(other)
        return self.amount > amount

    def __ge__(self, other: CashOrNumber) -> bool:
        amount = self._get_amount(other)
        return self.amount >= amount

    def __eq__(self, other: CashOrNumber) -> bool:
        amount = self._get_amount(other)
        return self.amount == amount

    def __ne__(self, other: CashOrNumber) -> bool:
        return not self == other

    def __bool__(self):
        return bool(self._amount)

    def __add__(self, other: CashOrNumber) -> "Cash":
        amount = self.amount + self._get_amount(other)

        if TargetCurrency.currency:
            return Cash(amount, self.currency).to(TargetCurrency.currency)

        return Cash(amount, self.currency)

    def __radd__(self, other: CashOrNumber) -> "Cash":
        return self.__add__(other)

    def __sub__(self, other: CashOrNumber) -> "Cash":
        amount = self.amount - self._get_amount(other)

        if TargetCurrency.currency:
            return Cash(amount, self.currency).to(TargetCurrency.currency)

        return Cash(amount, self.currency)

    def __mul__(self, other: CashOrNumber) -> "Cash":
        amount = self.amount * self._get_amount(other)

        if TargetCurrency.currency:
            return Cash(amount, self.currency).to(TargetCurrency.currency)

        return Cash(amount, self.currency)

    def __neg__(self) -> "Cash":
        if TargetCurrency.currency:
            return Cash(-self._amount, self.currency).to(TargetCurrency.currency)

        return Cash(-self._amount, self.currency)

    def __pos__(self) -> "Cash":
        if TargetCurrency.currency:
            return Cash(+self._amount, self.currency).to(TargetCurrency.currency)

        return Cash(+self._amount, self.currency)

    def __abs__(self) -> "Cash":
        if TargetCurrency.currency:
            return Cash(abs(self._amount), self.currency).to(TargetCurrency.currency)

        return Cash(abs(self._amount), self.currency)

    def __matmul__(self, target_currency: Currency) -> "Cash":
        return self.to(target_currency)

    def to(self, target_currency: Currency) -> "Cash":
        """TODO: Part 3"""
        if self.currency != target_currency and target_currency is not None:
            try:
                return Cash(self.amount * exchange_rate_service.quotation(self.currency, target_currency), target_currency)
            except:
                raise ExchangeRateUnknownError
        else:
            # return Cash( self.amount, self.currency)
            return self

        # amount = self.amount
        # if self.currency != target_currency or target_currency is not None:
        #     amount = amount * exchange_rate_service.quotation(self.currency, target_currency)
        # return Cash( amount, target_currency)

    def _get_amount(self, other: CashOrNumber) -> decimal.Decimal:
        if isinstance(other, Cash):
            other = other.to(self.currency)
            return other.amount
        return other


class TargetCurrency:
    """TODO: Part 4"""
    currency = None

    def __init__(self, *args, **kwargs):
        TargetCurrency.currency = args[0]

    def __enter__(self, *args, **kwargs):
        pass

    def __exit__(self, *args, **kwargs):
        TargetCurrency.currency = None
