import json
import os
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import time
import glob
import urllib.parse

# --- CONFIGURATION ---
GH_USER = "mehmetcan52"
GH_REPO = "subscription-catalog"

# GÜVENLİK: Logo.dev API anahtarını GitHub Actions (veya ortam değişkenlerinden) çekiyoruz
LOGO_DEV_TOKEN = os.getenv("LOGO_DEV_TOKEN")

# --- FULL SERVICES LIST ---
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
    {"id": "viki", "name": "Rakuten Viki", "domain": "viki.com", "category": "Video"},
    {"id": "kanopy", "name": "Kanopy", "domain": "kanopy.com", "category": "Video"},
    {"id": "curiositystream", "name": "CuriosityStream", "domain": "curiositystream.com", "category": "Video"},
    {"id": "britbox", "name": "BritBox", "domain": "britbox.com", "category": "Video"},
    {"id": "shudder", "name": "Shudder", "domain": "shudder.com", "category": "Video"},
    {"id": "starz", "name": "Starz", "domain": "starz.com", "category": "Video"},
    {"id": "mgm_plus", "name": "MGM+", "domain": "mgmplus.com", "category": "Video"},
    {"id": "acorn_tv", "name": "Acorn TV", "domain": "acorn.tv", "category": "Video"},
    {"id": "amc_plus", "name": "AMC+", "domain": "amcplus.com", "category": "Video"},
    {"id": "cineverse", "name": "Cineverse", "domain": "cineverse.com", "category": "Video"},
    {"id": "dropout", "name": "Dropout", "domain": "dropout.tv", "category": "Video"},
    {"id": "vimeo", "name": "Vimeo", "domain": "vimeo.com", "category": "Video"},
    {"id": "dailymotion", "name": "Dailymotion", "domain": "dailymotion.com", "category": "Video"},
    {"id": "twitch", "name": "Twitch", "domain": "twitch.tv", "category": "Video"},
    {"id": "kick", "name": "Kick", "domain": "kick.com", "category": "Video"},
    {"id": "plex", "name": "Plex Pass", "domain": "plex.tv", "category": "Video"},
    {"id": "tivo", "name": "TiVo", "domain": "tivo.com", "category": "Video"},
    {"id": "directv", "name": "DirecTV Stream", "domain": "directv.com", "category": "Video"},
    {"id": "sling_tv", "name": "Sling TV", "domain": "sling.com", "category": "Video"},
    {"id": "philo", "name": "Philo", "domain": "philo.com", "category": "Video"},
    {"id": "pluto_tv", "name": "Pluto TV", "domain": "pluto.tv", "category": "Video"},
    {"id": "tubi", "name": "Tubi TV", "domain": "tubitv.com", "category": "Video"},
    {"id": "dsmart_go", "name": "D-Smart GO", "domain": "dsmartgo.com.tr", "category": "Video"},
    {"id": "tivibu_go", "name": "Tivibu GO", "domain": "tivibu.com.tr", "category": "Video"},

    # --- ARTIFICIAL INTELLIGENCE ---
    {"id": "chatgpt", "name": "ChatGPT Plus", "domain": "openai.com", "category": "AI"},
    {"id": "claude", "name": "Claude Pro", "domain": "anthropic.com", "category": "AI"},
    {"id": "gemini", "name": "Gemini Advanced", "domain": "gemini.google.com", "category": "AI"},
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
    {"id": "copy_ai", "name": "Copy.ai", "domain": "copy.ai", "category": "AI"},
    {"id": "writesonic", "name": "Writesonic", "domain": "writesonic.com", "category": "AI"},
    {"id": "fireflies", "name": "Fireflies.ai", "domain": "fireflies.ai", "category": "AI"},
    {"id": "suno", "name": "Suno AI", "domain": "suno.com", "category": "AI"},
    {"id": "udio", "name": "Udio", "domain": "udio.com", "category": "AI"},
    {"id": "krea", "name": "Krea AI", "domain": "krea.ai", "category": "AI"},
    {"id": "fal_ai", "name": "Fal.ai", "domain": "fal.ai", "category": "AI"},
    {"id": "replicate", "name": "Replicate", "domain": "replicate.com", "category": "AI"},
    {"id": "huggingface", "name": "Hugging Face", "domain": "huggingface.co", "category": "AI"},
    {"id": "synthesia", "name": "Synthesia", "domain": "synthesia.io", "category": "AI"},
    {"id": "character_ai", "name": "Character.ai", "domain": "character.ai", "category": "AI"},
    {"id": "gamma", "name": "Gamma", "domain": "gamma.app", "category": "AI"},
    {"id": "tome", "name": "Tome", "domain": "tome.app", "category": "AI"},
    {"id": "poe", "name": "Poe (Quora)", "domain": "poe.com", "category": "AI"},
    {"id": "perplexity_pages", "name": "Perplexity Pages", "domain": "perplexity.ai", "category": "AI"},
    {"id": "phind", "name": "Phind", "domain": "phind.com", "category": "AI"},
    {"id": "cursor", "name": "Cursor", "domain": "cursor.com", "category": "AI"},
    {"id": "warp", "name": "Warp", "domain": "warp.dev", "category": "AI"},
    {"id": "sourcegraph", "name": "Sourcegraph Cody", "domain": "sourcegraph.com", "category": "AI"},
    {"id": "tabnine", "name": "Tabnine", "domain": "tabnine.com", "category": "AI"},
    {"id": "blackbox_ai", "name": "Blackbox AI", "domain": "blackbox.ai", "category": "AI"},
    {"id": "replit_ghostwriter", "name": "Replit Agent", "domain": "replit.com", "category": "AI"},
    {"id": "adobe_firefly", "name": "Adobe Firefly", "domain": "adobe.com", "category": "AI"},

    # --- MUSIC & AUDIO ---
    {"id": "spotify", "name": "Spotify", "domain": "spotify.com", "category": "Music"},
    {"id": "apple_music", "name": "Apple Music", "domain": "music.apple.com", "category": "Music"},
    {"id": "youtube_music", "name": "YouTube Music", "domain": "music.youtube.com", "category": "Music"},
    {"id": "tidal", "name": "Tidal", "domain": "tidal.com", "category": "Music"},
    {"id": "deezer", "name": "Deezer", "domain": "deezer.com", "category": "Music"},
    {"id": "fizy", "name": "Fizy", "domain": "fizy.com", "category": "Music"},
    {"id": "muud", "name": "Muud", "domain": "muud.com.tr", "category": "Music"},
    {"id": "soundcloud", "name": "SoundCloud Go", "domain": "soundcloud.com", "category": "Music"},
    {"id": "pandora", "name": "Pandora Plus", "domain": "pandora.com", "category": "Music"},
    {"id": "siriusxm", "name": "SiriusXM", "domain": "siriusxm.com", "category": "Music"},
    {"id": "audible", "name": "Audible", "domain": "audible.com", "category": "Books"},
    {"id": "storytel", "name": "Storytel", "domain": "storytel.com", "category": "Books"},
    {"id": "audioteka", "name": "Audioteka", "domain": "audioteka.com", "category": "Books"},
    {"id": "blinkist", "name": "Blinkist", "domain": "blinkist.com", "category": "Books"},
    {"id": "pocket_casts", "name": "Pocket Casts", "domain": "pocketcasts.com", "category": "Music"},
    {"id": "overcast", "name": "Overcast Premium", "domain": "overcast.fm", "category": "Music"},
    {"id": "mixcloud", "name": "Mixcloud Select", "domain": "mixcloud.com", "category": "Music"},
    {"id": "bandcamp", "name": "Bandcamp", "domain": "bandcamp.com", "category": "Music"},
    {"id": "idagio", "name": "IDAGIO", "domain": "idagio.com", "category": "Music"},
    {"id": "primephonic", "name": "Primephonic", "domain": "apple.com", "category": "Music"},
    {"id": "lastfm", "name": "Last.fm Pro", "domain": "last.fm", "category": "Music"},
    {"id": "ultimate_guitar", "name": "Ultimate Guitar Pro", "domain": "ultimate-guitar.com", "category": "Music"},
    {"id": "yousician", "name": "Yousician", "domain": "yousician.com", "category": "Music"},
    {"id": "flowkey", "name": "flowkey", "domain": "flowkey.com", "category": "Music"},
    {"id": "simply_piano", "name": "Simply Piano", "domain": "joytunes.com", "category": "Music"},
    {"id": "splice", "name": "Splice", "domain": "splice.com", "category": "Music"},
    {"id": "loopcloud", "name": "Loopcloud", "domain": "loopcloud.com", "category": "Music"},
    {"id": "beatport", "name": "Beatport Streaming", "domain": "beatport.com", "category": "Music"},
    {"id": "shazam", "name": "Shazam", "domain": "shazam.com", "category": "Music"},
    {"id": "tuner", "name": "Tuner Radio", "domain": "tuner.com", "category": "Music"},

    # --- PRODUCTIVITY & COLLABORATION ---
    {"id": "notion", "name": "Notion", "domain": "notion.so", "category": "Productivity"},
    {"id": "slack", "name": "Slack", "domain": "slack.com", "category": "Productivity"},
    {"id": "zoom", "name": "Zoom", "domain": "zoom.us", "category": "Productivity"},
    {"id": "microsoft_365", "name": "Microsoft 365", "domain": "microsoft.com", "category": "Productivity"},
    {"id": "google_workspace", "name": "Google Workspace", "domain": "workspace.google.com", "category": "Productivity"},
    {"id": "trello", "name": "Trello", "domain": "trello.com", "category": "Productivity"},
    {"id": "asana", "name": "Asana", "domain": "asana.com", "category": "Productivity"},
    {"id": "monday", "name": "Monday.com", "domain": "monday.com", "category": "Productivity"},
    {"id": "clickup", "name": "ClickUp", "domain": "clickup.com", "category": "Productivity"},
    {"id": "evernote", "name": "Evernote", "domain": "evernote.com", "category": "Productivity"},
    {"id": "obsidian", "name": "Obsidian Sync", "domain": "obsidian.md", "category": "Productivity"},
    {"id": "todoist", "name": "Todoist", "domain": "todoist.com", "category": "Productivity"},
    {"id": "ticktick", "name": "TickTick", "domain": "ticktick.com", "category": "Productivity"},
    {"id": "calendly", "name": "Calendly", "domain": "calendly.com", "category": "Productivity"},
    {"id": "loom", "name": "Loom", "domain": "loom.com", "category": "Productivity"},
    {"id": "miro", "name": "Miro", "domain": "miro.com", "category": "Productivity"},
    {"id": "mural", "name": "Mural", "domain": "mural.co", "category": "Productivity"},
    {"id": "lucidchart", "name": "Lucidchart", "domain": "lucid.co", "category": "Productivity"},
    {"id": "basecamp", "name": "Basecamp", "domain": "basecamp.com", "category": "Productivity"},
    {"id": "superhuman", "name": "Superhuman", "domain": "superhuman.com", "category": "Productivity"},
    {"id": "raycast", "name": "Raycast Pro", "domain": "raycast.com", "category": "Productivity"},
    {"id": "setapp", "name": "Setapp", "domain": "setapp.com", "category": "Productivity"},
    {"id": "craft_docs", "name": "Craft Docs", "domain": "craft.do", "category": "Productivity"},
    {"id": "anytype", "name": "Anytype", "domain": "anytype.io", "category": "Productivity"},
    {"id": "linear", "name": "Linear", "domain": "linear.app", "category": "Productivity"},
    {"id": "front", "name": "Front", "domain": "front.com", "category": "Productivity"},
    {"id": "intercom", "name": "Intercom", "domain": "intercom.com", "category": "Productivity"},
    {"id": "zendesk", "name": "Zendesk", "domain": "zendesk.com", "category": "Productivity"},
    {"id": "hubspot", "name": "HubSpot", "domain": "hubspot.com", "category": "Productivity"},
    {"id": "salesforce", "name": "Salesforce", "domain": "salesforce.com", "category": "Productivity"},
    {"id": "airtable", "name": "Airtable", "domain": "airtable.com", "category": "Productivity"},
    {"id": "zapier", "name": "Zapier", "domain": "zapier.com", "category": "Productivity"},
    {"id": "make_com", "name": "Make (Integromat)", "domain": "make.com", "category": "Productivity"},
    {"id": "retool", "name": "Retool", "domain": "retool.com", "category": "Productivity"},
    {"id": "bubble", "name": "Bubble", "domain": "bubble.io", "category": "Productivity"},
    {"id": "webflow", "name": "Webflow", "domain": "webflow.com", "category": "Design"},
    {"id": "framer", "name": "Framer", "domain": "framer.com", "category": "Design"},
    {"id": "figma", "name": "Figma", "domain": "figma.com", "category": "Design"},
    {"id": "canva", "name": "Canva", "domain": "canva.com", "category": "Design"},
    {"id": "adobe_cc", "name": "Adobe Creative Cloud", "domain": "adobe.com", "category": "Design"},
    {"id": "sketch", "name": "Sketch", "domain": "sketch.com", "category": "Design"},
    {"id": "dribbble", "name": "Dribbble Pro", "domain": "dribbble.com", "category": "Design"},
    {"id": "behance", "name": "Behance", "domain": "behance.net", "category": "Design"},
    {"id": "envato_elements", "name": "Envato Elements", "domain": "elements.envato.com", "category": "Design"},
    {"id": "shutterstock", "name": "Shutterstock", "domain": "shutterstock.com", "category": "Design"},

    # --- GAMING & SOCIAL & CREATORS ---
    {"id": "ps_plus", "name": "PlayStation Plus", "domain": "playstation.com", "category": "Gaming"},
    {"id": "xbox_game_pass", "name": "Xbox Game Pass", "domain": "xbox.com", "category": "Gaming"},
    {"id": "nintendo_online", "name": "Nintendo Switch Online", "domain": "nintendo.com", "category": "Gaming"},
    {"id": "apple_arcade", "name": "Apple Arcade", "domain": "apple.com", "category": "Gaming"},
    {"id": "geforce_now", "name": "GeForce NOW", "domain": "nvidia.com", "category": "Gaming"},
    {"id": "discord_nitro", "name": "Discord Nitro", "domain": "discord.com", "category": "Social"},
    {"id": "twitch_turbo", "name": "Twitch Turbo", "domain": "twitch.tv", "category": "Gaming"},
    {"id": "ea_play", "name": "EA Play", "domain": "ea.com", "category": "Gaming"},
    {"id": "ubisoft_plus", "name": "Ubisoft+", "domain": "ubisoft.com", "category": "Gaming"},
    {"id": "wow_sub", "name": "World of Warcraft", "domain": "blizzard.com", "category": "Gaming"},
    {"id": "roblox_premium", "name": "Roblox Premium", "domain": "roblox.com", "category": "Gaming"},
    {"id": "humble_choice", "name": "Humble Choice", "domain": "humblebundle.com", "category": "Gaming"},
    {"id": "steam", "name": "Steam", "domain": "steampowered.com", "category": "Gaming"},
    {"id": "epic_games", "name": "Epic Games", "domain": "epicgames.com", "category": "Gaming"},
    {"id": "battlenet", "name": "Battle.net", "domain": "blizzard.com", "category": "Gaming"},
    {"id": "riot_games", "name": "Riot Games", "domain": "riotgames.com", "category": "Gaming"},
    {"id": "minecraft_realms", "name": "Minecraft Realms", "domain": "minecraft.net", "category": "Gaming"},
    {"id": "gog", "name": "GOG.com", "domain": "gog.com", "category": "Gaming"},
    {"id": "itch_io", "name": "itch.io", "domain": "itch.io", "category": "Gaming"},
    {"id": "chess_com", "name": "Chess.com Gold", "domain": "chess.com", "category": "Gaming"},
    {"id": "lichess", "name": "Lichess Patron", "domain": "lichess.org", "category": "Gaming"},
    {"id": "fortnite_crew", "name": "Fortnite Crew", "domain": "fortnite.com", "category": "Gaming"},
    {"id": "linkedin_premium", "name": "LinkedIn Premium", "domain": "linkedin.com", "category": "Social"},
    {"id": "x_premium", "name": "X Premium", "domain": "x.com", "category": "Social"},
    {"id": "reddit_premium", "name": "Reddit Premium", "domain": "reddit.com", "category": "Social"},
    {"id": "patreon", "name": "Patreon", "domain": "patreon.com", "category": "Social"},
    {"id": "onlyfans", "name": "OnlyFans", "domain": "onlyfans.com", "category": "Social"},
    {"id": "youtube_memberships", "name": "YouTube Kanal Katıl", "domain": "youtube.com", "category": "Social"},

    # --- LIFESTYLE, FOOD & E-COMMERCE ---
    {"id": "tinder_gold", "name": "Tinder Gold", "domain": "tinder.com", "category": "Lifestyle"},
    {"id": "bumble_premium", "name": "Bumble Premium", "domain": "bumble.com", "category": "Lifestyle"},
    {"id": "hinge_plus", "name": "Hinge+", "domain": "hinge.co", "category": "Lifestyle"},
    {"id": "grindr_unlimited", "name": "Grindr Unlimited", "domain": "grindr.com", "category": "Lifestyle"},
    {"id": "uber_one", "name": "Uber One", "domain": "uber.com", "category": "Lifestyle"},
    {"id": "lyft_pink", "name": "Lyft Pink", "domain": "lyft.com", "category": "Lifestyle"},
    {"id": "instacart_plus", "name": "Instacart+", "domain": "instacart.com", "category": "Lifestyle"},
    {"id": "doorDash_pass", "name": "DashPass", "domain": "doordash.com", "category": "Lifestyle"},
    {"id": "delivery_hero", "name": "Delivery Hero", "domain": "deliveryhero.com", "category": "Food"},
    {"id": "yemeksepeti", "name": "Yemeksepeti Plus", "domain": "yemeksepeti.com", "category": "Food"},
    {"id": "getir", "name": "Getir", "domain": "getir.com", "category": "Food"},
    {"id": "hellofresh", "name": "HelloFresh", "domain": "hellofresh.com", "category": "Food"},
    {"id": "blue_apron", "name": "Blue Apron", "domain": "blueapron.com", "category": "Food"},
    {"id": "hepsiburada_premium", "name": "Hepsiburada Premium", "domain": "hepsiburada.com", "category": "Shopping"},
    {"id": "trendyol_pass", "name": "Trendyol Pass", "domain": "trendyol.com", "category": "Shopping"},
    {"id": "airbnb", "name": "Airbnb", "domain": "airbnb.com", "category": "Lifestyle"},
    {"id": "booking_com", "name": "Booking.com", "domain": "booking.com", "category": "Lifestyle"},
    {"id": "expedia", "name": "Expedia", "domain": "expedia.com", "category": "Lifestyle"},
    {"id": "tripadvisor", "name": "Tripadvisor Plus", "domain": "tripadvisor.com", "category": "Lifestyle"},
    {"id": "priority_pass", "name": "Priority Pass", "domain": "prioritypass.com", "category": "Lifestyle"},
    {"id": "hopper", "name": "Hopper", "domain": "hopper.com", "category": "Lifestyle"},
    {"id": "kayak", "name": "KAYAK", "domain": "kayak.com", "category": "Lifestyle"},

    # --- CLOUD, DEV & HOSTING ---
    {"id": "icloud", "name": "iCloud+", "domain": "apple.com", "category": "Cloud"},
    {"id": "google_one", "name": "Google One", "domain": "google.com", "category": "Cloud"},
    {"id": "dropbox", "name": "Dropbox", "domain": "dropbox.com", "category": "Cloud"},
    {"id": "box_com", "name": "Box", "domain": "box.com", "category": "Cloud"},
    {"id": "onedrive", "name": "OneDrive", "domain": "microsoft.com", "category": "Cloud"},
    {"id": "pcloud", "name": "pCloud", "domain": "pcloud.com", "category": "Cloud"},
    {"id": "mega", "name": "MEGA", "domain": "mega.nz", "category": "Cloud"},
    {"id": "backblaze", "name": "Backblaze", "domain": "backblaze.com", "category": "Cloud"},
    {"id": "aws", "name": "Amazon Web Services", "domain": "aws.amazon.com", "category": "Cloud"},
    {"id": "google_cloud", "name": "Google Cloud", "domain": "cloud.google.com", "category": "Cloud"},
    {"id": "azure", "name": "Microsoft Azure", "domain": "azure.microsoft.com", "category": "Cloud"},
    {"id": "digitalocean", "name": "DigitalOcean", "domain": "digitalocean.com", "category": "Cloud"},
    {"id": "linode", "name": "Linode (Akamai)", "domain": "linode.com", "category": "Cloud"},
    {"id": "vultr", "name": "Vultr", "domain": "vultr.com", "category": "Cloud"},
    {"id": "heroku", "name": "Heroku", "domain": "heroku.com", "category": "Cloud"},
    {"id": "vercel", "name": "Vercel", "domain": "vercel.com", "category": "Cloud"},
    {"id": "netlify", "name": "Netlify", "domain": "netlify.com", "category": "Cloud"},
    {"id": "supabase", "name": "Supabase", "domain": "supabase.com", "category": "Cloud"},
    {"id": "firebase", "name": "Firebase", "domain": "firebase.google.com", "category": "Cloud"},
    {"id": "mongodb_atlas", "name": "MongoDB Atlas", "domain": "mongodb.com", "category": "Cloud"},
    {"id": "planetscale", "name": "PlanetScale", "domain": "planetscale.com", "category": "Cloud"},
    {"id": "cloudflare", "name": "Cloudflare", "domain": "cloudflare.com", "category": "Security"},
    {"id": "fastly", "name": "Fastly", "domain": "fastly.com", "category": "Security"},
    {"id": "github", "name": "GitHub Pro", "domain": "github.com", "category": "Productivity"},
    {"id": "gitlab", "name": "GitLab Premium", "domain": "gitlab.com", "category": "Productivity"},
    {"id": "bitbucket", "name": "Bitbucket", "domain": "atlassian.com", "category": "Productivity"},
    {"id": "docker", "name": "Docker Personal", "domain": "docker.com", "category": "Cloud"},
    {"id": "kubernetes", "name": "Kubernetes", "domain": "kubernetes.io", "category": "Cloud"},
    {"id": "terraform", "name": "HashiCorp Terraform", "domain": "hashicorp.com", "category": "Cloud"},
    {"id": "sentry", "name": "Sentry", "domain": "sentry.io", "category": "Cloud"},
    {"id": "datadog", "name": "Datadog", "domain": "datadoghq.com", "category": "Cloud"},
    {"id": "new_relic", "name": "New Relic", "domain": "newrelic.com", "category": "Cloud"},
    {"id": "postman", "name": "Postman", "domain": "postman.com", "category": "Cloud"},
    {"id": "insomnia", "name": "Insomnia", "domain": "insomnia.rest", "category": "Cloud"},
    {"id": "strapi", "name": "Strapi Cloud", "domain": "strapi.io", "category": "Cloud"},
    {"id": "ghost", "name": "Ghost(Pro)", "domain": "ghost.org", "category": "Cloud"},
    {"id": "wordpress", "name": "WordPress.com", "domain": "wordpress.com", "category": "Cloud"},
    {"id": "squarespace", "name": "Squarespace", "domain": "squarespace.com", "category": "Cloud"},
    {"id": "wix", "name": "Wix", "domain": "wix.com", "category": "Cloud"},
    {"id": "shopify", "name": "Shopify", "domain": "shopify.com", "category": "Lifestyle"},

    # --- SECURITY & PRIVACY ---
    {"id": "nordvpn", "name": "NordVPN", "domain": "nordvpn.com", "category": "Security"},
    {"id": "surfshark", "name": "Surfshark", "domain": "surfshark.com", "category": "Security"},
    {"id": "expressvpn", "name": "ExpressVPN", "domain": "expressvpn.com", "category": "Security"},
    {"id": "mullvad", "name": "Mullvad VPN", "domain": "mullvad.net", "category": "Security"},
    {"id": "proton_mail", "name": "Proton Mail", "domain": "proton.me", "category": "Security"},
    {"id": "proton_vpn", "name": "Proton VPN", "domain": "protonvpn.com", "category": "Security"},
    {"id": "tutanota", "name": "Tuta Mail", "domain": "tuta.com", "category": "Security"},
    {"id": "1password", "name": "1Password", "domain": "1password.com", "category": "Security"},
    {"id": "bitwarden", "name": "Bitwarden", "domain": "bitwarden.com", "category": "Security"},
    {"id": "dashlane", "name": "Dashlane", "domain": "dashlane.com", "category": "Security"},
    {"id": "lastpass", "name": "LastPass", "domain": "lastpass.com", "category": "Security"},
    {"id": "malwarebytes", "name": "Malwarebytes", "domain": "malwarebytes.com", "category": "Security"},
    {"id": "bitdefender", "name": "Bitdefender", "domain": "bitdefender.com", "category": "Security"},
    {"id": "norton", "name": "Norton 360", "domain": "norton.com", "category": "Security"},
    {"id": "mcafee", "name": "McAfee", "domain": "mcafee.com", "category": "Security"},
    {"id": "kaspersky", "name": "Kaspersky", "domain": "kaspersky.com", "category": "Security"},
    {"id": "duckduckgo", "name": "DuckDuckGo", "domain": "duckduckgo.com", "category": "Security"},
    {"id": "brave", "name": "Brave Browser", "domain": "brave.com", "category": "Security"},
    {"id": "tor_project", "name": "Tor Project", "domain": "torproject.org", "category": "Security"},
    {"id": "tailscale", "name": "Tailscale", "domain": "tailscale.com", "category": "Security"},
    {"id": "nextdns", "name": "NextDNS", "domain": "nextdns.io", "category": "Security"},
    {"id": "adguard", "name": "AdGuard", "domain": "adguard.com", "category": "Security"},
    {"id": "pivpn", "name": "Pi-VPN", "domain": "pivpn.io", "category": "Security"},
    {"id": "little_snitch", "name": "Little Snitch", "domain": "obdev.at", "category": "Security"},
    {"id": "cleanmymac", "name": "CleanMyMac X", "domain": "macpaw.com", "category": "Security"},

    # --- EDUCATION & LEARNING & NEWS ---
    {"id": "duolingo", "name": "Duolingo", "domain": "duolingo.com", "category": "Education"},
    {"id": "babbel", "name": "Babbel", "domain": "babbel.com", "category": "Education"},
    {"id": "busuu", "name": "Busuu", "domain": "busuu.com", "category": "Education"},
    {"id": "memrise", "name": "Memrise", "domain": "memrise.com", "category": "Education"},
    {"id": "rosetta_stone", "name": "Rosetta Stone", "domain": "rosettastone.com", "category": "Education"},
    {"id": "masterclass", "name": "MasterClass", "domain": "masterclass.com", "category": "Education"},
    {"id": "skillshare", "name": "Skillshare", "domain": "skillshare.com", "category": "Education"},
    {"id": "coursera", "name": "Coursera", "domain": "coursera.org", "category": "Education"},
    {"id": "udemy", "name": "Udemy", "domain": "udemy.com", "category": "Education"},
    {"id": "edx", "name": "edX", "domain": "edx.org", "category": "Education"},
    {"id": "brilliant", "name": "Brilliant.org", "domain": "brilliant.org", "category": "Education"},
    {"id": "khan_academy", "name": "Khan Academy", "domain": "khanacademy.org", "category": "Education"},
    {"id": "codecademy", "name": "Codecademy", "domain": "codecademy.com", "category": "Education"},
    {"id": "datacamp", "name": "DataCamp", "domain": "datacamp.com", "category": "Education"},
    {"id": "freecodecamp", "name": "freeCodeCamp", "domain": "freecodecamp.org", "category": "Education"},
    {"id": "pluralsight", "name": "Pluralsight", "domain": "pluralsight.com", "category": "Education"},
    {"id": "linkedin_learning", "name": "LinkedIn Learning", "domain": "linkedin.com", "category": "Education"},
    {"id": "udacity", "name": "Udacity", "domain": "udacity.com", "category": "Education"},
    {"id": "brilliant_ai", "name": "Brilliant AI", "domain": "brilliant.org", "category": "Education"},
    {"id": "quizlet", "name": "Quizlet", "domain": "quizlet.com", "category": "Education"},
    {"id": "anki", "name": "Anki", "domain": "ankisrs.net", "category": "Education"},
    {"id": "wolfram_alpha", "name": "Wolfram Alpha Pro", "domain": "wolframalpha.com", "category": "Education"},
    {"id": "medium_membership", "name": "Medium", "domain": "medium.com", "category": "News"},
    {"id": "substack", "name": "Substack", "domain": "substack.com", "category": "News"},
    {"id": "the_economist", "name": "The Economist", "domain": "economist.com", "category": "News"},
    {"id": "ny_times", "name": "The New York Times", "domain": "nytimes.com", "category": "News"},
    {"id": "wsj", "name": "Wall Street Journal", "domain": "wsj.com", "category": "News"},
    {"id": "the_atlantic", "name": "The Atlantic", "domain": "theatlantic.com", "category": "News"},
    {"id": "wired", "name": "Wired", "domain": "wired.com", "category": "News"},
    {"id": "hbr", "name": "Harvard Business Review", "domain": "hbr.org", "category": "News"},

    # --- HEALTH, FITNESS & APPLE BUNDLES ---
    {"id": "headspace", "name": "Headspace", "domain": "headspace.com", "category": "Health"},
    {"id": "calm", "name": "Calm", "domain": "calm.com", "category": "Health"},
    {"id": "insight_timer", "name": "Insight Timer", "domain": "insighttimer.com", "category": "Health"},
    {"id": "myfitnesspal", "name": "MyFitnessPal", "domain": "myfitnesspal.com", "category": "Health"},
    {"id": "lifesum", "name": "Lifesum", "domain": "lifesum.com", "category": "Health"},
    {"id": "noom", "name": "Noom", "domain": "noom.com", "category": "Health"},
    {"id": "fitbit_premium", "name": "Fitbit Premium", "domain": "fitbit.com", "category": "Health"},
    {"id": "whoop", "name": "Whoop", "domain": "whoop.com", "category": "Health"},
    {"id": "peloton", "name": "Peloton", "domain": "onepeloton.com", "category": "Health"},
    {"id": "nike_training", "name": "Nike Training Club", "domain": "nike.com", "category": "Health"},
    {"id": "adidas_running", "name": "Adidas Running", "domain": "runtastic.com", "category": "Health"},
    {"id": "flo", "name": "Flo Premium", "domain": "flo.health", "category": "Health"},
    {"id": "clue", "name": "Clue Plus", "domain": "helloclue.com", "category": "Health"},
    {"id": "sleep_cycle", "name": "Sleep Cycle", "domain": "sleepcycle.com", "category": "Health"},
    {"id": "aura_health", "name": "Aura Health", "domain": "aurahealth.io", "category": "Health"},
    {"id": "betterhelp", "name": "BetterHelp", "domain": "betterhelp.com", "category": "Health"},
    {"id": "talkspace", "name": "Talkspace", "domain": "talkspace.com", "category": "Health"},
    {"id": "zocdoc", "name": "Zocdoc", "domain": "zocdoc.com", "category": "Health"},
    {"id": "strava_premium", "name": "Strava Premium", "domain": "strava.com", "category": "Fitness"},
    {"id": "komoot", "name": "Komoot Premium", "domain": "komoot.com", "category": "Fitness"},
    {"id": "alltrails", "name": "AllTrails+", "domain": "alltrails.com", "category": "Fitness"},
    {"id": "apple_fitness", "name": "Apple Fitness+", "domain": "apple.com", "category": "Health"},
    {"id": "apple_one", "name": "Apple One", "domain": "apple.com", "category": "Bundle"}
]

