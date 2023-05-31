# Currency Exchange Library
 
The task verifies the candidates' knowledge of pure `Python`.
 
## Introduction
 
You are creating a `Python` library that provides the following classes: `Cash` and `Currency`.
The classes allow you to represent the instances of money with currency exchange.
The `Cash` class supports most of the logical operators and some of the mathematical operators.
 
## Task Details
 
1. Please do NOT modify any tests unless specifically told to do so.
2. Make the tests pass by implementing the missing features in the production code.
3. There are multiple tests placed in the project that will help you verify your solution. Please use them as a guideline when developing the project. Keep in mind that only a subset of the tests is visible to you and that your solution will be tested against many edge cases.
4. Type annotations can help you occasionally.
5. The currency rates are fixed (`rates.py` file). Please do not modify them.
6. Amounts are quantized to precision of 4 decimal places.
 
### Part 1 - Currency enum
Please implement the following class method: `Currency.is_member`,
which checks if the given value (currency code) belongs to the enum.
 
### Part 2 - Exchange rates quotation
Please fill in the `ExchangeRateService.quotation` method body ([app/exchange_rate.py](app/exchange_rate.py)).
It should return a currency pair’s exchange rate.
The currency pair's exchange rate reflects how much of the quote currency is needed
to be sold/bought to buy/sell one unit of the base currency.
 
The quotation EUR/USD 1.2500 means that one euro is exchanged for 1.2500 US dollars.
This means that 1 euro can be exchanged for 1.25 US dollars.
 
The result decimal has a default precision of 28 places.
 
```python
# Rates:
# PLN = 1.0
# USD = 4.55
 
assert quotation(Currency.PLN, Currency.EUR) == decimal.Decimal("0.2197802197802197802197802198")
```
 
If a currency or an exchange rate is invalid it should raise a `QuotationError`.
 
### Part 3 - Cash class - currency conversion ([app/cash.py](app/cash.py))
 
1. Please implement the `Cash.to` method with one positional argument `target_currency` of the following type: `Currency`
that will convert/exchange the current instance to another currency.
If the `target_currency` is the same currency or `None` it should not change the instance.
You should use the `ExchangeRateService.quotation` from part 2 to calculate the new amount.
 
2. Implement a functionality that will allow you to use the `@` operator for currency conversion.
It should behave like the `Cash.to` method.
For example:
```python
in_pln = Cash("1337", Currency.EUR) @ Currency.PLN
```
 
If a rate is missing an `ExchangeRateUnknownError` should be raised.
 
### Part 4 -  TargetCurrency context manager
 
Fill in the class `TargetCurrency` ([app/cash.py](app/cash.py))
to behave like a context manager that will allow you to change the result/target of the `Cash` objects operations (addition, subtraction, multiplication).
 
To get it done, you should probably modify the `Cash` class but be careful and do not spoil other tasks.
 
Example usage:
```python
value = None
with TargetCurrency(Currency.EUR):
   value = Cash("10", Currency.PLN) + Cash("12", Currency.PLN)
 
assert value.currency == Currency.EUR
assert value.amount > 22
```
 
### Part 5 - Subtracting Cash instances
 
Please fill in the `Cash` class with methods that will allow you to subtract the `Cash` instances, decimals and integers.
Examples:
 
```python
assert Cash("100", Currency.PLN) - Cash("25", Currency.USD) == Cash("4.9400", Currency.PLN)
assert Cash("100", Currency.USD) - 15 == Cash("85", Currency.USD)
```
 
## Hints
 
To execute unit tests, use:
 
```
pip install -q -e . && python3 setup.py test
```
