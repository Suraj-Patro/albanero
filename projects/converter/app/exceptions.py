class CurrencyExchangeError(Exception):
    pass


class InvalidCurrencyError(CurrencyExchangeError):
    pass


class ExchangeRateUnknownError(CurrencyExchangeError):
    pass


class QuotationError(CurrencyExchangeError):
    pass
