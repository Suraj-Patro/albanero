import decimal

from app.currency import Currency

RATES = {
    Currency.PLN: decimal.Decimal("1.0000"),  # Base currency
    Currency.CZK: decimal.Decimal("5.7034"),
    Currency.DKK: decimal.Decimal("0.6152"),
    Currency.EUR: decimal.Decimal("4.5500"),
    Currency.GBP: decimal.Decimal("5.2500"),
    Currency.NOK: decimal.Decimal("0.4511"),
    Currency.USD: decimal.Decimal("3.8024"),
    Currency.ZAR: None,
}
