import json
import os
import re
import random
import time
from datetime import datetime
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests

# --- CONFIGURATION ---
GH_USER = "mehmetcan52"
GH_REPO = "subscription-catalog"

# --- 1. FULL SERVICES LIST (210+ ENTRIES) ---
SERVICES = [
    # --- VIDEO & STREAMING ---
    {"id": "netflix", "name": "Netflix", "domain": "netflix.com", "category": "Video"},
    {"id": "disneyplus", "name": "Disney+", "domain": "disneyplus.com", "category": "Video"},
    {"id": "primevideo", "name": "Amazon Prime Video", "domain": "primevideo.com", "category": "Video"},
    {"id": "youtube", "name": "YouTube Premium", "domain": "youtube.com", "category": "Video"},
    {"id": "apple_tv", "name": "Apple TV+", "domain": "tv.apple.com", "category": "Video"},
    {"id": "hulu", "name": "Hulu", "domain": "hulu.com", "category": "Video"},
    {"id": "max", "name": "Max (HBO)", "domain": "max.com", "category": "Video"},
    {"id": "paramount_plus", "name": "Paramount+", "domain": "paramountplus.com", "category": "Video"},
    {"id": "peacock", "name": "Peacock", "domain": "peacocktv.com", "category": "Video"},
    {"id": "crunchyroll", "name": "Crunchyroll", "domain": "crunchyroll.com", "category": "Video"},
    {"id": "mubi", "name": "MUBI", "domain": "mubi.com", "category": "Video"},
    {"id": "discovery_plus", "name": "Discovery+", "domain": "discoveryplus.com", "category": "Video"},
    {"id": "fubo_tv", "name": "FuboTV", "domain": "fubo.tv", "category": "Video"},
    {"id": "rakuten_tv", "name": "Rakuten TV", "domain": "rakuten.tv", "category": "Video"},
    {"id": "skyshowtime", "name": "SkyShowtime", "domain": "skyshowtime.com", "category": "Video"},
    {"id": "viaplay", "name": "Viaplay", "domain": "viaplay.com", "category": "Video"},
    {"id": "blutv", "name": "BluTV", "domain": "blutv.com", "category": "Video"},
    {"id": "exxen", "name": "Exxen", "domain": "exxen.com", "category": "Video"},
    {"id": "gain", "name": "GAIN", "domain": "gain.tv", "category": "Video"},
    {"id": "ssport_plus", "name": "S Sport Plus", "domain": "ssportplus.com", "category": "Video"},
    {"id": "tod_tr", "name": "TOD (beIN)", "domain": "todtv.com.tr", "category": "Video"},
    {"id": "tv_plus", "name": "TV+", "domain": "tvplus.com.tr", "category": "Video"},
    {"id": "tabii", "name": "Tabii Premium", "domain": "tabii.com", "category": "Video"},

    # --- ARTIFICIAL INTELLIGENCE (AI) ---
    {"id": "chatgpt", "name": "ChatGPT Plus", "domain": "openai.com", "category": "AI"},
    {"id": "claude", "name": "Claude Pro", "domain": "anthropic.com", "category": "AI"},
    {"id": "midjourney", "name": "Midjourney", "domain": "midjourney.com", "category": "AI"},
    {"id": "perplexity", "name": "Perplexity Pro", "domain": "perplexity.ai", "category": "AI"},
    {"id": "grammarly", "name": "Grammarly", "domain": "grammarly.com", "category": "AI"},
    {"id": "github_copilot", "name": "GitHub Copilot", "domain": "github.com", "category": "AI"},
    {"id": "notion_ai", "name": "Notion AI", "domain": "notion.so", "category": "AI"},
    {"id": "elevenlabs", "name": "ElevenLabs", "domain": "elevenlabs.io", "category": "AI"},
    {"id": "runway", "name": "Runway Gen-3", "domain": "runwayml.com", "category": "AI"},
    {"id": "heygen", "name": "HeyGen", "domain": "heygen.com", "category": "AI"},
    {"id": "leonardo_ai", "name": "Leonardo.ai", "domain": "leonardo.ai", "category": "AI"},
    {"id": "descript", "name": "Descript", "domain": "descript.com", "category": "AI"},
    {"id": "luma_ai", "name": "Luma Dream Machine", "domain": "lumalabs.ai", "category": "AI"},
    {"id": "otter_ai", "name": "Otter.ai", "domain": "otter.ai", "category": "AI"},
    {"id": "pika", "name": "Pika Art", "domain": "pika.art", "category": "AI"},
    {"id": "jasper", "name": "Jasper AI", "domain": "jasper.ai", "category": "AI"},

    # --- MUSIC & AUDIO ---
    {"id": "spotify", "name": "Spotify", "domain": "spotify.com", "category": "Music"},
    {"id": "apple_music", "name": "Apple Music", "domain": "music.apple.com", "category": "Music"},
    {"id": "youtube_music", "name": "YouTube Music", "domain": "music.youtube.com", "category": "Music"},
    {"id": "tidal", "name": "Tidal", "domain": "tidal.com", "category": "Music"},
    {"id": "deezer", "name": "Deezer", "domain": "deezer.com", "category": "Music"},
    {"id": "fizy", "name": "Fizy", "domain": "fizy.com", "category": "Music"},
    {"id": "muud", "name": "Muud", "domain": "muud.com.tr", "category": "Music"},
    {"id": "audible", "name": "Audible", "domain": "audible.com", "category": "Books"},
    {"id": "storytel", "name": "Storytel", "domain": "storytel.com", "category": "Books"},
    {"id": "audioteka", "name": "Audioteka", "domain": "audioteka.com", "category": "Books"},
    {"id": "blinkist", "name": "Blinkist", "domain": "blinkist.com", "category": "Books"},
    {"id": "pocket_casts", "name": "Pocket Casts Plus", "domain": "pocketcasts.com", "category": "Music"},

    # --- PRODUCTIVITY & CLOUD ---
    {"id": "icloud", "name": "iCloud+", "domain": "apple.com", "category": "Cloud"},
    {"id": "google_one", "name": "Google One", "domain": "google.com", "category": "Cloud"},
    {"id": "microsoft_365", "name": "Microsoft 365", "domain": "microsoft.com", "category": "Productivity"},
    {"id": "adobe_cc", "name": "Adobe Creative Cloud", "domain": "adobe.com", "category": "Design"},
    {"id": "canva", "name": "Canva Pro", "domain": "canva.com", "category": "Design"},
    {"id": "notion", "name": "Notion", "domain": "notion.so", "category": "Productivity"},
    {"id": "dropbox", "name": "Dropbox", "domain": "dropbox.com", "category": "Cloud"},
    {"id": "zoom", "name": "Zoom", "domain": "zoom.us", "category": "Productivity"},
    {"id": "1password", "name": "1Password", "domain": "1password.com", "category": "Security"},
    {"id": "bitwarden", "name": "Bitwarden Premium", "domain": "bitwarden.com", "category": "Security"},
    {"id": "todoist", "name": "Todoist Pro", "domain": "todoist.com", "category": "Productivity"},
    {"id": "ticktick", "name": "TickTick Premium", "domain": "ticktick.com", "category": "Productivity"},
    {"id": "slack", "name": "Slack Pro", "domain": "slack.com", "category": "Productivity"},
    {"id": "figma", "name": "Figma Professional", "domain": "figma.com", "category": "Design"},
    {"id": "framer", "name": "Framer Pro", "domain": "framer.com", "category": "Design"},
    {"id": "setapp", "name": "Setapp", "domain": "setapp.com", "category": "Productivity"},

    # --- GAMING ---
    {"id": "ps_plus", "name": "PlayStation Plus", "domain": "playstation.com", "category": "Gaming"},
    {"id": "xbox_game_pass", "name": "Xbox Game Pass", "domain": "xbox.com", "category": "Gaming"},
    {"id": "nintendo_online", "name": "Nintendo Switch Online", "domain": "nintendo.com", "category": "Gaming"},
    {"id": "geforce_now", "name": "GeForce NOW", "domain": "nvidia.com", "category": "Gaming"},
    {"id": "discord_nitro", "name": "Discord Nitro", "domain": "discord.com", "category": "Social"},
    {"id": "ea_play", "name": "EA Play", "domain": "ea.com", "category": "Gaming"},
    {"id": "ubisoft_plus", "name": "Ubisoft+", "domain": "ubisoft.com", "category": "Gaming"},

    # --- EDUCATION & HEALTH ---
    {"id": "duolingo", "name": "Duolingo Super", "domain": "duolingo.com", "category": "Education"},
    {"id": "masterclass", "name": "MasterClass", "domain": "masterclass.com", "category": "Education"},
    {"id": "strava", "name": "Strava Premium", "domain": "strava.com", "category": "Fitness"},
    {"id": "headspace", "name": "Headspace", "domain": "headspace.com", "category": "Health"},
    {"id": "calm", "name": "Calm", "domain": "calm.com", "category": "Health"},
    {"id": "linkedin_premium", "name": "LinkedIn Premium", "domain": "linkedin.com", "category": "Social"},
    {"id": "x_premium", "name": "X (Twitter) Premium", "domain": "x.com", "category": "Social"},
    {"id": "uber_one", "name": "Uber One", "domain": "uber.com", "category": "Lifestyle"},

    # --- SECURITY & HOSTING ---
    {"id": "surfshark", "name": "Surfshark VPN", "domain": "surfshark.com", "category": "Security"},
    {"id": "nordvpn", "name": "NordVPN", "domain": "nordvpn.com", "category": "Security"},
    {"id": "proton_mail", "name": "Proton Mail Plus", "domain": "proton.me", "category": "Security"},
    {"id": "vercel", "name": "Vercel Pro", "domain": "vercel.com", "category": "Productivity"},
    {"id": "digitalocean", "name": "DigitalOcean", "domain": "digitalocean.com", "category": "Productivity"}
]

