import pytest

from credit_calculator.calculator import Calculator
from tests.helpers.file_helper import text_from_file


@pytest.fixture()
def calculator():
    calculator = Calculator()

    yield calculator


def test_differentiate_option(calculator):
    args = [
        '--type', 'diff'
    ]

    calculator.calculate(args)

    assert calculator.arguments.type == 'diff'


def test_interactive_differentiate(calculator):
    args = [
        '--type', 'diff',
        '--principal', '1000000',
        '--periods', '10',
        '--interest', '10'
    ]

    expected_text = text_from_file('diff_example_1.txt', True)
    actual_text = calculator.calculate(args)

    assert actual_text == expected_text


def test_differentiate_again(calculator):
    args = [
        '--type', 'diff',
        '--principal', '500000',
        '--periods', '8',
        '--interest', '7.8'
    ]

    expected_text = text_from_file('diff_example_2.txt', True)
    actual_text = calculator.calculate(args)

    assert actual_text == expected_text
