class Choice:
    def __init__(self, choice: str, description: str, default: bool = False):
        """
        A menu choice to add to a prompt in interactive mode.

        :param choice: Letter to respond to
        :param description: Description of the choice
        :param default: If true, this will be the default choice for a the parent prompt.
        """
        self.choice = choice
        self.description = description
        self.default = default

    def show(self) -> str:
        """
        Show the choice to the user.

        :return: Choice info
        """
        output = f"'{self.choice}' - {self.description}"

        if self.default:
            output += " (default)"

        return output
