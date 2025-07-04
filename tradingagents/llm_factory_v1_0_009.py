import os
from .language_wrapper import LanguageWrapper


def create_llm(cfg, *, quick=False):
    provider = cfg["llm_provider"]
    model = cfg["quick_think_llm"] if quick else cfg["deep_think_llm"]
    if provider == "ollama":
        from langchain_community.chat_models import ChatOllama
        llm = ChatOllama(model=model, base_url=cfg["backend_url"])
        return LanguageWrapper(llm, cfg.get("language", "en"))
    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            convert_system_message_to_human=True,
        )
        return LanguageWrapper(llm, cfg.get("language", "en"))
    # default: openai
    from langchain_openai import ChatOpenAI
    llm = ChatOpenAI(model=model, base_url=cfg["backend_url"])
    return LanguageWrapper(llm, cfg.get("language", "en"))
