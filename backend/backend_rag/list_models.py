import httpx
from config.settings import settings

def main():
    api_key = settings.COHERE_API_KEY
    headers = {"Authorization": f"Bearer {api_key}"}

    r = httpx.get("https://api.cohere.com/v1/models", headers=headers, timeout=30)
    print("Status:", r.status_code)
    print(r.text)

if __name__ == "__main__":
    main()