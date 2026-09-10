import ollama


class OllamaChatClient:
    """Generic reusable client for interacting with a local chat model service."""

    def __init__(self, model_name="llama3.2"):
        """
        Initialize the client.
        Requirements:
        - Store the model name.
        - Create an empty list for conversation history.
        - Each client instance should have its own history list.
        """
        self.model_name = model_name
        self.history = []


    def send(self, prompt):
        """
        Send a prompt to the AI service and return the assistant response text.

        Requirements:
        - Reject None, empty, or whitespace-only prompts with ValueError.
        - Strip the prompt before saving it.
        - Add a user message to self.history before calling the service.
        - Call ollama.chat(model=self.model_name, messages=self.history).
        - Extract usable assistant response content.
        - Support both dictionary-style and object-style response shapes.
        - Reject missing, non-string, or blank assistant content.
        - Add the assistant response to self.history only after a usable response.
        - Return the assistant response text.
        - If the service call or response extraction fails:
            - remove the failed user message,
            - preserve previous valid history,
            - raise RuntimeError with a clear service-error message.
        """
        # Validate the prompt
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        # Create and append the user message
        user_message = {"role": "user", "content": prompt.strip()}
        self.history.append(user_message)

        # Call the AI service and validate its response
        try:
            response = ollama.chat(model=self.model_name, messages=self.history)

            # Extract assistant content, supporting both dict-style and object-style responses
            try:
                content = response["message"]["content"]
            except (TypeError, KeyError):
                content = getattr(response, "message", None)
                content = getattr(content, "content", None)

            # Reject missing, non-string, or blank content
            if not isinstance(content, str) or not content.strip():
                raise RuntimeError("unusable response")

        except Exception:
            # Roll back the failed user message and surface a clear service error
            self.history.remove(user_message)
            raise RuntimeError("AI service request failed.")

        # Append the assistant response only after a successful, usable response
        assistant_message = {"role": "assistant", "content": content}
        self.history.append(assistant_message)

        # Return the assistant response text
        return content


    def reset(self):
        """
        Clear the conversation history.

        Requirements:
        - After this method runs, self.history should be an empty list.
        """
        # Clear conversation history.
        self.history = []


    def message_count(self):
        """
        Return the number of messages currently stored in conversation history.

        Requirements:
        - Return an integer.
        - Count both user messages and assistant messages.
        """
        # Return the number of stored messages.
        return len(self.history)

    def get_transcript(self):
        """
        Return a safe copy of the conversation history.

        Requirements:
        - Return a list with the same message dictionaries.
        - Do not return the internal self.history list directly.
        - The returned message dictionaries should also be copies.
        """
        # Return a copy of the transcript.
        return [message.copy() for message in self.history]