import openai

async def ai_generate_description(command_name: str):
    prompt = f"""
    Discord komutu için profesyonel, kısa, net bir açıklama oluştur:
    Komut adı: {command_name}
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"].strip()
    except:
        return "Açıklama yüklenemedi."
