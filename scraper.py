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

# --- FULL COMPREHENSIVE SERVICE LIST (210+ ENTRIES) ---
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
    {"id": "lastpass", "name": "LastPass", "domain": "lastpass.com", "category": "Security"},
    {"id": "dashlane", "name": "Dashlane", "domain": "dashlane.com", "category": "Security"},
    {"id": "bitwarden", "name": "Bitwarden Premium", "domain": "bitwarden.com", "category": "Security"},
    {"id": "todoist", "name": "Todoist Pro", "domain": "todoist.com", "category": "Productivity"},
    {"id": "ticktick", "name": "TickTick Premium", "domain": "ticktick.com", "category": "Productivity"},
    {"id": "monday", "name": "Monday.com", "domain": "monday.com", "category": "Productivity"},
    {"id": "slack", "name": "Slack Pro", "domain": "slack.com", "category": "Productivity"},
    {"id": "evernote", "name": "Evernote", "domain": "evernote.com", "category": "Productivity"},
    {"id": "obsidian", "name": "Obsidian Sync", "domain": "obsidian.md", "category": "Productivity"},
    {"id": "loom", "name": "Loom Pro", "domain": "loom.com", "category": "Productivity"},
    {"id": "figma", "name": "Figma Professional", "domain": "figma.com", "category": "Design"},
    {"id": "framer", "name": "Framer Pro", "domain": "framer.com", "category": "Design"},
    {"id": "sketch", "name": "Sketch", "domain": "sketch.com", "category": "Design"},
    {"id": "craft_docs", "name": "Craft Docs", "domain": "craft.do", "category": "Productivity"},
    {"id": "superhuman", "name": "Superhuman", "domain": "superhuman.com", "category": "Productivity"},
    {"id": "raycast", "name": "Raycast Pro", "domain": "raycast.com", "category": "Productivity"},
    {"id": "setapp", "name": "Setapp", "domain": "setapp.com", "category": "Productivity"},

    # --- GAMING ---
    {"id": "ps_plus", "name": "PlayStation Plus", "domain": "playstation.com", "category": "Gaming"},
    {"id": "xbox_game_pass", "name": "Xbox Game Pass", "domain": "xbox.com", "category": "Gaming"},
    {"id": "nintendo_online", "name": "Nintendo Switch Online", "domain": "nintendo.com", "category": "Gaming"},
    {"id": "apple_arcade", "name": "Apple Arcade", "domain": "apple.com", "category": "Gaming"},
    {"id": "geforce_now", "name": "GeForce NOW", "domain": "nvidia.com", "category": "Gaming"},
    {"id": "discord_nitro", "name": "Discord Nitro", "domain": "discord.com", "category": "Social"},
    {"id": "twitch_turbo", "name": "Twitch Turbo", "domain": "twitch.tv", "category": "Gaming"},
    {"id": "ea_play", "name": "EA Play", "domain": "ea.com", "category": "Gaming"},
    {"id": "ubisoft_plus", "name": "Ubisoft+", "domain": "ubisoft.com", "category": "Gaming"},
    {"id": "wow_sub", "name": "WoW Subscription", "domain": "blizzard.com", "category": "Gaming"},
    {"id": "humble_choice", "name": "Humble Choice", "domain": "humblebundle.com", "category": "Gaming"},
    {"id": "roblox_premium", "name": "Roblox Premium", "domain": "roblox.com", "category": "Gaming"},
    {"id": "minecraft_realms", "name": "Minecraft Realms", "domain": "minecraft.net", "category": "Gaming"},

    # --- EDUCATION & LEARNING ---
    {"id": "duolingo", "name": "Duolingo Super", "domain": "duolingo.com", "category": "Education"},
    {"id": "masterclass", "name": "MasterClass", "domain": "masterclass.com", "category": "Education"},
    {"id": "skillshare", "name": "Skillshare", "domain": "skillshare.com", "category": "Education"},
    {"id": "coursera", "name": "Coursera Plus", "domain": "coursera.org", "category": "Education"},
    {"id": "udemy", "name": "Udemy Personal", "domain": "udemy.com", "category": "Education"},
    {"id": "brilliant", "name": "Brilliant.org", "domain": "brilliant.org", "category": "Education"},
    {"id": "codecademy", "name": "Codecademy Pro", "domain": "codecademy.com", "category": "Education"},
    {"id": "datacamp", "name": "DataCamp", "domain": "datacamp.com", "category": "Education"},
    {"id": "babbel", "name": "Babbel", "domain": "babbel.com", "category": "Education"},
    {"id": "busuu", "name": "Busuu Premium", "domain": "busuu.com", "category": "Education"},
    {"id": "cambly", "name": "Cambly", "domain": "cambly.com", "category": "Education"},
    {"id": "lingoda", "name": "Lingoda", "domain": "lingoda.com", "category": "Education"},
    {"id": "memrise", "name": "Memrise Pro", "domain": "memrise.com", "category": "Education"},
    {"id": "quizlet", "name": "Quizlet Plus", "domain": "quizlet.com", "category": "Education"},

    # --- HEALTH & FITNESS ---
    {"id": "headspace", "name": "Headspace", "domain": "headspace.com", "category": "Health"},
    {"id": "calm", "name": "Calm", "domain": "calm.com", "category": "Health"},
    {"id": "strava", "name": "Strava Premium", "domain": "strava.com", "category": "Fitness"},
    {"id": "myfitnesspal", "name": "MyFitnessPal Premium", "domain": "myfitnesspal.com", "category": "Health"},
    {"id": "flo", "name": "Flo Premium", "domain": "flo.health", "category": "Health"},
    {"id": "fitbit_premium", "name": "Fitbit Premium", "domain": "fitbit.com", "category": "Fitness"},
    {"id": "peloton", "name": "Peloton App", "domain": "onepeloton.com", "category": "Fitness"},
    {"id": "nike_training", "name": "Nike Training Club", "domain": "nike.com", "category": "Fitness"},
    {"id": "whoop", "name": "Whoop Membership", "domain": "whoop.com", "category": "Fitness"},
    {"id": "sleep_cycle", "name": "Sleep Cycle Premium", "domain": "sleepcycle.com", "category": "Health"},
    {"id": "aura_health", "name": "Aura Health", "domain": "aurahealth.io", "category": "Health"},
    {"id": "noom", "name": "Noom", "domain": "noom.com", "category": "Health"},
    {"id": "workout_trainer", "name": "Workout Trainer", "domain": "skimble.com", "category": "Fitness"},
    {"id": "lifesum", "name": "Lifesum Premium", "domain": "lifesum.com", "category": "Health"},

    # --- SOCIAL & LIFESTYLE ---
    {"id": "linkedin_premium", "name": "LinkedIn Premium", "domain": "linkedin.com", "category": "Social"},
    {"id": "x_premium", "name": "X (Twitter) Premium", "domain": "x.com", "category": "Social"},
    {"id": "tinder_gold", "name": "Tinder Gold", "domain": "tinder.com", "category": "Lifestyle"},
    {"id": "bumble_premium", "name": "Bumble Premium", "domain": "bumble.com", "category": "Lifestyle"},
    {"id": "hinge_plus", "name": "Hinge+", "domain": "hinge.co", "category": "Lifestyle"},
    {"id": "grindr_unlimited", "name": "Grindr Unlimited", "domain": "grindr.com", "category": "Lifestyle"},
    {"id": "uber_one", "name": "Uber One", "domain": "uber.com", "category": "Lifestyle"},
    {"id": "instacart_plus", "name": "Instacart+", "domain": "instacart.com", "category": "Lifestyle"},
    {"id": "walmart_plus", "name": "Walmart+", "domain": "walmart.com", "category": "Lifestyle"},
    {"id": "yemeksepeti_plus", "name": "Yemeksepeti Plus", "domain": "yemeksepeti.com", "category": "Food"},
    {"id": "getir_plus", "name": "Getir+", "domain": "getir.com", "category": "Food"},
    {"id": "migros_money", "name": "Money Pro", "domain": "migros.com.tr", "category": "Food"},
    {"id": "delivery_hero", "name": "Delivery Hero", "domain": "deliveryhero.com", "category": "Food"},
    {"id": "hellofresh", "name": "HelloFresh", "domain": "hellofresh.com", "category": "Food"},
    {"id": "blue_apron", "name": "Blue Apron", "domain": "blueapron.com", "category": "Food"},

    # --- NEWS & READING ---
    {"id": "medium", "name": "Medium Membership", "domain": "medium.com", "category": "News"},
    {"id": "nytimes", "name": "NY Times", "domain": "nytimes.com", "category": "News"},
    {"id": "wsj", "name": "Wall Street Journal", "domain": "wsj.com", "category": "News"},
    {"id": "economist", "name": "The Economist", "domain": "economist.com", "category": "News"},
    {"id": "financial_times", "name": "Financial Times", "domain": "ft.com", "category": "News"},
    {"id": "kindle_unlimited", "name": "Kindle Unlimited", "domain": "amazon.com", "category": "Books"},
    {"id": "magzter", "name": "Magzter Gold", "domain": "magzter.com", "category": "News"},
    {"id": "readly", "name": "Readly", "domain": "readly.com", "category": "News"},
    {"id": "pocket_premium", "name": "Pocket Premium", "domain": "getpocket.com", "category": "Productivity"},
    {"id": "instapaper_premium", "name": "Instapaper Premium", "domain": "instapaper.com", "category": "Productivity"},
    {"id": "the_athletic", "name": "The Athletic", "domain": "theathletic.com", "category": "News"},
    {"id": "substack", "name": "Substack Sub", "domain": "substack.com", "category": "News"},

    # --- OTHERS / VARIOUS ---
    {"id": "surfshark", "name": "Surfshark VPN", "domain": "surfshark.com", "category": "Security"},
    {"id": "nordvpn", "name": "NordVPN", "domain": "nordvpn.com", "category": "Security"},
    {"id": "expressvpn", "name": "ExpressVPN", "domain": "expressvpn.com", "category": "Security"},
    {"id": "proton_mail", "name": "Proton Mail Plus", "domain": "proton.me", "category": "Security"},
    {"id": "mullvad", "name": "Mullvad VPN", "domain": "mullvad.net", "category": "Security"},
    {"id": "strapi", "name": "Strapi Cloud", "domain": "strapi.io", "category": "Productivity"},
    {"id": "netlify", "name": "Netlify Pro", "domain": "netlify.com", "category": "Productivity"},
    {"id": "vercel", "name": "Vercel Pro", "domain": "vercel.com", "category": "Productivity"},
    {"id": "digitalocean", "name": "DigitalOcean", "domain": "digitalocean.com", "category": "Productivity"}
]

