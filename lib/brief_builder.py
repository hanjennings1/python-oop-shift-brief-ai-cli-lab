class HandoffBriefBuilder:
    """Builds prompts and verifies output for shift handoff briefs."""

    REQUIRED_SECTIONS = (
        "Shift Summary:",
        "Open Issues:",
        "Action Items:",
        "Follow-Up Questions:",
        "Risk Notes:",
    )

    def _guidance(self):
        # Shared instructions used by both build_brief_prompt and build_revision_prompt
        sections = "\n".join(self.REQUIRED_SECTIONS)
        return (
            "Do not invent unsupported details. If information is missing, "
            "write \"Unknown\" for that detail.\n\n"
            "Respond using exactly these section labels:\n"
            f"{sections}\n"
        )

    def build_brief_prompt(self, notes):

        # Validate notes
        if not notes or not notes.strip():
            raise ValueError("Shift notes cannot be empty.")
        
        # Build and return a prompt for a new handoff brief
        return (
            "You are creating a shift handoff brief for a retail store.\n"
            "Use the shift notes below to produce a structured handoff brief.\n\n"
            f"Shift notes:\n{notes.strip()}\n\n"
            f"{self._guidance()}"
        )
    

    def build_revision_prompt(self, feedback):

        # Validate feedback
        if not feedback or not feedback.strip():
            raise ValueError("Revision feedback cannot be empty.")
        
        # Build and return a revision prompt
        return (
            "You are writing a revision of the previous shift handoff brief "
            "based on manager feedback.\n"
            "Use the earlier brief from the conversation history as context.\n\n"
            f"Revision feedback:\n{feedback.strip()}\n\n"
            f"{self._guidance()}"
        )


    def is_usable_brief(self, response_text):

        # Check whether response_text contains all required sections.
        if not response_text or not response_text.strip():
            return False
        return all(section in response_text for section in self.REQUIRED_SECTIONS)


    def format_brief(self, response_text, revised=False):
 
        # Choose the heading based on whether this is a new or revised brief
        if revised:
            heading = "Revised Shift Handoff Brief"
        else:
            heading = "Shift Handoff Brief"

        # Return a formatted created-brief string.
        return f"\n{heading}\n{response_text}"


    def create_brief(self, ai_client, notes):
 
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

        # Build the revision prompt
        prompt = self.build_revision_prompt(feedback)

        # Send the prompt through the AI client
        response = ai_client.send(prompt)

        # Verify the response structure
        if not self.is_usable_brief(response):
            raise RuntimeError("AI response did not include required sections.")
        # Return the formatted revised brief.
        return self.format_brief(response, revised=True)
