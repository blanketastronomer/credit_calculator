import argparse


class ArgumentParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def add_argument(self, *name_or_flags: str, **kwargs):
        self.parser.add_argument(*name_or_flags, **kwargs)

    def parse_args(self, args):
        self.parser.add_argument('--type', choices=['annuity'], help='Annuity or differentiate')

        return self.parser.parse_args(args)
