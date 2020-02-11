import pytest

from credit_calculator.calculator import Calculator


@pytest.fixture()
def calculator():
    calculator = Calculator()

    yield calculator


def error_matches(result):
    assert result == "Incorrect parameters"


def test_type_not_specified(calculator):
    args = [
        '--principal', '1000000',
        '--periods', '60',
        '--interest', '10'
    ]

    error_matches(calculator.calculate(args))


def test_less_than_four_arguments(calculator):
    args = [
        '--type', 'diff',
        '--principal', '1000000',
        '--interest', '10'
    ]

    error_matches(calculator.calculate(args))
