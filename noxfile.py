import os
import sys
from pathlib import Path

import nox

try:
    from actions.github_action import GithubAction
except ModuleNotFoundError:
    sys.path.insert(0, os.path.abspath('.'))
    from actions.github_action import GithubAction

nox.options.reuse_existing_virtualenvs = True

PROJECT_DIR: Path = Path(__file__).parent
WORKFLOW_DIR = PROJECT_DIR / '.github' / 'workflows'
NOX_WORKFLOW = WORKFLOW_DIR / 'pythonapp.yml'


ga = GithubAction('Python application')
ga.add_step(
    'Install dependencies',
    u'python -m pip install --upgrade pip\npip install -r requirements.txt\n'
)


def run_and_save(name: str, commands, session):
    for command in commands:
        if not command.startswith('pip install'):
            c = command.rstrip().split(' ')
            session.run(*c)

    interactive_session = session.interactive

    if interactive_session:
        joined = ''.join(commands)
        ga.add_step(
            name,
            joined
        )
        ga.save(NOX_WORKFLOW)


@nox.session()
def lint(session):
    commands = [
        u'pip install flake8\n',
        # Stop the build if there are Python syntax errors or undefined names
        'flake8 credit_calculator --count --select=E9,F63,F7,F82 --show-source --statistics\n',
        # Exit-zero treats all errors as warnings.  The Github editor is 127 chars wide
        'flake8 credit_calculator --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics\n'
    ]

    session.install('flake8')

    run_and_save('Lint with flake8', commands, session)


@nox.session()
def test(session):
    commands = [
        'pip install pytest\n',
        'pytest\n'
    ]

    session.install('pytest')

    run_and_save('Test with pytest', commands, session)