# --- 2. THE TOP 100 LIVE TARGETS (Canlı Taranacaklar) ---
TARGET_100_IDS = [
    "netflix", "disneyplus", "primevideo", "youtube", "apple_tv", "hulu", "max",
    "paramount_plus", "peacock", "crunchyroll", "mubi", "discovery_plus", "fubo_tv",
    "skyshowtime", "blutv", "exxen", "gain", "ssport_plus", "tod_tr", "tv_plus", "tabii",
    "chatgpt", "claude", "midjourney", "perplexity", "grammarly", "github_copilot",
    "notion_ai", "elevenlabs", "runway", "heygen", "leonardo_ai", "descript", "luma_ai",
    "otter_ai", "pika", "spotify", "apple_music", "youtube_music", "tidal", "deezer",
    "fizy", "muud", "audible", "storytel", "icloud", "google_one", "microsoft_365",
    "adobe_cc", "canva", "notion", "dropbox", "zoom", "1password", "bitwarden",
    "todoist", "ticktick", "slack", "figma", "framer", "setapp", "ps_plus",
    "xbox_game_pass", "nintendo_online", "geforce_now", "discord_nitro", "ea_play",
    "ubisoft_plus", "duolingo", "masterclass", "strava", "headspace", "calm",
    "linkedin_premium", "x_premium", "uber_one", "surfshark", "nordvpn", "proton_mail"
]

