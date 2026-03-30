# 🌍 Global Service Logo Catalog & API

[![Auto Update Subscription Catalog](https://github.com/mehmetcan52/subscription-catalog/actions/workflows/main.yml/badge.svg)](https://github.com/mehmetcan52/subscription-catalog/actions/workflows/main.yml)
![iOS](https://img.shields.io/badge/Platform-iOS%20%2F%20macOS-blue)
![SwiftUI](https://img.shields.io/badge/SwiftUI-6.0-orange)
![Python](https://img.shields.io/badge/Backend-Python%20Scraper-yellow)

This project is a comprehensive, open-source library containing logos, categories, and metadata for **over 300** globally recognized subscriptions, tech tools, and software services. 

It serves as the backend for our **SwiftUI 6.0** applications, providing a reliable and automated **Brand Identity Archive**.

---

## ✨ Features

* **310+ Global Services:** Covers everything from video streaming and AI tools to cloud infrastructure and gaming platforms.
* **Fully Automated Updates:** Powered by GitHub Actions to automatically fetch new or updated logos on the 1st of every month.
* **SwiftUI Ready:** Optimized for high-resolution logo displays in iOS 18 and macOS 15 applications.
* **CDN Support:** Use logos directly via `jsDelivr` for zero-latency loading in your apps.
* **Clean Data (JSON):** All service metadata is stored in a single, developer-friendly `catalog.json` file.

---

## 🛠️ Technical Stack

* **Backend:** Python-based scraper for automated asset management.
* **Frontend:** Designed for modern **SwiftUI 6.0** (iOS/macOS) integration.
* **Automation:** GitHub Actions for scheduled maintenance and delivery.
* **Database:** Lightweight JSON-based catalog.

---

## 🚀 Usage (For Developers)

You can reference logos directly using the GitHub raw link or the jsDelivr CDN for better performance.

**Logo URL Structure (CDN):**
`https://cdn.jsdelivr.net/gh/mehmetcan52/subscription-catalog/logos/netflix_com.png`

**SwiftUI Implementation Example:**
```swift
AsyncImage(url: URL(string: "https://cdn.jsdelivr.net/gh/mehmetcan52/subscription-catalog/logos/netflix_com.png")) { image in
    image.resizable().scaledToFit()
} placeholder: {
    ProgressView()
}
.frame(width: 60, height: 60)
```

---

## 📁 Repository Structure

```text
├── .github/workflows/
│   └── scrape.yml        # Automation engine (Runs monthly)
├── logos/                # Archive of 300+ PNG logos
├── scraper.py            # Python engine for logo fetching
├── catalog.json          # The master JSON database
└── README.md             # Project documentation
```

---

## 🔧 Local Setup

To run the scraper locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/mehmetcan52/subscription-catalog.git
   ```
2. Install dependencies:
   ```bash
   pip install requests
   ```
3. Run the engine:
   ```bash
   python scraper.py
   ```

---

## 🤝 Contributing

Want to add a new service to the catalog? 
Simply add a new entry to the `SERVICES` list in `scraper.py` and submit a **Pull Request**!

---

**⭐ If you find this project useful, please give it a star!**

---
