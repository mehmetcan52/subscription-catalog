import json
import os
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import time
# --- CONFIGURATION ---
GH_USER = "mehmetcan52"
GH_REPO = "subscription-catalog"

# --- FULL SERVICES LIST (210 ENTRIES) ---
SERVICES = [
    # --- VIDEO & STREAMING (45) ---
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

    # --- ARTIFICIAL INTELLIGENCE (40) ---
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

    # --- MUSIC & AUDIO (30) ---
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

    # --- PRODUCTIVITY & COLLABORATION (45) ---
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

    # --- GAMING & SOCIAL (40) ---
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
    {"id": "tinder_gold", "name": "Tinder Gold", "domain": "tinder.com", "category": "Lifestyle"},
    {"id": "bumble_premium", "name": "Bumble Premium", "domain": "bumble.com", "category": "Lifestyle"},
    {"id": "hinge_plus", "name": "Hinge+", "domain": "hinge.co", "category": "Lifestyle"},
    {"id": "grindr_unlimited", "name": "Grindr Unlimited", "domain": "grindr.com", "category": "Lifestyle"},
    {"id": "linkedin_premium", "name": "LinkedIn Premium", "domain": "linkedin.com", "category": "Social"},
    {"id": "x_premium", "name": "X Premium", "domain": "x.com", "category": "Social"},
    {"id": "reddit_premium", "name": "Reddit Premium", "domain": "reddit.com", "category": "Social"},
    {"id": "strava_premium", "name": "Strava Premium", "domain": "strava.com", "category": "Fitness"},
    {"id": "komoot", "name": "Komoot Premium", "domain": "komoot.com", "category": "Fitness"},
    {"id": "alltrails", "name": "AllTrails+", "domain": "alltrails.com", "category": "Fitness"},
    {"id": "uber_one", "name": "Uber One", "domain": "uber.com", "category": "Lifestyle"},
    {"id": "lyft_pink", "name": "Lyft Pink", "domain": "lyft.com", "category": "Lifestyle"},
    {"id": "instacart_plus", "name": "Instacart+", "domain": "instacart.com", "category": "Lifestyle"},
    {"id": "doorDash_pass", "name": "DashPass", "domain": "doordash.com", "category": "Lifestyle"},
    {"id": "delivery_hero", "name": "Delivery Hero", "domain": "deliveryhero.com", "category": "Food"},
    {"id": "yemeksepeti", "name": "Yemeksepeti Plus", "domain": "yemeksepeti.com", "category": "Food"},
    {"id": "getir", "name": "Getir", "domain": "getir.com", "category": "Food"},
    {"id": "hellofresh", "name": "HelloFresh", "domain": "hellofresh.com", "category": "Food"},
    {"id": "blue_apron", "name": "Blue Apron", "domain": "blueapron.com", "category": "Food"},

    # --- CLOUD, DEV & HOSTING (40) ---
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

    # --- SECURITY & PRIVACY (25) ---
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

    # --- EDUCATION & LEARNING (30) ---
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

    # --- HEALTH, FITNESS & LIFESTYLE (25) ---
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
    {"id": "airbnb", "name": "Airbnb", "domain": "airbnb.com", "category": "Lifestyle"},
    {"id": "booking_com", "name": "Booking.com", "domain": "booking.com", "category": "Lifestyle"},
    {"id": "expedia", "name": "Expedia", "domain": "expedia.com", "category": "Lifestyle"},
    {"id": "tripadvisor", "name": "Tripadvisor Plus", "domain": "tripadvisor.com", "category": "Lifestyle"},
    {"id": "priority_pass", "name": "Priority Pass", "domain": "prioritypass.com", "category": "Lifestyle"},
    {"id": "hopper", "name": "Hopper", "domain": "hopper.com", "category": "Lifestyle"},
    {"id": "kayak", "name": "KAYAK", "domain": "kayak.com", "category": "Lifestyle"}
]

class LogoDevHDPlusEngine:
    def __init__(self):
        self.session = requests.Session()
        # En kaliteli Retina ikonları çekmek için iPhone 15 Pro simülasyonu
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
        }

    def get_apple_icon_fallback(self, domain):
        """Eğer Logo.dev başarısız olursa sitenin içindeki Apple ikonunu arar."""
        try:
            url = f"https://www.{domain}"
            res = self.session.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            # En büyük ikonu bul
            icons = soup.find_all("link", rel=re.compile(r"apple-touch-icon|icon", re.I))
            best_href = None
            max_size = 0

            for icon in icons:
                href = icon.get('href')
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

    def fetch_logo(self, domain, path):
        # ÖNCELİK SIRALAMASI
        sources = [
            # 1. Logo.dev (Ana Kaynak - 512px)
            f"https://img.logo.dev/{domain}?size=512",
            
            # 2. HTML Apple Touch Icon (İkinci en kaliteli kaynak)
            self.get_apple_icon_fallback(domain),
            
            # 3. Clearbit (Yedek - 512px)
            f"https://logo.clearbit.com/{domain}?size=512"
        ]

        for url in sources:
            if not url: continue
            try:
                res = self.session.get(url, headers=self.headers, timeout=10)
                
                # KALİTE KONTROLÜ: 10KB (10.000 byte) altını HD kabul etmiyoruz.
                if res.status_code == 200 and len(res.content) > 10000:
                    with open(path, 'wb') as f:
                        f.write(res.content)
                    return True
            except:
                continue
        return False

def main():
    engine = LogoDevHDPlusEngine()
    logo_dir = "logos"
    if not os.path.exists(logo_dir): os.makedirs(logo_dir)

    print(f"🚀 Logo.dev HD+ Engine Started")

    catalog = {
        "lastUpdated": datetime.now().isoformat(),
        "total": len(SERVICES),
        "services": []
    }

    for i, s in enumerate(SERVICES, 1):
        domain = s['domain'].replace('https://', '').replace('http://', '').split('/')[0]
        logo_fn = f"{domain.replace('.', '_')}.png"
        logo_path = f"{logo_dir}/{logo_fn}"
        
        # Eğer logo yoksa veya 10KB altındaysa (pikselliyse) indir
        needs_update = True
        if os.path.exists(logo_path):
            if os.path.getsize(logo_path) > 10000:
                needs_update = False

        if needs_update:
            success = engine.fetch_logo(domain, logo_path)
            status = "✨ LOGO.DEV HD" if success else "❌ NOT FOUND/LOW RES"
        else:
            status = "📦 ALREADY HD"

        print(f"[{i}/{len(SERVICES)}] {status}: {s['name']}")
        s['logoUrl'] = f"https://cdn.jsdelivr.net/gh/{GH_USER}/{GH_REPO}/{logo_path}"
        catalog['services'].append(s)

    with open('catalog.json', 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print("\n🏁 Mission Accomplished! Catalog is now powered by Logo.dev.")

if __name__ == "__main__":
    main()
