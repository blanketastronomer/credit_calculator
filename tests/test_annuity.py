import pytest

from credit_calculator.calculator import Calculator


@pytest.fixture()
def calculator():
    calculator = Calculator()

    yield calculator


def test_annuity(calculator):
    args = [
        '--type', 'annuity'
    ]

    calculator.calculate(args)

    assert calculator.arguments.type == 'annuity'
