from io import StringIO
import pytest
from credit_calculator.calculator import Calculator

@pytest.fixture()
def calculator():
    calculator = Calculator()

    yield calculator


def compatible_input(*inputs) -> StringIO:
    return StringIO("\n".join(inputs))


def test_interactive_calculate_annuity_timeframe_in_years(monkeypatch, calculator):
    current_input = compatible_input('a', 'n', '500000', '23000', '7.8')

    monkeypatch.setattr('sys.stdin', current_input)

    assert calculator.calculate([]) == "You need 2 years to repay this credit!\nOverpayment = 52000"


def test_interactive_calculate_annuity_timeframe_in_months(monkeypatch, calculator):
    current_input = compatible_input('a', 'n', '50000', '22000', '7.8')

    monkeypatch.setattr('sys.stdin', current_input)

    assert calculator.calculate([]) == "You need 3 months to repay this credit!\nOverpayment = 16000"


def test_interactive_annuity_timeframe_in_years_and_months(monkeypatch, calculator):
    current_input = compatible_input('a', 'n', '500000', '22000', '7.8')

    monkeypatch.setattr('sys.stdin', current_input)

    assert calculator.calculate([]) == "You need 2 years and 1 month to repay this credit!\nOverpayment = 50000"
