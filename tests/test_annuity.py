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


def test_calculate_annuity_payment(calculator):
    args = [
        '--type', 'annuity',
        '--principal', '1000000',
        '--periods', '60',
        '--interest', '10'
    ]

    assert calculator.calculate(args) == "Your annuity payment = 21248!\nOverpayment = 274880"
