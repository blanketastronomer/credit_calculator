from pathlib import Path

import nox

PROJECt_DIR: Path = Path(__file__).parent
DOCS_DIR: Path = PROJECt_DIR / 'docs'

nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session):
    session.install('flake8')
    session.run('flake8', 'credit_calculator', '--count', '--select=E9,F63,F7,F82', '--show-source', '--statistics')
    session.run('flake8', 'credit_calculator', '--count', '--exit-zero', '--max-complexity=10', '--max-line-length=127',
                '--statistics')


@nox.session
def test(session):
    session.install('pytest')
    session.run('pytest')


@nox.session
def docs(session):
    session.install('Sphinx')
    # session.install('sphinx-apidoc')
    if DOCS_DIR.exists():
        print("docs/ exists!")
    else:
        print("docs/ does not exist.  Creating...")
        session.run(
            'sphinx-quickstart', 'docs',
            '--sep',
            '--project', '"Credit Calculator"',
            '--author', 'BlanketAstronomer',
            '--language', 'en',
            '--release', '1.0.0',
            '--ext-autodoc',
            '--ext-intersphinx',
            '--ext-viewcode',
            '--makefile',
            '--batchfile'
        )

    session.run('cd', 'docs', external=True)
    session.run('sphinx-apidoc', '-o', 'docs/source/', '../credit_calculator')
    session.run('make', '-C', 'docs', 'html', external=True)
    session.run('pwd', external=True)
