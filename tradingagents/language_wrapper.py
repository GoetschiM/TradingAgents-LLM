class LanguageWrapper:
    """Wrap an LLM to enforce responses in a specified language."""

    def __init__(self, llm, language="en"):
        self.llm = llm
        self.language = language

    def _prepend_language(self, messages):
        system_prompt = {"role": "system", "content": f"Respond in {self.language}."}
        if isinstance(messages, list):
            return [system_prompt] + messages
        else:  # assume string or message object
            return [system_prompt, {"role": "user", "content": messages}]

    def invoke(self, messages, **kwargs):
        return self.llm.invoke(self._prepend_language(messages), **kwargs)

    def bind_tools(self, *args, **kwargs):
        bound = self.llm.bind_tools(*args, **kwargs)
        return LanguageWrapper(bound, self.language)

    def __getattr__(self, attr):
        return getattr(self.llm, attr)
