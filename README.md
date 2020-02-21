# credit_calculator

My solution to the Jetbrains Academy "Credit Calculator" project.

## Getting started

### Prerequisites

* Python 3
* OSX or a Linux distro

NOTE: Due to the fact that Nox, which is used to test and lint this project, ONLY has PROVISIONAL support for Windows, this
project can ONLY be tested on a Non-Windows system.

### Installing

To get a development environment locally, do the following:

```shell script
# Clone the repo
git clone https://github.com/blanketastronomer/credit_calculator.git

# Switch to the project root
cd credit_calculator

# Checkout the "develop" branch, since that's where you'll be branching your
# changes off of
git checkout --track origin/develop

# Install all project requirements
pip install -r requirements.txt
```

At this point, to run any tests or linters, you can just use Nox by running:

```shell script
# Run this in the project root directory.
# It will test and lint the code as well as generate all necessary files for
# testing/deploying.
nox
```

### Running the tests

This project uses Nox for running tests.  There are two ways of using it:

1. Running `nox` in your terminal as stated in the previous section
2. Running `nox.sh` (yes, those two are different)

```shell script
# Run all tests/linters, reuse virtualenvs, and rebuild the Github Action
nox

# Run all tests/linters, rebuild virtualenvs, leave Github Action alone
./nox.sh
```

#### Running `nox`

Running `nox` in your terminal WILL (re)generate the Github Action the project uses.  It will also reuse any virtualenvs
created by Nox.  While this is fastest, it can lead to problems if you run it AFTER modifying `noxfile.py`.

#### Running `nox.sh`

Running `nox.sh` will run everything in `noxfile.py`, just like running `nox` in your terminal would do, except that it WILL
NOT (re)generate the Github Action, but WILL (re)generate the virtualenvs used by Nox.  While this method is the slowest, it's
also closest to how things are run via the Github Action when you push your branch.

### Usage

Usage is simple.  Right now, you can run the script from the current working directory, so long as you provide all necessary
parameters.  There are two (2) different ways to calculate your loan parameters:

* Annuity - Where all payments made over the lifetime of the loan are exactly the same
* Differentiated - Where all payments made over the lifetime of the loan are different

NOTE: You will need to know the interest rate of the loan in ALL cases.  Failure to provide the loan's interest rate will
result in an error.  This calculator CANNOT calculate the interest rate of your loan.

#### Annuity

First we'll cover annuity payments, since that's the most common way people will use this application.  For annuity-based
calculations, three (3) different values may be calculated:

* The payment amount
* The loan principal
* The timeframe in months and/or years when the loan will be paid off

##### Example: Calculating the payment amount

Calculating the payment amount where the principal is $1,000,000 with a 10% interest rate and you want to pay off the loan in 5
years (60 months):

```shell script
python credit_calc.py --type annuity --principal 1000000 --periods 60 --interest 10
```

Your result will be:

```text
Your annuity payment = 21248!
Overpayment = 274880
```

---

##### Example: Calculating the loan principal

Calculating your loan principal where your monthly payment is $8,722, you want to pay off the loan in 10 years (120 months),
and you're paying 5.6% interest:

```shell script
python credit_calc.py --type annuity --payment 8722 --periods 120 --interest 5.6
```

Your result will be:

```text
Your credit principal = 800019!
Overpayment = 246621
```

---

##### Example: Calculating the time it will take to pay off the loan

Calculating the time it'll take for you to pay off a $500,000 loan at 7.8% interest with a $22,000 payment:

```shell script
python credit_calc.py --type annuity --principal 500000 --payment 22000 --interest 7.8
```

Your result will be:

```text
You need 2 years and 1 month to repay this credit!
Overpayment = 50000
```

#### Differentiated

Next we'll cover "differentiated" payments.  For differentiated payment calculations, each payment will be a different amount,
so they'll be displayed in an amortization schedule.

NOTE: You MUST provide the principal amount, timeframe in months, and interest rate of the loan in order to use this method!

##### Example: Calculating your monthly payments

Calculating your monthly payments on a $1,000,000 loan with a 10% interest rate that you want to pay off in 10 months:

```shell script
python credit_calc.py --type diff --principal 1000000 --periods 10 --interest 10
```

Your result will be:

```text
Month 1: paid out 108334
Month 2: paid out 107500
Month 3: paid out 106667
Month 4: paid out 105834
Month 5: paid out 105000
Month 6: paid out 104167
Month 7: paid out 103334
Month 8: paid out 102500
Month 9: paid out 101667
Month 10: paid out 100834

Overpayment = 45837
```

## Built with

* [flake8](https://gitlab.com/pycqa/flake8)
* [pytest](https://github.com/pytest-dev/pytest)
* [nox](https://github.com/theacodes/nox)

## Contributing

TODO: Write contributing guidelines.

## Authors

* **Nicholas S.** - *Initial work* - [BlanketAstronomer](https://github.com/BlanketAstronomer)

## License

This project is licensed under the MIT License - See the [LICENSE.md](LICENSE.md) file for details.
