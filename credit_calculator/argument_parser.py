import argparse


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def add_argument(self, *name_or_flags: str, **kwargs):
        self.parser.add_argument(*name_or_flags, **kwargs)

    def parse_args(self, args):
        self.parser.add_argument('--type', choices=['annuity', 'diff'], help='Annuity')
        self.parser.add_argument('--principal', type=int, help='Loan principal')
        self.parser.add_argument('--periods', type=int, help='Pay periods, usually the term of the loan in months.')
        self.parser.add_argument('--interest', type=float, help='Interest rate given as a percentage.')
        self.parser.add_argument('--payment', type=int, help='Payment amount')

        return self.parser.parse_args(args)
