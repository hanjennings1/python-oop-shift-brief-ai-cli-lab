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
            return "Input Error: Command cannot be empty."
        # Parse the command and payload
        stripped_input = raw_input.strip()
        parts = stripped_input.split(maxsplit=1)
        command = parts[0].lower()
        payload = parts[1].strip() if len(parts) > 1 else ""

        # Route supported commands.
        # Return helpful messages for errors and unknown commands.
        if command == "brief":
            if not payload:
                return "Input Error: Please provide shift notes to create a brief."
            try:
                return self.brief_builder.create_brief(self.ai_client, payload)
            except ValueError as error:
                return f"Input Error: {error}"
            except RuntimeError as error:
                return f"Service Error: {error}"

        if command == "revise":
            if not payload:
                return "Input Error: Please provide revision feedback."
            try:
                return self.brief_builder.revise_brief(self.ai_client, payload)
            except ValueError as error:
                return f"Input Error: {error}"
            except RuntimeError as error:
                return f"Service Error: {error}"

        if command in ("exit", "quit"):
            self.running = False
            return "Goodbye!"

        if command == "help":
            return self.command_help()

        if command == "history":
            return f"Conversation messages: {self.ai_client.message_count()}"

        if command == "reset":
            self.ai_client.reset()
            return "Conversation history reset."
        
        # Unknown command fallback
        return f"Input Error: Unknown command '{command}'. Type 'help' for a list of commands."


    def run(self):
        # Display welcome text
        self.display_welcome()
        # Run the input loop
        while self.running:
            try:
                raw_input = input("> ")
            except EOFError:
                break

            response = self.handle_command(raw_input)
            print(response)


def main():
    client = OllamaChatClient(model_name="llama3.2")
    app = ShiftBriefCLI(client)
    app.run()


if __name__ == "__main__":
    main()