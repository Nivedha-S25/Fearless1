import requests

def analyze_soft_skills(text, model="mistral"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": f"Analyze this interview answer for tone, clarity, and confidence: {text}",
            "stream": False
        }
    )
    result = response.json()
    return result.get("response", "No response from model.")