# --- REGIONAL PRICE DATABASE (Fallback Data) ---
REGIONAL_PRICES = {
    "netflix": {
        "Standard": {"TRY": 189.99, "USD": 15.49, "EUR": 12.99, "GBP": 10.99},
        "Premium": {"TRY": 299.99, "USD": 22.99, "EUR": 19.99, "GBP": 17.99}
    },
    "spotify": {
        "Individual": {"TRY": 59.99, "USD": 11.99, "EUR": 10.99, "GBP": 11.99},
        "Family": {"TRY": 99.99, "USD": 19.99, "EUR": 17.99, "GBP": 17.99}
    },
    "chatgpt": {
        "Plus": {"USD": 20.00, "EUR": 18.50, "GBP": 16.00, "TRY": 0.0}
    },
    "youtube": {
        "Individual": {"TRY": 57.99, "USD": 13.99, "EUR": 12.99, "GBP": 12.99}
    },
    "icloud": {
        "50GB": {"TRY": 12.99, "USD": 0.99, "EUR": 0.99, "GBP": 0.99},
        "200GB": {"TRY": 39.99, "USD": 2.99, "EUR": 2.99, "GBP": 2.49},
        "2TB": {"TRY": 129.99, "USD": 9.99, "EUR": 9.99, "GBP": 8.99}
    },
    "disneyplus": {
        "Standard": {"TRY": 134.99, "USD": 9.99, "EUR": 8.99, "GBP": 7.99}
    },
    "primevideo": {
        "Prime": {"TRY": 39.00, "USD": 14.99, "EUR": 8.99, "GBP": 8.99}
    }
}

