class HandoffBriefBuilder:
    """Builds prompts and verifies output for shift handoff briefs."""

    REQUIRED_SECTIONS = (
        "Shift Summary:",
        "Open Issues:",
        "Action Items:",
        "Follow-Up Questions:",
        "Risk Notes:",
    )

    def build_brief_prompt(self, notes):
        """
        Build a prompt for creating a new shift handoff brief.

        Requirements:
        - Reject None, empty, or whitespace-only notes with ValueError.
        - Include the original shift notes in the prompt.
        - Include every required section label from REQUIRED_SECTIONS.
        - Tell the model not to invent unsupported details.
        - Tell the model to use "Unknown" when details are not provided.
        - Keep this domain-specific prompt logic in this builder class,
          not in the reusable AI client.
        """
        # Validate notes
        if not notes or not notes.strip():
            raise ValueError("Shift notes cannot be empty.")
        
        # Build and return a prompt for a new handoff brief
        sections = "\n".join(self.REQUIRED_SECTIONS)

        return (
            "You are creating a shift handoff brief for a retail store.\n"
            "Use the shift notes below to produce a structured handoff brief.\n\n"
            f"Shift notes:\n{notes.strip()}\n\n"
            "Do not invent unsupported details. If information is missing, "
            "write \"Unknown\" for that detail.\n\n"
            "Respond using exactly these section labels:\n"
            f"{sections}\n"
        )
    

    def build_revision_prompt(self, feedback):
        """
        Build a prompt for revising the previous handoff brief.

        Requirements:
        - Reject None, empty, or whitespace-only feedback with ValueError.
        - Reference the previous brief or earlier conversation.
        - Include the manager's revision feedback.
        - Include every required section label from REQUIRED_SECTIONS.
        - Tell the model not to invent unsupported details.
        """
        # Validate feedback
        if not feedback or not feedback.strip():
            raise ValueError("Revision feedback cannot be empty.")
        
        # Build and return a revision prompt
        sections = "\n".join(self.REQUIRED_SECTIONS)

        return (
            "You are writing a revision of the previous shift handoff brief "
            "based on manager feedback.\n"
            "Use the earlier brief from the conversation history as context.\n\n"
            f"Revision feedback:\n{feedback.strip()}\n\n"
            "Do not invent unsupported details. If information is missing, "
            "write \"Unknown\" for that detail.\n\n"
            "Respond using exactly these section labels:\n"
            f"{sections}\n"
        )


    def is_usable_brief(self, response_text):
        """
        Check whether the AI response includes the required handoff structure.

        Requirements:
        - Return False for None, empty, or whitespace-only responses.
        - Return True only when the response contains every required section label.
        - Return False if one or more required sections are missing.
        """
        # Check whether response_text contains all required sections.
        if not response_text or not response_text.strip():
            return False
        return all(section in response_text for section in self.REQUIRED_SECTIONS)


    def format_brief(self, response_text, revised=False):
        """
        Format a created handoff brief for display.

        Requirements:
        - Return a string.
        - Add a clear user-facing heading before the response text.
        - Preserve the AI response content.
        """
        # Choose the heading based on whether this is a new or revised brief
        if revised:
            heading = "Revised Shift Handoff Brief"
        else:
            heading = "Shift Handoff Brief"

        # Return a formatted created-brief string.
        return f"\n{heading}\n{response_text}"


    def create_brief(self, ai_client, notes):
        """
        Create a new handoff brief.

        Requirements:
        - Build a prompt from the shift notes.
        - Send the prompt through ai_client.send().
        - Verify that the AI response includes the required sections.
        - Raise RuntimeError if the AI response is not usable.
        - Return a formatted user-facing brief.
        """
        # Build the prompt
        prompt = self.build_brief_prompt(notes)
        # Send the prompt through the AI client
        response = ai_client.send(prompt)
        # Verify the response structure
        if not self.is_usable_brief(response):
            raise RuntimeError("AI response did not include required sections.")
        # Return the formatted brief.
        return self.format_brief(response)


    def revise_brief(self, ai_client, feedback):
        """
        Revise the previous handoff brief.

        Requirements:
        - Build a revision prompt from the feedback.
        - Send the prompt through ai_client.send().
        - Verify that the AI response includes the required sections.
        - Raise RuntimeError if the AI response is not usable.
        - Return a formatted user-facing revised brief.
        """
        # Build the revision prompt
        prompt = self.build_revision_prompt(feedback)

        # Send the prompt through the AI client
        response = ai_client.send(prompt)

        # Verify the response structure
        if not self.is_usable_brief(response):
            raise RuntimeError("AI response did not include required sections.")
        # Return the formatted revised brief.
        return self.format_brief(response, revised=True)
