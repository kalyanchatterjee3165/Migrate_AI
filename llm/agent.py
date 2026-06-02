import json
from openai import OpenAI

import config.settings as settings
from .prompts import SYSTEM_PROMPT
from .tool_registry import ToolRegistry


class MigrationAgent:
    """
    Conversational agent that drives the migration workflow.

    - Maintains full conversation history per session
    - Passes tools from ToolRegistry to the OpenAI API
    - Detects tool_calls in responses and dispatches to registered handlers
    - Returns plain-text responses back to the Gradio UI
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.model = settings.LLM_MODEL
        client_kwargs = {"api_key": settings.LLM_API_KEY}
        if settings.LLM_BASE_URL:
            client_kwargs["base_url"] = settings.LLM_BASE_URL
        self.client = OpenAI(**client_kwargs)
        self.history: list[dict] = []   # full conversation history

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def chat(self, user_message: str) -> str:
        """
        Accept a user message, run the agent loop, return the assistant reply.
        This is the method Gradio calls on every user turn.
        """
        self.history.append({"role": "user", "content": user_message})
        reply = self._run_agent_loop()
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def reset(self):
        """Clear conversation history (called when user starts a new migration)."""
        self.history = []

    # ------------------------------------------------------------------
    # Core agent loop
    # ------------------------------------------------------------------

    def _run_agent_loop(self) -> str:
        """
        Single turn of the agent loop.

        1. Call the LLM with current history + tool definitions
        2. If finish_reason == 'tool_calls' → execute each tool,
           append results, call LLM again for a natural-language reply
        3. If finish_reason == 'stop' → return plain text directly
        """
        tools = self.registry.get_openai_tools()
        messages = self._build_messages()

        response = self.client.chat.completions.create(
            model=self.model,
            tools=tools,
            tool_choice="auto",
            messages=messages,
        )

        message = response.choices[0].message

        # ── Case 1: LLM wants to call one or more tools ───────────────
        if message.tool_calls:
            return self._handle_tool_calls(message, tools)

        # ── Case 2: Plain conversational reply ────────────────────────
        return message.content or "(No response)"

    # ------------------------------------------------------------------
    # Tool execution
    # ------------------------------------------------------------------

    def _handle_tool_calls(self, assistant_message, tools: list[dict]) -> str:
        """
        Execute every tool call the LLM requested, collect results,
        then send them back for a final natural-language summary.
        """
        # 1. Append the assistant's message (with tool_calls) to history
        self.history.append(assistant_message)

        # 2. Execute each tool call and append its result
        for tool_call in assistant_message.tool_calls:
            tool_name  = tool_call.function.name
            tool_input = json.loads(tool_call.function.arguments)

            print(f"\n[tool_call] >>> {tool_name}")
            print(f"[tool_call]     args: {json.dumps(tool_input, indent=2)}")

            tool_result = self._execute_tool(tool_name, tool_input)

            print(f"[tool_call] <<< {tool_name} → status={tool_result.get('status')}")
            if tool_result.get("status") == "error":
                print(f"[tool_call]     error: {tool_result.get('error_message')}")

            self.history.append({
                "role":         "tool",
                "tool_call_id": tool_call.id,
                "name":         tool_name,
                "content":      json.dumps(tool_result),
            })

        # 3. Call LLM again so it can summarize the results in plain English
        final_response = self.client.chat.completions.create(
            model=self.model,
            tools=tools,
            tool_choice="auto",
            messages=self._build_messages(),
        )

        final_message = final_response.choices[0].message
        reply = final_message.content or "(No response)"

        # 4. Keep history clean — replace the raw assistant_message object
        #    with the plain text reply we'll show the user
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def _execute_tool(self, tool_name: str, tool_input: dict) -> dict:
        """
        Look up the handler in the registry and call it.
        Returns a result dict that goes back to the LLM as a tool message.
        """
        try:
            handler = self.registry.get_handler(tool_name)
            result  = handler(**tool_input)
            return {"status": "success", **result}
        except Exception as e:
            return {"status": "error", "error_message": str(e)}

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _build_messages(self) -> list[dict]:
        """
        Prepend the system prompt to the current conversation history.
        OpenAI expects system message as the first entry in messages[].
        """
        return [{"role": "system", "content": SYSTEM_PROMPT}] + self.history