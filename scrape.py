import requests
from bs4 import BeautifulSoup

urls = {
    "instagram_community": "https://help.instagram.com/477434105621119",
    "instagram_copyright": "https://help.instagram.com/126382350847838",
    "tiktok_community": "https://www.tiktok.com/community-guidelines/en/",
    "tiktok_copyright": "https://www.tiktok.com/legal/page/global/copyright-policy/en",
}

for name, url in urls.items():
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        with open(f"data/{name}.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print(f"{name} kaydedildi ✓")
    except Exception as e:
        print(f"{name} hata: {e}")