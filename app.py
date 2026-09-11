import os
import re
import smtplib
import threading
import webbrowser
from email.message import EmailMessage
from flask import Flask, render_template_string
import requests

app = Flask(__name__)

TRACKED_CARDS = [
    # --- GOD-TIER / EXTREME ENTHUSIAST & HYBRID COOLING ---
    "--- GOD-TIER / EXTREME ENTHUSIAST & HYBRID COOLING ---",
    {
        "name": "EVGA GeForce RTX 3090 KingPin AIO 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAEVG309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=58",
    },
    {
        "name": "KFA2 GeForce RTX 3090 HOF 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAKFA309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=43",
    },

    # --- ELITE AIR-COOLED (Massive Heatsinks & Premium VRMs) ---
    "--- ELITE AIR-COOLED (Massive Heatsinks & Premium VRMs) ---",
    {
        "name": "MSI GeForce RTX 3090 Ti SUPRIM X 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAMSI3090TI24G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=AF5A878DB9954652D656E6849F8E002A&position=15",
    },
    {
        "name": "MSI GeForce RTX 3090 SUPRIM X 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAMSI309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=73F873D2C37EBA0C055F8CC8FF4A48FB&position=16",
    },
    {
        "name": "Asus GeForce RTX 3090 ROG Strix Gaming OC White Ed. 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAASU309024G05&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=EA656D94D96346043BDAE959D26DD99D&position=22",
    },
    {
        "name": "Asus GeForce RTX 3090 ROG Strix Gaming White 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAASU309024G07&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=63",
    },
    {
        "name": "Asus GeForce RTX 3090 ROG Strix Gaming OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAASU309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=82995FD5813C408C986CAA37E8958780&position=30",
    },
    {
        "name": "Asus GeForce RTX 3090 ROG Strix Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAASU309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=64",
    },
    {
        "name": "EVGA GeForce RTX 3090 Ti FTW3 Ultra Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAEVG3090TI24G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=CC6B3806608ED1AC4B96B383865250D4&position=20",
    },
    {
        "name": "EVGA GeForce RTX 3090 FTW3 Ultra Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAEVG309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=CD9EEE87EC894DE5AC3443CF2D0A7709&position=29",
    },
    {
        "name": "Zotac GeForce RTX 3090 Ti AMP Extreme Holo 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAZOT3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=E4C93875DC76D25070225E55DD490479&position=31",
    },
    {
        "name": "Gigabyte Aorus GeForce RTX 3090 Xtreme 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIG309024G05&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=36",
    },
    {
        "name": "Gigabyte Aorus GeForce RTX 3090 Master 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIG309024G04&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=53",
    },
    {
        "name": "Palit GeForce RTX 3090 GameRock 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAPAL309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=A57B506B1741CBA4617F2C475CFCD81B&position=33",
    },
    {
        "name": "Inno3D GeForce RTX 3090 iChill X4 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAINN309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=46",
    },
    {
        "name": "Inno3D GeForce RTX 3090 iChill X3 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAINN309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=45",
    },

    # --- HIGH-MID TIER (Solid Build, Great Daily Drivers) ---
    "--- HIGH-MID TIER (Solid Build, Great Daily Drivers) ---",
    {
        "name": "ASUS GeForce RTX 3090 Ti TUF Gaming OC Edition 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAASU3090TI24G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=EC330EE626A05BADCD418E5092140B6C&position=21",
    },
    {
        "name": "ASUS GeForce RTX 3090 Ti TUF Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAASU3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=62",
    },
    {
        "name": "Asus GeForce RTX 3090 TUF Gaming OC 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAASU309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=7CC837494F36C5A55CBD526CBA4A28AE&position=8",
    },
    {
        "name": "Asus GeForce RTX 3090 TUF Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAASU309024G04&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=821FD88D0B7D36B4033E1783B8D40AF8&position=23",
    },
    {
        "name": "MSI GeForce RTX 3090 Ti Gaming X Trio 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAMSI3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=48785F16536EBC3328B119A6DAD5E893&position=10",
    },
    {
        "name": "MSI GeForce RTX 3090 Gaming X Trio 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAMSI309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=73C44C8DA35B09CDFB33C8227F50DF59&position=17",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Ti Gaming OC 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIGGERTX3090TIOC&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=48",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Gaming OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAGIG309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=AEF70485CD38C8102BC8B39B28C97912&position=28",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Vision OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAGIG309024G06&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=22764BFE2A7234AA5659BD52829D974E&position=34",
    },
    {
        "name": "EVGA GeForce RTX 3090 XC3 Ultra Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAEVG309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=59",
    },
    {
        "name": "Gainward GeForce RTX 3090 Phantom GS 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGAI309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=57",
    },
    {
        "name": "Gainward GeForce RTX 3090 Phantom 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGAI309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=56",
    },
    {
        "name": "Gainward GeForce RTX 3090 Phoenix GS 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGAIRTX3090GS24G&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=55",
    },

    # --- STANDARD / REFERENCE TIER (Expect higher rear VRAM temps) ---
    "--- STANDARD / REFERENCE TIER (Expect higher rear VRAM temps) ---",
    {
        "name": "NVIDIA GeForce RTX 3090 Ti Founders Edition 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRANVI3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=9A819C4F964916BADC51138B6212DC4C&position=14",
    },
    {
        "name": "NVIDIA GeForce RTX 3090 Founders Edition 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRANVI309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=76099B812040D8D6E8905DCA68A337B4&position=6",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Ti Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIGGERTX3090TI&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=49",
    },
    {
        "name": "PNY GeForce RTX 3090 XLR8 Gaming Uprising EpicX RGB 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAPNY309024G03&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=41",
    },
    {
        "name": "PNY GeForce RTX 3090 XLR8 Gaming Revel Epic-X 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAPNY309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=20C7FECB702D0BD60B8D6A8C3E44EBCE&position=9",
    },
    {
        "name": "PNY GeForce RTX 3090 XLR8 Gaming 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAPNY309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=70DE8E3CFFED60C5ADB706F3C3196963&position=32",
    },
    {
        "name": "Zotac GeForce RTX 3090 Trinity OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAZOT3090OC24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=DF1B3BDDE9D5C5179B401FDE147240FC&position=1",
    },
    {
        "name": "Zotac GeForce RTX 3090 Trinity 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAZOT309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=35",
    },
    {
        "name": "KFA2 GeForce RTX 3090 SG 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAKFA309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=F85C45A752412F7408F5EFB4D2D69DC9&position=18",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Eagle OC 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIG309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=54",
    },
    {
        "name": "INNO3D GEFORCE RTX 3090 TI X3 OC 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAINN3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=44",
    },
    {
        "name": "Inno3D GeForce RTX 3090 Gaming X3 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAINN309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=47",
    },
    {
        "name": "Colorful GeForce RTX 3090 Ti NB EX-V 24GB",
        "url": "https://uk.webuy.com/product-detail/?id=SGRACOL3090TI24G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=8B62BF1FBA296577C6AF279002035D44&position=60",
    },

    # --- BUDGET / BLOWER TIER (Higher thermal throttling risks for AI workloads) ---
    "--- BUDGET / BLOWER TIER (Higher thermal throttling risks for AI workloads) ---",
    {
        "name": "Palit GeForce RTX 3090 Gaming Pro OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAPAL309024G02&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=FD8D970F2555E6A16E77825713C7A7BB&position=7",
    },
    {
        "name": "Palit GeForce RTX 3090 Gaming Pro 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAPAL309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=4D538445A86814A5C7E22490FEBA177C&position=13",
    },
    {
        "name": "MSi GeForce RTX 3090 Ventus 3X OC 24GB",
        "url": "https://uk.webuy.com/product-detail?id=SGRAMSI309024G01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=76099B812040D8D6E8905DCA68A337B4&position=3",
    },
    {
        "name": "Gigabyte GeForce RTX 3090 Turbo 24GB (Blower)",
        "url": "https://uk.webuy.com/product-detail/?id=SGRAGIG309024GA01&categoryName=PCI-EXPRESS-GRAPHICS-CARDS&superCatName=COMPUTING&title=&queryID=5D55B53C96854FE1EE9A8C0638E73AD6&position=50",
    },
]

