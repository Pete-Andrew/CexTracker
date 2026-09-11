import json
import os
import re
import smtplib
from datetime import datetime
from email.message import EmailMessage
import pytz
import requests

TRACKED_CARDS = [
    "--- GOD-TIER / EXTREME ENTHUSIAST & HYBRID COOLING ---",
    {
        "name": "EVGA GeForce RTX 3090 KingPin AIO 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAEVG309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "KFA2 GeForce RTX 3090 HOF 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAKFA309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    # --- ELITE AIR-COOLED (Massive Heatsinks & Premium VRMs) ---
    "--- ELITE AIR-COOLED (Massive Heatsinks & Premium VRMs) ---",
    {
        "name": "MSI GeForce RTX 3090 Ti SUPRIM X 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAMSI3090TI24G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "MSI GeForce RTX 3090 SUPRIM X 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAMSI309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Asus GeForce RTX 3090 ROG Strix Gaming OC White Ed. 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAASU309024G05&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Asus GeForce RTX 3090 ROG Strix Gaming White 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAASU309024G07&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Asus GeForce RTX 3090 ROG Strix Gaming OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAASU309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Asus GeForce RTX 3090 ROG Strix Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAASU309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "EVGA GeForce RTX 3090 Ti FTW3 Ultra Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAEVG3090TI24G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "EVGA GeForce RTX 3090 FTW3 Ultra Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAEVG309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Zotac GeForce RTX 3090 Ti AMP Extreme Holo 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAZOT3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gigabyte Aorus GeForce RTX 3090 Xtreme 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIG309024G05&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gigabyte Aorus GeForce RTX 3090 Master 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIG309024G04&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Palit GeForce RTX 3090 GameRock 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAPAL309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Inno3D GeForce RTX 3090 iChill X4 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAINN309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Inno3D GeForce RTX 3090 iChill X3 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAINN309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    # --- HIGH-MID TIER (Solid Build, Great Daily Drivers) ---
    "--- HIGH-MID TIER (Solid Build, Great Daily Drivers) ---",
    {
        "name": "ASUS GeForce RTX 3090 Ti TUF Gaming OC Edition 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAASU3090TI24G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "ASUS GeForce RTX 3090 Ti TUF Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAASU3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Asus GeForce RTX 3090 TUF Gaming OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAASU309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=A44CA97D986EDE6566688806AE3D1892&position=1",
    },
    {
        "name": "Asus GeForce RTX 3090 TUF Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAASU309024G04&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "MSI GeForce RTX 3090 Ti Gaming X Trio 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAMSI3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "MSI GeForce RTX 3090 Gaming X Trio 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAMSI309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Ti Gaming OC 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIGGERTX3090TIOC&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Gaming OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAGIG309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Vision OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAGIG309024G06&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "EVGA GeForce RTX 3090 XC3 Ultra Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAEVG309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gainward GeForce RTX 3090 Phantom GS 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGAI309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gainward GeForce RTX 3090 Phantom 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGAI309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gainward GeForce RTX 3090 Phoenix GS 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGAIRTX3090GS24G&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    # --- STANDARD / REFERENCE TIER (Expect higher rear VRAM temps) ---
    "--- STANDARD / REFERENCE TIER (Expect higher rear VRAM temps) ---",
    {
        "name": "NVIDIA GeForce RTX 3090 Ti Founders Edition 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRANVI3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "NVIDIA GeForce RTX 3090 Founders Edition 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRANVI309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Ti Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIGGERTX3090TI&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "PNY GeForce RTX 3090 XLR8 Gaming Uprising EpicX RGB 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAPNY309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "PNY GeForce RTX 3090 XLR8 Gaming Revel Epic-X 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAPNY309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "PNY GeForce RTX 3090 XLR8 Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAPNY309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Zotac GeForce RTX 3090 Trinity OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAZOT3090OC24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=951F091E616E1B7340700892099F8DEE&position=1",
    },
    {
        "name": "Zotac GeForce RTX 3090 Trinity 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAZOT309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "KFA2 GeForce RTX 3090 SG 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAKFA309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Eagle OC 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIG309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "INNO3D GEFORCE RTX 3090 TI X3 OC 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAINN3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Inno3D GeForce RTX 3090 Gaming X3 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAINN309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Colorful GeForce RTX 3090 Ti NB EX-V 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRACOL3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    # --- BUDGET / BLOWER TIER (Higher thermal throttling risks for AI workloads) ---
    "--- BUDGET / BLOWER TIER (Higher thermal throttling risks for AI workloads) ---",
    {
        "name": "Palit GeForce RTX 3090 Gaming Pro OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAPAL309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Palit GeForce RTX 3090 Gaming Pro 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAPAL309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "MSi GeForce RTX 3090 Ventus 3X OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAMSI309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Turbo 24GB (Blower)",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIG309024GA01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING",
    },
]

STATE_FILE = "stock_state.json"
HTML_OUTPUT = "index.html"


def load_previous_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_current_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)


def check_cex_stock(product_url):
    try:
        match = re.search(r"id=([A-Za-z0-9_-]+)", product_url)
        if not match:
            return {"in_stock": False, "price": "Invalid URL"}

        prod_id = match.group(1)
        api_url = f"https://wss2.cex.uk.webuy.io/v3/boxes/{prod_id}/detail"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
        }

        response = requests.get(api_url, headers=headers, timeout=8)
        if response.status_code == 200:
            data = response.json()
            box_data = data.get("response", {}).get("data", {}).get("boxDetails", [])
            if box_data:
                item = box_data[0]
                price_val = item.get("sellPrice")
                stock_val = item.get("outOfStock", 1)
                price_str = f"£{price_val:.2f}" if price_val else "£POA"
                return {"in_stock": stock_val == 0, "price": price_str}

        return {"in_stock": False, "price": "£POA"}
    except Exception as e:
        print(f"Error checking stock for {product_url}: {e}")
        return {"in_stock": False, "price": "Error"}


def send_stock_alert_email(card_name, price):
    sender_email = os.environ.get("EMAIL_USER")
    email_pass = os.environ.get("EMAIL_PASS")

    if not sender_email or not email_pass:
        print("Email credentials not set.")
        return

    msg = EmailMessage()
    msg.set_content(
        f"Good news! {card_name} is now IN STOCK at CeX for {price}.\nCheck it"
        " out immediately."
    )
    msg["Subject"] = f"🚨 CeX Stock Alert: {card_name} Available!"
    msg["From"] = sender_email
    msg["To"] = sender_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, email_pass)
            server.send_message(msg)
        print(f"Alert sent for {card_name}")
    except Exception as e:
        print(f"Failed to send email alert: {e}")


PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RTX 3090 CeX Stock Hub</title>
    <style>
        body { background-color: #121212; color: #e0e0e0; font-family: monospace; padding: 2rem; max-width: 1000px; margin: auto; }
        h1 { color: #bb86fc; }
        .section-header { 
            color: #bb86fc; 
            font-weight: bold; 
            font-size: 1.1em; 
            margin-top: 2rem; 
            margin-bottom: 0.75rem; 
            border-bottom: 1px dashed #444; 
            padding-bottom: 4px; 
        }
        .card-row { background: #1e1e1e; padding: 12px 20px; margin: 8px 0; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #333; }
        a { color: #03dac6; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .status-green { color: #03dac6; font-weight: bold; }
        .status-red { color: #cf6679; font-weight: bold; }
        .timestamp { color: #888; font-size: 0.9em; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>RTX 3090 Local AI Hub - CeX Tracker</h1>
    <div class="timestamp">Last background check: {{ timestamp }}</div>
    <hr style="border: 0; border-top: 1px solid #333; margin-bottom: 20px;">
    
    {% for item in results %}
        {% if item.is_header %}
            <div class="section-header">{{ item.text }}</div>
        {% else %}
        <div class="card-row">
            <div><strong>{{ item.name }}</strong></div>
            <div>
                In stock: 
                {% if item.in_stock %}
                    <span class="status-green">🟢</span>
                {% else %}
                    <span class="status-red">🔴</span>
                {% endif %}
                &nbsp;&nbsp;&nbsp;&nbsp;
                Price: <strong>{{ item.price }}</strong>
                &nbsp;&nbsp;&nbsp;&nbsp;
                <a href="{{ item.url }}" target="_blank">View at CeX ↗</a>
            </div>
        </div>
        {% endif %}
    {% endfor %}
</body>
</html>
"""


def main():
    previous_states = load_previous_state()
    new_states = {}
    results = []

    for entry in TRACKED_CARDS:
        if isinstance(entry, str):
            results.append(
                {"is_header": True, "text": entry.replace("#", "").strip()}
            )
            continue

        card_name = entry["name"]
        url = entry["url"]
        status = check_cex_stock(url)
        is_in_stock = status["in_stock"]
        price = status["price"]

        new_states[card_name] = is_in_stock

        was_in_stock = previous_states.get(card_name, False)
        if not was_in_stock and is_in_stock:
            send_stock_alert_email(card_name, price)

        results.append({
            "is_header": False,
            "name": card_name,
            "in_stock": is_in_stock,
            "price": price,
            "url": url,
        })

    save_current_state(new_states)

    # Generate html rows for template replacement
    html_rows = []
    for item in results:
        if item["is_header"]:
            html_rows.append(f'<div class="section-header">{item["text"]}</div>')
        else:
            green_red = (
                '<span class="status-green">🟢</span>'
                if item["in_stock"]
                else '<span class="status-red">🔴</span>'
            )
            html_rows.append(f"""
            <div class="card-row">
                <div><strong>{item['name']}</strong></div>
                <div>
                    In stock: {green_red}
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    Price: <strong>{item['price']}</strong>
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    <a href="{item['url']}" target="_blank">View at CeX ↗</a>
                </div>
            </div>
            """)

    uk_tz = pytz.timezone('Europe/London')
    timestamp_str = datetime.now(uk_tz).strftime('%Y-%m-%d %H:%M:%S %Z')

    final_page = (
        PAGE_TEMPLATE.replace("{{ timestamp }}", timestamp_str)
        .replace(
            """    {% for item in results %}
        {% if item.is_header %}
            <div class="section-header">{{ item.text }}</div>
        {% else %}
        <div class="card-row">
            <div><strong>{{ item.name }}</strong></div>
            <div>
                In stock: 
                {% if item.in_stock %}
                    <span class="status-green">🟢</span>
                {% else %}
                    <span class="status-red">🔴</span>
                {% endif %}
                &nbsp;&nbsp;&nbsp;&nbsp;
                Price: <strong>{{ item.price }}</strong>
                &nbsp;&nbsp;&nbsp;&nbsp;
                <a href="{{ item.url }}" target="_blank">View at CeX ↗</a>
            </div>
        </div>
        {% endif %}
    {% endfor %}""",
            "\n".join(html_rows),
        )
    )

    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(final_page)


if __name__ == "__main__":
    main()