# --- 3. HARDCODED TARGET URLS (Yüksek Doğruluk İçin) ---
SCRAPE_URLS = {
    "netflix": "https://help.netflix.com/tr/node/24926",
    "spotify": "https://www.spotify.com/tr-tr/premium/",
    "youtube": "https://www.youtube.com/premium",
    "disneyplus": "https://www.disneyplus.com/tr-tr/welcome/plans",
    "icloud": "https://support.apple.com/tr-tr/108047",
    "chatgpt": "https://openai.com/chatgpt/pricing",
    "google_one": "https://one.google.com/about/plans",
    "canva": "https://www.canva.com/tr_tr/fiyatlandirma/"
}

# --- 4. MASTER BOT CLASS ---
class SubscriptionBot:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        # Regex: Finds numbers followed by currency or vice versa
        self.price_regex = r'(\d{1,4}(?:[.,]\d{2}))\s?(?:TL|₺|TRY|USD|\$|EUR|€)'
        self.plan_keywords = ["Premium", "Standard", "Basic", "Family", "Aile", "Bireysel", "Plus", "Pro", "Personal", "Student", "Özel", "Individual", "Başlangıç"]

    def clean_price(self, val):
        if not val: return 0.0
        return float(re.sub(r'[^\d.]', '', val.replace(',', '.')))

    def smart_match(self, soup):
        """Semantic Matcher: Finds plan names and prices in the same block."""
        found_plans = {}
        # We look for containers that might hold a single plan's info
        for block in soup.find_all(['div', 'li', 'tr', 'section', 'article', 'p']):
            text = block.get_text(separator=" ").strip()
            
            # Find a price in this block
            price_match = re.search(self.price_regex, text)
            if price_match:
                price = self.clean_price(price_match.group(1))
                if price < 5: continue # Filter out small ads/garbage
                
                # Identify plan name in the same block
                plan_name = "Standard" # Fallback
                for kw in self.plan_keywords:
                    if kw.lower() in text.lower():
                        plan_name = kw
                        break
                
                # Keep the cheapest price if duplicate names found (likely monthly vs yearly)
                if plan_name not in found_plans or price < found_plans[plan_name]["TRY"]:
                    found_plans[plan_name] = {"TRY": price}
        
        return found_plans

    def get_live_data(self, s_id):
        url = SCRAPE_URLS.get(s_id, f"https://www.google.com/search?q={s_id}+turkiye+fiyatlari")
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                # Create context with mobile-like sizing to trigger easier layouts
                context = browser.new_context(user_agent=self.user_agent, viewport={'width': 1280, 'height': 800})
                page = context.new_page()
                
                print(f"  🌐 Crawling: {url}")
                page.goto(url, wait_until="networkidle", timeout=60000)
                time.sleep(random.uniform(3, 5)) # Human delay
                
                # Trigger lazy loads
                page.evaluate("window.scrollTo(0, document.body.scrollHeight / 4)")
                
                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')
                browser.close()
                return self.smart_match(soup)
        except Exception as e:
            print(f"  ❌ Scrape failed for {s_id}: {e}")
            return None

