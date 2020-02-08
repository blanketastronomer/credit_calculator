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


def test_calculate_annuity_principal(calculator):
    args = [
        '--type', 'annuity',
        '--payment', '8722',
        '--periods', '120',
        '--interest', '5.6'
    ]

    assert calculator.calculate(args) == "Your credit principal = 800019!\nOverpayment = 246621"


def test_calculate_annuity_timeframe_in_years(calculator):
    args = [
        '--type', 'annuity',
        '--principal', '500000',
        '--payment', '23000',
        '--interest', '7.8'
    ]

    assert calculator.calculate(args) == "You need 2 years to repay this credit!\nOverpayment = 52000"


def test_calculate_annuity_timeframe_in_months(calculator):
    args = [
        '--type', 'annuity',
        '--principal', '50000',
        '--payment', '22000',
        '--interest', '7.8'
    ]

    assert calculator.calculate(args) == "You need 3 months to repay this credit!\nOverpayment = 16000"


def test_calculate_annuity_timeframe_in_years_and_months(calculator):
    args = [
        '--type', 'annuity',
        '--principal', '500000',
        '--payment', '22000',
        '--interest', '7.8'
    ]

    assert calculator.calculate(args) == "You need 2 years and 1 month to repay this credit!\nOverpayment = 50000"
