from math import ceil
from math import log
from math import pow
from typing import List

from credit_calculator.argument_parser import ArgumentParser
from credit_calculator.choice import Choice
from credit_calculator.errors.missing_parameter_error import MissingParameterError
from credit_calculator.errors.negative_parameter_error import NegativeValueError
from credit_calculator.errors.too_many_values_error import TooManyValuesError
from credit_calculator.errors.value_missing_error import ValueMissingError
from credit_calculator.helpers.value_helper import value_missing
from credit_calculator.prompt import Prompt

ERR_INCORRECT_PARAMETERS = "Incorrect parameters"


class Calculator(object):
    def __init__(self):
        """
        Calculator for various loan parameters given other known values.
        """
        self.argument_parser = ArgumentParser()
        self.arguments = None
        self.calc_prompt: Prompt = None

        # Needed ONLY for interactive mode.
        self.principal_prompt: Prompt = None
        self.payment_prompt: Prompt = None
        self.timeframe_prompt: Prompt = None
        self.interest_prompt: Prompt = None

    def _interest_rate(self, rate: float) -> float:
        """
        Private function to turn a percentage into a float.

        :param rate: Rate to convert
        :return: Converted interest rate
        """
        return (rate / 12) / 100

    def _check_arguments(self, args: List[str]) -> list:
        """
        Check if arguments are valid.

        :param args: List of arguments to check.
        :return: List of arguments
        """
        self.arguments = self.argument_parser.parse_args(args)
        calculation_type = self.arguments.type
        principal = self.arguments.principal
        interest = self.arguments.interest
        pay_periods = self.arguments.periods
        payment = self.arguments.payment
        argc = 0

        string_arguments = [calculation_type]
        numeric_arguments = [principal, interest, pay_periods, payment]
        all_arguments = string_arguments + numeric_arguments

        # One value MUST be missing to calculate anything
        existing_values = set()

        for arg in all_arguments:
            missing = value_missing(arg)

            if not missing:
                argc += 1

            existing_values.add(missing)

        if existing_values == {False}:
            raise TooManyValuesError

        if argc < 4:
            raise ValueMissingError

        # Check if numeric arguments are negative
        for arg in numeric_arguments:
            if not value_missing(arg) and arg < 0:
                raise NegativeValueError

        if value_missing(calculation_type) or value_missing(interest):
            raise MissingParameterError

        return [calculation_type, principal, interest, pay_periods, payment]

    def calculate(self, args: List[str]) -> str:
        """
        Calculate a missing parameter for a loan given the other parameters and their values.

        :param args: Arguments to calculate missing values.
        :type args: List[str]
        :return: String with the calculated missing value or an error message.
        """
        if args:
            try:
                calculation_type, principal, interest, pay_periods, payment = self._check_arguments(args)

                if calculation_type == 'annuity':
                    if value_missing(pay_periods):
                        return self.annuity_timeframe(principal, payment, interest)
                    else:
                        if value_missing(principal):
                            return self.annuity_principal(payment, pay_periods, interest)
                        else:
                            return self.annuity_payment(principal, pay_periods, interest)
                elif calculation_type == 'diff':
                    if not value_missing(principal) and not value_missing(pay_periods):
                        return self.differentiate_payment(principal, pay_periods, interest)
                    else:
                        raise ValueMissingError
            except (MissingParameterError, NegativeValueError, ValueMissingError, TooManyValuesError):
                return ERR_INCORRECT_PARAMETERS
        else:
            return self.interactive_mode()

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

    def differentiate_payment(self, principal: int, timeframe: int, interest_rate: float) -> str:
        """
        Calculate all future loan payments.

        In a differentiate payment structure, each pay period has a different payment amount.

        An overpayment amount will also be included if the loan will be overpaid.

        :param principal: Loan principal
        :param timeframe: Pay periods, usually the amount of time to pay the loan off in months
        :param interest_rate: Interest rate specified as a percentage, e.g. 12% is 12, 0.9% is 0.9
        :return: String showing the payments and overpayment, if overpaid
        """
        m = 1
        balance = principal
        paid = 0
        output = ""

        while balance > 0:
            interest = self._interest_rate(interest_rate)
            formula = (principal / timeframe) + interest * (principal - (principal * (m - 1) / timeframe))

            payment = ceil(formula)
            output += f"Month {m}: paid out {payment}\n"
            balance -= payment
            paid += payment
            m += 1

        overpayment = paid - principal

        if overpayment > 0:
            output += f"\nOverpayment = {overpayment}"

        return output

    def interactive_mode(self):
        parser_type = Prompt(
            "Which type of debt would you like to calculate?",
            Choice('a', 'Annuity'),
            Choice('d', 'Differentiate')
        ).prompt()

        self.load_interactive_prompts()

        if parser_type == 'a':
            calc_prompt = self.calc_prompt.prompt()

            if calc_prompt == 'n':
                principal = self.principal_prompt.int_prompt()
                payment = self.payment_prompt.int_prompt()
                interest = self.interest_prompt.float_prompt()

                return self.annuity_timeframe(principal, payment, interest)
            elif calc_prompt == 'a':
                principal = self.principal_prompt.int_prompt()
                timeframe = self.payment_prompt.int_prompt()
                interest = self.interest_prompt.float_prompt()

                return self.annuity_payment(principal, timeframe, interest)
            elif calc_prompt == 'p':
                payment = self.payment_prompt.int_prompt()
                timeframe = self.timeframe_prompt.int_prompt()
                interest = self.interest_prompt.float_prompt()

                return self.annuity_principal(payment, timeframe, interest)
        elif parser_type == 'd':
            principal = self.principal_prompt.int_prompt()
            timeframe = self.timeframe_prompt.int_prompt()
            interest = self.interest_prompt.float_prompt()

            return self.differentiate_payment(principal, timeframe, interest)

        return parser_type

    def load_interactive_prompts(self):
        self.calc_prompt = Prompt(
            "What do you want to calculate?",
            Choice('n', 'Timeframe to payoff'),
            Choice('a', 'Monthly payment'),
            Choice('p', 'Credit principal')
        )

        self.principal_prompt = Prompt("Please enter the credit principal")
        self.payment_prompt = Prompt("Please enter the monthly payment")
        self.timeframe_prompt = Prompt("Please enter the number of pay cycles")
        self.interest_prompt = Prompt("Please enter the credit interest rate")