class PriceUpdater:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'

    def clean_price(self, price_str):
        if not price_str: return 0.0
        cleaned = re.sub(r'[^\d.,]', '', price_str)
        cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except:
            return 0.0

    def get_price_with_playwright(self, url, selector, plan_name_map):
        """Scrapes dynamic prices with human-mimicry logic."""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context(
                    user_agent=self.user_agent,
                    viewport={'width': 1920, 'height': 1080}
                )
                page = context.new_page()
                
                # Human Mimicry
                time.sleep(random.uniform(2, 5))
                print(f"  🌐 Navigating to: {url}")
                page.goto(url, wait_until="networkidle", timeout=60000)
                
                page.evaluate("window.scrollTo(0, document.body.scrollHeight / 3)")
                time.sleep(random.uniform(1, 3))
                page.wait_for_timeout(random.randint(2000, 4000))
                
                content = page.content()
                soup = BeautifulSoup(content, 'html.parser')
                browser.close()
                
                prices = {}
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text()
                    for plan_key, plan_name in plan_name_map.items():
                        if plan_key.lower() in text.lower() and ("TL" in text or "₺" in text):
                            prices[plan_name] = {"TRY": self.clean_price(text)}
                
                return prices if prices else None
        except Exception as e:
            print(f"  ❌ Scraping Error: {e}")
            return None

