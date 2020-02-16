from pathlib import Path

import nox

nox.options.reuse_existing_virtualenvs = True

PROJECT_DIR: Path = Path(__file__).parent


@nox.session()
def lint(session):
    session.install('flake8')
    session.run('flake8', 'credit_calculator', '--count', '--select=E9,F63,F7,F82', '--show-source', '--statistics')
    session.run('flake8', 'credit_calculator', '--count', '--exit-zero', '--max-complexity=10', '--max-line-length=127',
                '--statistics')


@nox.session()
def test(session):
    session.install('pytest')
    session.run('pytest')
