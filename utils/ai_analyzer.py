import openai

async def analyze_message(content: str):
    prompt = f"""
Aşağıdaki mesajı analiz et.

Mesaj: "{content}"

Şu formatta JSON döndür:

{{
  "toxicity": 0-100 arası sayı,
  "category": "kufur / hakaret / spam / tehdit / taciz / reklam / nefret / normal",
  "score": -1 (negatif) veya 0 (nötr) veya +1 (pozitif)
}}
"""

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        import json
        return json.loads(response.choices[0].message["content"])
    except:
        # Her ihtimale karşı fallback
        return {"toxicity": 0, "category": "normal", "score": 0}