def fetch_best_logo(domain, session):
    if not os.path.exists('logos'): os.makedirs('logos')
    safe_name = domain.replace('.', '_')
    file_path = f"logos/{safe_name}.png"
    
    if os.path.exists(file_path): return True

    urls = [
        f"https://logo.clearbit.com/{domain}?size=512&format=png",
        f"https://www.google.com/s2/favicons?sz=128&domain={domain}"
    ]
    for url in urls:
        try:
            res = session.get(url, timeout=10)
            if res.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(res.content)
                return True
        except: continue
    return False

def generate_catalog():
    updater = PriceUpdater()
    logo_session = requests.Session()
    logo_session.headers.update({'User-Agent': updater.user_agent})

    print(f"🚀 Starting Automated Scraper: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # --- TARGETED LIVE UPDATES ---
    # Sadece taramak istediğimiz ana servisleri buraya ekliyoruz
    live_prices = {
        "netflix": updater.get_price_with_playwright(
            "https://help.netflix.com/tr/node/24926", 
            "li p", 
            {"Standart": "Standard", "Özel": "Premium"}
        ),
    }

    catalog = {
        "version": "3.1",
        "lastUpdated": datetime.now().isoformat(),
        "totalServices": len(SERVICES),
        "services": []
    }

    for index, s in enumerate(SERVICES, 1):
        print(f"[{index}/{len(SERVICES)}] Processing: {s['name']}...")
        
        # 1. Logo Discovery
        fetch_best_logo(s['domain'], logo_session)
        img_name = s['domain'].replace('.', '_') + ".png"
        s['logoUrl'] = f"https://cdn.jsdelivr.net/gh/{GH_USER}/{GH_REPO}/logos/{img_name}"

        # 2. Smart Price Logic (Live > Regional > Default)
        if s['id'] in live_prices and live_prices[s['id']]:
            scraped_plans = live_prices[s['id']]
            s['plans'] = [{"name": n, "prices": p} for n, p in scraped_plans.items()]
            print(f"  ✨ Live update success for {s['name']}")
        elif s['id'] in REGIONAL_PRICES:
            plans_dict = REGIONAL_PRICES[s['id']]
            s['plans'] = []
            for name, prices in plans_dict.items():
                full_prices = {"USD": 0.0, "TRY": 0.0, "EUR": 0.0, "GBP": 0.0}
                full_prices.update(prices)
                s['plans'].append({"name": name, "prices": full_prices})
        else:
            s['plans'] = [{"name": "Standard", "prices": {"TRY": 0.0, "USD": 0.0, "EUR": 0.0, "GBP": 0.0}}]

        catalog['services'].append(s)
        
        # Anti-ban sleep for logos
        if index % 15 == 0:
            time.sleep(1)

    # Save Catalog
    with open('catalog.json', 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ FINISHED: catalog.json updated with {len(SERVICES)} services.")

if __name__ == "__main__":
    generate_catalog()