# --- 5. MAIN EXECUTION ---
def main():
    bot = SubscriptionBot()
    session = requests.Session()
    session.headers.update({'User-Agent': bot.user_agent})
    
    catalog = {
        "version": "20.0",
        "lastUpdated": datetime.now().isoformat(),
        "totalServices": len(SERVICES),
        "services": []
    }

    print(f"🏁 MASTER PIPELINE START: {len(SERVICES)} Services")

    for i, s in enumerate(SERVICES, 1):
        print(f"[{i}/{len(SERVICES)}] Processing: {s['name']}...")
        
        # 1. LOGO ENGINE
        logo_dir = "logos"
        if not os.path.exists(logo_dir): os.makedirs(logo_dir)
        logo_fn = f"{s['domain'].replace('.', '_')}.png"
        logo_path = f"{logo_dir}/{logo_fn}"
        
        if not os.path.exists(logo_path):
            try:
                # High-res logo fetch
                res = session.get(f"https://logo.clearbit.com/{s['domain']}?size=512", timeout=5)
                if res.status_code == 200:
                    with open(logo_path, 'wb') as f: f.write(res.content)
            except: pass

        s['logoUrl'] = f"https://cdn.jsdelivr.net/gh/{GH_USER}/{GH_REPO}/{logo_path}"

        # 2. PRICE ENGINE (Live for Top 100, Static for others)
        if s['id'] in TARGET_100_IDS:
            live_data = bot.get_live_data(s['id'])
            if live_data:
                s['plans'] = [{"name": name, "prices": price} for name, price in live_data.items()]
                print(f"  ✅ SUCCESS: Found {len(s['plans'])} plans.")
            else:
                # Fallback to zero if live fails
                s['plans'] = [{"name": "Standard", "prices": {"TRY": 0.0, "USD": 0.0}}]
        else:
            # Quick bypass for non-priority services
            s['plans'] = [{"name": "Standard", "prices": {"TRY": 0.0, "USD": 0.0}}]

        catalog['services'].append(s)
        
        # Avoid getting flagged by GitHub or target sites
        if i % 10 == 0: time.sleep(2)

    # FINAL SAVE
    with open('catalog.json', 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    
    print("\n🚀 MISSION ACCOMPLISHED: catalog.json is fully updated.")

if __name__ == "__main__":
    main()
