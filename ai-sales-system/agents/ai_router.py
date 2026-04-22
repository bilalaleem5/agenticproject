"""
===============================================================
  AI SALES SYSTEM — AI Router
  Gemini / Grok / OpenRouter — auto-fallback
===============================================================
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests, json, time
from config import GEMINI_KEYS, GROK_KEYS, OPENROUTER_KEY, PRIMARY_AI, USE_MOCK_AI

_gemini_idx = 0
_grok_idx = 0


def _call_mock(prompt: str, system: str = "", temperature: float = 0.7) -> str:
    """Mock AI for verification without API keys."""
    p_lower = prompt.lower()
    if "decompose" in p_lower:
        return json.dumps({
            "product_task": "Generate a detailed product spec for a sales automation tool.",
            "engineer_task": "Create a high-converting HTML landing page.",
            "marketing_task": "Draft a cold email and Slack announcement."
        })
    if "verdict" in p_lower:
        return json.dumps({
            "verdict": "pass",
            "reason": "The output meets all criteria.",
            "revision_instruction": None,
            "ethics_score": 9,
            "ethics_justification": "Professional and transparent tone used."
        })
    if "product" in p_lower:
        return json.dumps({
            "value_proposition": "Automate your sales with AI.",
            "features": ["Lead Gen", "Cold Email", "Analytics"],
            "personas": ["Sales Manager", "Founder"]
        })
    if "marketing" in p_lower:
        return json.dumps({
            "tagline": "AI Sales OS - Your virtual SDR",
            "email_body": "Hi, I noticed your business could benefit from AI automation..."
        })
    
    return "Mock AI Response for: " + prompt[:50]


def _call_gemini(prompt: str, system: str = "", temperature: float = 0.7) -> str:
    global _gemini_idx
    models_to_try = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-pro"]
    
    for model_name in models_to_try:
        for attempt in range(len(GEMINI_KEYS)):
            key = GEMINI_KEYS[_gemini_idx % len(GEMINI_KEYS)]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={key}"
            body = {
                "contents": [{"role": "user", "parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": temperature, "maxOutputTokens": 2048},
            }
            if system:
                body["systemInstruction"] = {"parts": [{"text": system}]}
            try:
                r = requests.post(url, json=body, timeout=30)
                if r.status_code == 200:
                    data = r.json()
                    return data["candidates"][0]["content"]["parts"][0]["text"].strip()
                elif r.status_code == 429:
                    _gemini_idx += 1
                    time.sleep(5) # Longer wait for rate limit
                    continue
                else:
                    _gemini_idx += 1
                    continue
            except Exception:
                _gemini_idx += 1
                continue
    raise RuntimeError("All Gemini models/keys exhausted")


def _call_grok(prompt: str, system: str = "", temperature: float = 0.7) -> str:
    global _grok_idx
    for attempt in range(len(GROK_KEYS)):
        key = GROK_KEYS[_grok_idx % len(GROK_KEYS)]
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        body = {"model": "grok-3-mini", "messages": messages, "temperature": temperature, "max_tokens": 2048}
        try:
            r = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=body, timeout=30)
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"].strip()
            elif r.status_code == 429:
                _grok_idx += 1
                time.sleep(2)
                continue
            else:
                _grok_idx += 1
                continue
        except Exception:
            _grok_idx += 1
            continue
    raise RuntimeError("All Grok keys exhausted")


def _call_openrouter(prompt: str, system: str = "", temperature: float = 0.7) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://zetamize.com",
        "X-Title": "ZetaMize AI Sales System",
    }
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    # Using a reliable Llama model on OpenRouter
    body = {
        "model": "meta-llama/llama-3.3-70b-instruct",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 2048,
    }
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body, timeout=40)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        pass
    raise RuntimeError("OpenRouter failed")


def ai_call(prompt: str, system: str = "", temperature: float = 0.7, prefer: str = None) -> str:
    """
    Smart AI router — tries primary first, then falls back.
    prefer: 'gemini' | 'grok' | 'openrouter' (overrides config PRIMARY_AI)
    """
    if USE_MOCK_AI:
        return _call_mock(prompt, system, temperature)

    order = prefer or PRIMARY_AI
    if order == "gemini":
        chain = [_call_gemini, _call_grok, _call_openrouter]
    elif order == "grok":
        chain = [_call_grok, _call_gemini, _call_openrouter]
    else:
        chain = [_call_openrouter, _call_gemini, _call_grok]

    last_err = None
    for fn in chain:
        try:
            result = fn(prompt, system, temperature)
            if result:
                return result
        except Exception as e:
            last_err = e
            continue
    raise RuntimeError(f"All AI providers failed: {last_err}")


def ai_json(prompt: str, system: str = "", prefer: str = None) -> dict:
    """Call AI and parse JSON response."""
    system_with_json = (system + "\n\nIMPORTANT: Respond with ONLY valid JSON, no markdown, no explanation.").strip()
    raw = ai_call(prompt, system_with_json, temperature=0.3, prefer=prefer)
    # Strip markdown code blocks if present
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip().rstrip("```").strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # Try to extract JSON object
        start = raw.find('{')
        end = raw.rfind('}') + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
        raise ValueError(f"Could not parse JSON from AI response: {raw[:200]}")


if __name__ == "__main__":
    print("Testing AI Router...")
    result = ai_call("Say 'AI Sales System is ready!' in one line.")
    print(f"Response: {result}")
