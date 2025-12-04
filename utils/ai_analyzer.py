import openai

async def analyze_message(content: str):
    prompt = f"""
Mesajı kategorize et:
Pozitif → +1
Negatif → -1
Nötr → 0

Mesaj: "{content}"
Sadece sayı döndür. (+1, 0, -1)
"""

    response = openai.ChatCompletion.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        return int(response.choices[0].message["content"].strip())
    except:
        return 0
