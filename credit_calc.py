import sys

from credit_calculator.calculator import Calculator

if __name__ == '__main__':
    calc = Calculator()
    output = calc.calculate(sys.argv[1:])

    print(output)
