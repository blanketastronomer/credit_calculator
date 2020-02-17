# credit_calculator

My solution to the Jetbrains Academy "Credit Calculator" project.

# Configuring

This project uses Nox to lint the project, run all tests, and (re)generate pythonapp.yml when adding new Nox sessions.

There are two (2) ways of running Nox for this project:

## Running nox.sh

Running nox.sh runs everything in `noxfile.py` as it'll run on Github.  That means that the Github workflow won't be
(re)generated but the virtualenvs used by Nox will be.  This method is also the slowest.

## Running `nox` in your terminal

Running `nox` in your terminal WILL (re)generate the Github action, and it'll reuse the virtualenvs that Nox uses.  This is
the fastest method.

If you made modifications to `noxfile.py`, you'll have to run Nox this way BEFORE committing or else you'll run into errors on
Github.