previous_stock_states = {}


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
        is_in_stock = stock_val == 0

        return {"in_stock": is_in_stock, "price": price_str}

    return {"in_stock": False, "price": "£POA"}

  except Exception as e:
    print(f"Error checking stock: {e}")
    return {"in_stock": False, "price": "Error"}


def send_stock_alert_email(card_name, price):
  sender_email = os.environ.get("EMAIL_USER", "your_email@gmail.com")
  email_pass = os.environ.get("EMAIL_PASS", "your_app_password")

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
  except Exception as e:
    print(f"Failed to send email alert: {e}")


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RTX 3090 CeX Stock Hub</title>
    <meta http-equiv="refresh" content="300">
    <style>
        body { background-color: #121212; color: #e0e0e0; font-family: monospace; padding: 2rem; }
        h1 { color: #bb86fc; }
        .section-header { 
            color: #bb86fc; 
            font-weight: bold; 
            font-size: 1.1em; 
            margin-top: 2rem; 
            margin-bottom: 0.75rem; 
            border-bottom: 1px dashed #444; 
            padding-bottom: 4px; 
            letter-spacing: 0.5px;
        }
        .card-row { background: #1e1e1e; padding: 12px 20px; margin: 8px 0; border-radius: 6px; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #333; }
        a { color: #03dac6; text-decoration: none; }
        a:hover { text-decoration: underline; }
        .status-green { color: #03dac6; font-weight: bold; }
        .status-red { color: #cf6679; font-weight: bold; }
    </style>
</head>
<body>
    <h1>RTX 3090 Local AI Hub - CeX Tracker</h1>
    <p>Auto-refreshing every 5 minutes. Ranked by thermal/build quality tier.</p>
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
                <a href="{{ item.url }}" target="_blank">Shortcut to item page ↗</a>
            </div>
        </div>
        {% endif %}
    {% endfor %}
</body>
</html>
"""


@app.route("/")
def dashboard():
  results = []
  for entry in TRACKED_CARDS:
    # If the entry is a plain string, treat it as a category header divider
    if isinstance(entry, str):
      results.append({"is_header": True, "text": entry})
      continue

    status = check_cex_stock(entry["url"])
    is_in_stock = status["in_stock"]
    price = status["price"]
    card_name = entry["name"]

    if card_name in previous_stock_states:
      was_in_stock = previous_stock_states[card_name]
      if not was_in_stock and is_in_stock:
        send_stock_alert_email(card_name, price)

    previous_stock_states[card_name] = is_in_stock

    results.append({
        "is_header": False,
        "name": card_name,
        "in_stock": is_in_stock,
        "price": price,
        "url": entry["url"],
    })

  return render_template_string(HTML_TEMPLATE, results=results)


def open_browser():
  webbrowser.open("http://localhost:5000")


if __name__ == "__main__":
  threading.Timer(1.0, open_browser).start()
  app.run(host="0.0.0.0", port=5000, debug=False)