# 🎌 Subscription Sensei - Global Catalog Engine

[![Auto Update Subscription Catalog](https://github.com/mehmetcan52/subscription-catalog/actions/workflows/main.yml/badge.svg)](https://github.com/mehmetcan52/subscription-catalog/actions/workflows/main.yml)
![iOS](https://img.shields.io/badge/Platform-iOS%20%2F%20macOS-blue)
![SwiftUI](https://img.shields.io/badge/SwiftUI-6.0-orange)
![Python](https://img.shields.io/badge/Backend-Python%20Scraper-yellow)

This repository serves as the **Autonomous Backend** for the Subscription Sensei iOS/macOS application. It manages a high-quality database of over 210+ global and local subscription services with multi-region pricing.

## 🚀 How It Works (The 3-Layer Logic)

The system is designed to be completely hands-off. Every Monday at 00:00 UTC, a GitHub Action triggers the `scraper.py` engine to perform the following:

1.  **HD Logo Discovery:** Automatically finds and downloads 512px Retina-ready logos for each service using Clearbit and Google APIs.
2.  **Multi-Region Pricing:** Syncs verified prices for **USD, TRY, EUR, and GBP**. 
3.  **CDN Delivery:** Serves all assets via **jsDelivr CDN** for lightning-fast loading speeds within the mobile app.

## 📂 Repository Structure

* `scraper.py`: The Python engine that hunts for logos and updates pricing.
* `catalog.json`: The main database consumed by the iOS app.
* `/logos`: Storage for high-resolution (512x512) transparent PNG service icons.
* `.github/workflows/main.yml`: The automation script that keeps everything fresh.

## 📱 App Integration

The Subscription Sensei iOS app connects to this repository's **Raw JSON** to provide users with a "Zero-Input" experience.

* **Smart Search:** Search through 210+ services instantly.
* **Auto-Fill:** When a user selects a service (e.g., Netflix), the app automatically pulls the correct price based on the user's local currency.
* **6-Month Cache:** Once a logo is downloaded to the device, it is cached for 6 months to save data and battery.

## 🛠️ Supported Services (Examples)

| Category | Top Services |
| :--- | :--- |
| **Video** | Netflix, Disney+, Prime Video, BluTV, Gain, Hulu, Max |
| **AI** | ChatGPT Plus, Claude Pro, Midjourney, Perplexity |
| **Music** | Spotify, Apple Music, YouTube Music, Tidal, Fizy |
| **Productivity** | iCloud+, Google One, Microsoft 365, Notion, Adobe CC |
| **Gaming** | PS Plus, Xbox Game Pass, GeForce NOW, Discord Nitro |

## ⚖️ Ethics & Privacy

This scraper only collects **publicly available** pricing information and uses official brand logos provided by discovery APIs. It operates with a polite `time.sleep()` delay to respect service providers' servers.

---
*Maintained by [mehmetcan52](https://github.com/mehmetcan52)*
