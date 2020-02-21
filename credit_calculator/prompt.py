from credit_calculator.choice import Choice


class Prompt:
    def __init__(self, text: str, *choices: Choice):
        """
        Interactive prompt that allows user interaction.

        :param text: Prompt text to display
        :param choices: Choices for the user to pick from
        """
        self.text = text
        self.choices = choices
        self.accepted_values = set()
        self.default_choice: Choice = None
        self.choice: Choice = None

    def _build_prompt(self) -> str:
        """
        Build the prompt to display to the user.

        :return: Prompt text
        """
        if self.choices is ():
            return f"{self.text}: "
        else:
            output = f"{self.text}\n"
            choice_list = []
            for choice in self.choices:
                choice_list.append(choice.show())
                self.accepted_values.add(choice.choice)

                if choice.default is True:
                    self.default_choice = choice

            choice_text = "\n".join(choice_list)
            output += f"{choice_text}: \n> "

            return output

    def prompt(self) -> str:
        """
        Display a prompt and return the user's input as a string.

        :return: User's choice as a string if choices were provided to the instance, else the user's input
        """
        user_input = input(self._build_prompt()).lower()

        if user_input == '' and self.default_choice is not None:
            return self.default_choice.choice
        else:
            self.choice = user_input
            return user_input

    def int_prompt(self) -> int:
        """
        Display a prompt and return the user's input as an integer.

        :return: User input as an integer
        """
        try:
            return int(self.prompt())
        except ValueError:
            return 0

    def float_prompt(self) -> float:
        """
        Display a prompt and return the user's input as a float.

        :return: User input as a float.
        """
        try:
            return float(self.prompt())
        except ValueError:
            return 0