class VectorLogoEngine:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
        }

    def get_extension(self, content_type, url):
        ct = content_type.lower()
        if 'svg' in ct or url.lower().endswith('.svg'): return '.svg'
        if 'webp' in ct: return '.webp'
        if 'png' in ct: return '.png'
        if 'jpeg' in ct or 'jpg' in ct: return '.jpg'
        if 'avif' in ct: return '.avif'
        if 'icon' in ct: return '.ico'
        return '.png'

    def get_itunes_icon(self, name):
        try:
            encoded_name = urllib.parse.quote(name)
            url = f"https://itunes.apple.com/search?term={encoded_name}&entity=software&country=tr&limit=3"
            res = self.session.get(url, headers=self.headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if data.get('resultCount', 0) > 0:
                    return data['results'][0].get('artworkUrl512')
        except:
            pass
        return None

    def scrape_html_for_icon(self, domain):
        try:
            url = f"https://www.{domain}"
            res = self.session.get(url, headers=self.headers, timeout=8)
            if res.status_code != 200: return None
            
            soup = BeautifulSoup(res.text, 'html.parser')
            icons = soup.find_all("link", rel=re.compile(r"apple-touch-icon|icon", re.I))
            
            best_href = None
            max_size = 0

            for icon in icons:
                href = str(icon.get('href'))
                if icon.get('type') == 'image/svg+xml' or href.lower().endswith('.svg') or 'mask-icon' in icon.get('rel', []):
                    best_href = href
                    break 
                
                sizes = icon.get('sizes', '0x0').lower()
                current_size = int(sizes.split('x')[0]) if 'x' in sizes else 0
                if current_size > max_size:
                    max_size = current_size
                    best_href = href
                elif not best_href:
                    best_href = href

            if best_href:
                if not best_href.startswith('http'):
                    best_href = f"https://{domain.strip('/')}/{best_href.lstrip('/')}"
                return best_href
        except:
            pass
        return None

    def fetch_logo(self, service_id, name, domain, base_path):
        simple_name = re.sub(r'[^a-z0-9]', '', service_id.lower())

        def get_lazy_itunes(): return self.get_itunes_icon(name)
        def get_lazy_html(): return self.scrape_html_for_icon(domain)

        # ŞELALE SİSTEMİ (SVG -> PNG -> JPG mantığı eklendi)
        sources = [
            ("Simple Icons (SVG)", f"https://cdn.simpleicons.org/{simple_name}"), 
            ("iTunes API", get_lazy_itunes)
        ]

        # Eğer Logo.dev token'ı sisteme tanımlanmışsa, asıl ağır topları en tepeye ekle
        if LOGO_DEV_TOKEN:
            sources = [
                ("Logo.dev (SVG)", f"https://img.logo.dev/{domain}?token={LOGO_DEV_TOKEN}&format=svg"),
                ("Logo.dev (PNG)", f"https://img.logo.dev/{domain}?token={LOGO_DEV_TOKEN}&format=png&size=512"),
                ("Logo.dev (JPG)", f"https://img.logo.dev/{domain}?token={LOGO_DEV_TOKEN}&format=jpg&size=512")
            ] + sources
            
        sources += [
            ("Clearbit API", f"https://logo.clearbit.com/{domain}?size=512"),
            ("HTML Scraper", get_lazy_html),
            ("DuckDuckGo Icons", f"https://icons.duckduckgo.com/ip3/{domain}.ico"),
            ("Google S2 (256px)", f"https://www.google.com/s2/favicons?domain={domain}&sz=256")
        ]

        for source_name, url_or_func in sources:
            url = url_or_func() if callable(url_or_func) else url_or_func
            if not url: continue
            
            try:
                res = self.session.get(url, headers=self.headers, timeout=8)
                if res.status_code != 200: continue
                
                content_type = res.headers.get('Content-Type', '')
                ext = self.get_extension(content_type, url)
                file_size = len(res.content)
                
                is_valid_svg = ext == '.svg' and file_size > 100
                is_valid_raster = ext != '.svg' and file_size > 1500
                
                if is_valid_svg or is_valid_raster:
                    final_path = f"{base_path}{ext}"
                    with open(final_path, 'wb') as f:
                        f.write(res.content)
                    return source_name, ext
            except:
                continue
                
        return None, None

    def find_cancel_page(self, name, domain):
        """YENİ: Google Arama Motorunu kullanarak iptal sayfalarını tespit eder."""
        try:
            # Aramayı URL formatına çeviriyoruz
            query = urllib.parse.quote(f"how to cancel {name} subscription site:{domain}")
            url = f"https://www.google.com/search?q={query}&hl=en"
            
            # Google'a kendimizi gerçek bir Chrome tarayıcı gibi tanıtıyoruz
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5'
            }

            res = self.session.get(url, headers=headers, timeout=10)
            
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                
                # Google sonuçlarındaki tüm tıklanabilir linkleri tarıyoruz
                for a in soup.find_all('a', href=True):
                    href = a['href']
                    
                    # Eğer link aradığımız şirketin domainini içeriyorsa ve google'ın kendi linki değilse
                    if domain in href and "google.com" not in href:
                        
                        # Google bazen linkleri /url?q=... içine gizler, onu temizliyoruz
                        if href.startswith('/url?q='):
                            clean_url = href.split('/url?q=')[1].split('&')[0]
                            clean_url = urllib.parse.unquote(clean_url)
                            if domain in clean_url:
                                return clean_url
                                
                        # Eğer doğrudan açık link verdiyse
                        elif href.startswith('http'):
                            return href
                            
        except Exception as e:
            pass
            
        # Hiçbir şey bulamazsa manuel Google arama linki bırak (Kırık link olmaması için)
        return f"https://www.google.com/search?q=how+to+cancel+{urllib.parse.quote(name)}+subscription"


