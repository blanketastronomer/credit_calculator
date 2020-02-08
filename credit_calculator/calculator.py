from math import ceil
from math import log
from math import pow
from typing import List

from credit_calculator.argument_parser import ArgumentParser
from credit_calculator.helpers.value_helper import value_missing


class Calculator(object):
    def __init__(self):
        """
        Calculator for various loan parameters given other known values.
        """
        self.argument_parser = ArgumentParser()
        self.arguments = None

    def _interest_rate(self, rate: float) -> float:
        """
        Private function to turn a percentage into a float.

        :param rate: Rate to convert
        :return: Converted interest rate
        """
        return (rate / 12) / 100

    def calculate(self, args: List[str]) -> str:
        """
        Calculate a missing parameter for a loan given the other parameters and their values.

        :param args: Arguments to calculate missing values.
        :type args: List[str]
        :return: String with the calculated missing value or an error message.
        """
        if args:
            # Commandline arguments have been passed.
            self.arguments = self.argument_parser.parse_args(args)
            calculation_type = self.arguments.type
            principal = self.arguments.principal
            interest = self.arguments.interest
            pay_periods = self.arguments.periods
            payment = self.arguments.payment

            if value_missing(interest):
                pass
            else:
                if value_missing(pay_periods):
                    return self.annuity_timeframe(principal, payment, interest)
                else:
                    if value_missing(principal):
                        return self.annuity_principal(payment, pay_periods, interest)
                    else:
                        return self.annuity_payment(principal, pay_periods, interest)
        else:
            pass

    def annuity_payment(self, principal: int, timeframe: int, interest_rate: float):
        """
        Calculate the current payment as an annuity.

        This means it'll be a single number with an overpayment amount if the debt will be paid off with a positive
        balance.

        :param principal: Loan principal
        :param timeframe: Pay periods, usually the amount of time to pay the loan off in months
        :param interest_rate: Interest rate specified as a percentage, e.g. 12% is 12, 0.9% is 0.9
        :return: String showing the payment and overpayment, if overpaid
        """
        i = self._interest_rate(interest_rate)
        power = pow(1 + i, timeframe)
        numerator = i * power
        denominator = power - 1
        payment = ceil(principal * (numerator / denominator))
        overpayment = (payment * timeframe) - principal
        output = f"Your annuity payment = {payment}!"

        if overpayment > 0:
            output += f"\nOverpayment = {overpayment}"

        return output

    def annuity_principal(self, payment: int, timeframe: int, interest_rate: float) -> str:
        """
        Calculate the principal on an annuity-style payment loan with overpayment amount if overpaid.

        :param payment: Single, annuity payment (since it won't change)
        :param timeframe: Pay periods, usually the amount of time to pay the loan off in months
        :param interest_rate: Interest rate specified as a percentage, e.g. 12% is 12, 0.9% is 0.9
        :return: String showing the principal and overpayment, if overpaid
        """
        i = self._interest_rate(interest_rate)
        power = pow(1 + i, timeframe)
        numerator = i * power
        denominator = power - 1
        principal = round(payment / (numerator / denominator))
        overpayment = (payment * timeframe) - principal

        output = f"Your credit principal = {principal}!"

        if overpayment > 0:
            output += f"\nOverpayment = {overpayment}"

        return output

    def annuity_timeframe(self, principal: int, payment: int, interest_rate: float):
        """
        Calculate the amount of time that it will take to pay off the loan, with overpayment.

        :param principal: Loan principal
        :param payment: Single, annuity payment (since it won't change)
        :param interest_rate: Interest rate specified as a percentage, e.g. 12% is 12, 0.9% is 0.9
        :return: String showing timeframe in months and years as well as any overpayment if overpaid
        """
        interest = self._interest_rate(interest_rate)
        inner_function = payment / (payment - interest * principal)
        pay_periods = ceil(log(inner_function, 1 + interest))

        years, months = divmod(pay_periods, 12)
        overpayment = (payment * pay_periods) - principal

        def pluralize(singular: str, plural: str, number: int):
            if abs(number) == 1:
                return singular
            else:
                return plural

        output = "You need "
        year_string = pluralize('year', 'years', years)
        month_string = pluralize('month', 'months', months)

        if years > 0:
            output += f"{years} {year_string} "

        if months > 0 and years > 0:
            output += "and "

        if months > 0:
            output += f"{months} {month_string} "

        output += "to repay this credit!"

        if overpayment > 0:
            output += f"\nOverpayment = {overpayment}"

        return output
