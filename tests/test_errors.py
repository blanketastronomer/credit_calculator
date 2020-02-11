import pytest

from credit_calculator.calculator import Calculator


@pytest.fixture()
def calculator():
    calculator = Calculator()

    yield calculator


def error_matches(result):
    assert result == "Incorrect parameters"


def switch_argument_sign(arguments: list, index: int):
    """
    Switch the sign of a passed argument
    :param arguments: List of arguments
    :param argument: Argument to switch sign of.  Starts at 1
    :return:
    """

    float_value = 0
    int_value = 0

    try:
        float_value = float(arguments[index]) * -1
        int_value = int(arguments[index]) * -1

        if int_value == float_value:
            arguments[index] = str(int_value)
    except ValueError:
        arguments[index] = str(float_value)

    # else:
    #     arguments[index] = float(float_value)


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


def test_some_arguments_cannot_be_negative():
    args = [
        '--type', 'annuity',
        '--principal', '30000',
        '--periods', '14',
        '--interest', '10.2'
    ]

    for i in [3, 5, 7]:
        calculator = Calculator()
        switch_argument_sign(args, i)
        error_matches(calculator.calculate(args))
        switch_argument_sign(args, i)


def test_cannot_calculate_interest(calculator):
    args = [
        '--type', 'annuity',
        '--principal', '100000',
        '--payment', '10400',
        '--periods', '10'
    ]

    error_matches(calculator.calculate(args))


def test_conflicting_options(calculator):
    args = [
        '--type', 'diff',
        '--principal', '1000000',
        '--interest', '10',
        '--payment', '100000'
    ]

    error_matches(calculator.calculate(args))


def test_all_options_specified_are_conflicting(calculator):
    args = [
        '--type', 'annuity',
        '--principal', '1000000',
        '--periods', '10',
        '--interest', '10',
        '--payment', '2500'
    ]

    error_matches(calculator.calculate(args))
