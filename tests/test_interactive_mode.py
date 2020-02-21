from io import StringIO
import pytest
from credit_calculator.calculator import Calculator
from tests.helpers.file_helper import text_from_file


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


def test_interative_annuity_payment(monkeypatch, calculator):
    current_input = compatible_input('a', 'a', '1000000', '60', '10')

    monkeypatch.setattr('sys.stdin', current_input)

    assert calculator.calculate([]) == "Your annuity payment = 21248!\nOverpayment = 274880"


def test_interactive_annuity_principal(monkeypatch, calculator):
    current_input = compatible_input('a', 'p', '8722', '120', '5.6')

    monkeypatch.setattr('sys.stdin', current_input)

    assert calculator.calculate([]) == "Your credit principal = 800019!\nOverpayment = 246621"


def test_interactive_differentiate_payments(monkeypatch, calculator):
    current_input = compatible_input('d', '1000000', '10', '10')

    monkeypatch.setattr('sys.stdin', current_input)

    expected_text = text_from_file('diff_example_1.txt', True)
    actual_text = calculator.calculate([])

    assert actual_text == expected_text
