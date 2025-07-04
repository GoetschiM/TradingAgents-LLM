from pathlib import Path
from typing import Any, Dict
import yaml

from tradingagents.llm_factory_v1_0_009 import create_llm

COST_RATES = {"gemini": 0.000019}


class LLMVerifierNode:
    """Verify signals using a local LLM with optional cloud fallback."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.cost_log = {"local_tok": 0, "cloud_tok": 0, "$": 0.0}

    def _count_tokens(self, resp) -> int:
        usage = resp.response_metadata.get("token_usage") if hasattr(resp, "response_metadata") else {}
        return usage.get("total_tokens", 0)

    def __call__(self, prompt: str) -> Dict[str, Any]:
        cfg = self.config.copy()
        profile = cfg.get("llm_profile", "local_phi3")
        llm = create_llm(cfg, quick=True)
        resp = llm.invoke(prompt)
        confidence = resp.response_metadata.get("confidence", 1.0) if hasattr(resp, "response_metadata") else 1.0
        tokens = self._count_tokens(resp)
        result = {
            "response": resp.content,
            "confidence": confidence,
            "cost_estimate_usd": 0.0,
        }
        if profile == "local_phi3":
            self.cost_log["local_tok"] += tokens
        else:
            self.cost_log["cloud_tok"] += tokens
            if cfg["llm_provider"] == "gemini":
                cost = tokens * COST_RATES["gemini"]
                self.cost_log["$"] += cost
                result["cost_estimate_usd"] = cost

        if profile == "local_phi3" and confidence < 0.8 and cfg.get("fallback_to_cloud"):
            profiles = yaml.safe_load((Path(__file__).resolve().parents[1] / "configs" / "llm_profiles.yaml").read_text())
            cloud_cfg = cfg.copy()
            cloud_cfg.update(profiles["cloud_gemini_flash"])
            cloud_cfg["llm_profile"] = "cloud_gemini_flash"
            llm2 = create_llm(cloud_cfg, quick=True)
            resp2 = llm2.invoke(prompt)
            conf2 = resp2.response_metadata.get("confidence", 1.0) if hasattr(resp2, "response_metadata") else 1.0
            tokens2 = self._count_tokens(resp2)
            cost = tokens2 * COST_RATES["gemini"]
            self.cost_log["cloud_tok"] += tokens2
            self.cost_log["$"] += cost
            result.update({"response": resp2.content, "confidence": conf2, "cost_estimate_usd": cost})
        return result
