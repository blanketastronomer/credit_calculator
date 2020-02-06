from typing import List

from credit_calculator.argument_parser import ArgumentParser


class Calculator(object):
    def __init__(self):
        """
        Calculator for various loan parameters given other known values.
        """
        self.argument_parser = ArgumentParser()
        self.arguments = None

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
        else:
            pass
