from ai_client import OllamaChatClient
from brief_builder import HandoffBriefBuilder


class ShiftBriefCLI:
    """Command-line workflow for generating and revising shift handoff briefs."""

    def __init__(self, ai_client, brief_builder=None):
        self.ai_client = ai_client
        self.brief_builder = brief_builder or HandoffBriefBuilder()
        self.running = True


    def display_welcome(self):
        # Print welcome text and command help.
        print("Shift Handoff Brief CLI")
        print("Create and revise AI-assisted shift handoff briefs.")
        print()
        print(self.command_help())


    def command_help(self):
        return (
            "Commands:\n"
            "- brief <shift notes>     Create a new handoff brief.\n"
            "- revise <feedback>       Revise the previous brief using feedback.\n"
            "- history                 Show the current conversation message count.\n"
            "- reset                   Clear conversation history.\n"
            "- help                    Show this command list.\n"
            "- exit or quit            Stop the program."
        )


    def handle_command(self, raw_input):
        # Validate raw_input
        if not raw_input or not raw_input.strip():
            return "Input Error: Command cannot be empty"
        # Parse the command and payload
        stripped_input = raw_input.strip()
        parts = stripped_input.split(maxsplit=1)
        command = parts[0].lower()
        payload = parts[1].strip() if len(parts) > 1 else ""
        # TODO: Route supported commands.
        # TODO: Return helpful messages for errors and unknown commands.
        pass

    def run(self):
        """
        Run the CLI input loop.

        Requirements:
        - Display the welcome message before the loop starts.
        - Continue while self.running is True.
        - Read user input.
        - Pass user input to handle_command().
        - Print returned messages.
        - Stop cleanly if EOFError occurs.
        """
        # TODO: Display welcome text.
        # TODO: Run the input loop.
        pass


def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()