def main():
    if not LOGO_DEV_TOKEN:
        print("⚠️ DİKKAT: LOGO_DEV_TOKEN bulunamadı. Logo.dev atlanarak diğer kaynaklar kullanılacak.")
        
    engine = VectorLogoEngine()
    logo_dir = "logos"
    if not os.path.exists(logo_dir): os.makedirs(logo_dir)

    print("🚀 Scraper Started (Ultra Quality Logos + Google Scraper)")

    logos_catalog = {
        "lastUpdated": datetime.now().isoformat(),
        "total": len(SERVICES),
        "data": []
    }
    cancel_catalog = {
        "lastUpdated": datetime.now().isoformat(),
        "total": len(SERVICES),
        "data": []
    }

    for i, s in enumerate(SERVICES, 1):
        domain = s['domain'].replace('https://', '').replace('http://', '').split('/')[0]
        if "googleusercontent" in domain: domain = s['id'] + ".com"
        
        base_fn = domain.replace('.', '_')
        base_path = f"{logo_dir}/{base_fn}"
        
        existing_files = glob.glob(f"{base_path}.*")
        needs_download = True
        final_ext = ""
        
        if existing_files:
            existing_file = existing_files[0]
            file_size = os.path.getsize(existing_file)
            ext = os.path.splitext(existing_file)[1]
            if (ext == '.svg' and file_size > 100) or (ext != '.svg' and file_size > 1500):
                needs_download = False
                final_ext = ext
            if needs_download:
                os.remove(existing_file)

        if needs_download:
            source, ext = engine.fetch_logo(s['id'], s['name'], domain, base_path)
            if source:
                status = f"✅ LOGO ({source})"
                final_ext = ext
            else:
                status = "❌ LOGO YOK"
                final_ext = ".png"
        else:
            status = f"📦 LOGO HAZIR"

        cancel_url = engine.find_cancel_page(s['name'], domain)
        print(f"[{i:03d}/{len(SERVICES):03d}] {status} | İptal: Bulundu -> {s['name']}")
        
        logo_url_full = f"https://cdn.jsdelivr.net/gh/{GH_USER}/{GH_REPO}/{base_path}{final_ext}"
        
        logos_catalog['data'].append({
            "id": s["id"],
            "name": s["name"],
            "category": s["category"],
            "logoUrl": logo_url_full
        })
        cancel_catalog['data'].append({
            "id": s["id"],
            "name": s["name"],
            "domain": s["domain"],
            "cancelUrl": cancel_url
        })
        
        # Google'dan IP ban (Rate Limit / Captcha) yememek için 3.5 saniye bekleme süresi!
        time.sleep(3.5) 

    with open('logos_catalog.json', 'w', encoding='utf-8') as f:
        json.dump(logos_catalog, f, indent=2, ensure_ascii=False)
    with open('cancellation_catalog.json', 'w', encoding='utf-8') as f:
        json.dump(cancel_catalog, f, indent=2, ensure_ascii=False)

    print("\n🏁 İşlem Tamamlandı!")

if __name__ == "__main__":
    main()
