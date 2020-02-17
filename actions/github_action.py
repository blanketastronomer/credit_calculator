from pathlib import Path

import oyaml as yaml
from pyparsing import unicode


class LiteralUnicode(unicode):
    pass


def literal_unicode_represnter(dumper, data):
    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')


yaml.add_representer(LiteralUnicode, literal_unicode_represnter)


class GithubAction:
    def __init__(self, name: str):
        """
        Creates a new Github Action.
        :param name: Name of the action.  Will be displayed in the action file.
        """
        self.name = name
        self.action_data = {
            'name': self.name,
            'on': '[push]',
            'jobs': {
                'build': {
                    'runs-on': 'ubuntu-latest',
                    'steps': [
                        {
                            'uses': 'actions/checkout@v2'
                        },
                        {
                            'name': 'Set up Python 3.8',
                            'uses': 'actions/setup-python@v1',
                            'with': {
                                'python-version': 3.8
                            }
                        }
                    ]
                }
            }
        }

    def add_step(self, name: str, *commands: str) -> None:
        """
        Add a step to the action.

        :param name: Step name
        :param commands: Commands to execute
        """
        steps = self.action_data['jobs']['build']['steps']

        data = {}
        data['name'] = name

        if commands != ():
            data['run'] = LiteralUnicode(*commands)

        steps.append(
            data
        )

    def save(self, path: Path) -> None:
        """
        Save the action to the given path.

        :param path: Path to save the action
        """
        with open(path, 'w') as file:
            yaml.dump(self.action_data, file)

        data = path.read_text()
        new_data = data.replace("'on': '[push]'", "on: [push]")
        path.write_text(new_data)

        data = path.read_text()
        new_data = data.replace('flake8 credit_calculator', 'flake8 .')
        path.write_text(new_data)
