import requests
import pandas as pd
import json
from openpyxl import Workbook


# === Load access token from Authentication.json ===
with open("nseIndiaCookies.json", "r") as f:
    auth_data = json.load(f)
COOKIE_STRING = auth_data.get("Cookie")

URL = "https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketSnapshot&&type=G"

HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1, i',
    'referer': 'https://www.nseindia.com/',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'cookie': COOKIE_STRING
}

def fetch_market_snapshot():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        top_gainers = data.get("data", {}).get("topGainers", [])

        if not top_gainers:
            print("⚠ No data found for top gainers.")
            return

        # Select only useful columns
        df = pd.DataFrame(top_gainers, columns=[
            "symbol", "series", "openPrice", "highPrice", "lowPrice", "lastPrice",
            "previousClose", "change", "pchange", "totalTradedVolume"
        ])

        # Format numbers
        df["openPrice"] = df["openPrice"].round(2)
        df["highPrice"] = df["highPrice"].round(2)
        df["lowPrice"] = df["lowPrice"].round(2)
        df["lastPrice"] = df["lastPrice"].round(2)
        df["previousClose"] = df["previousClose"].round(2)
        df["change"] = df["change"].round(2)
        df["pchange"] = df["pchange"].round(2)

        print("\n📊 Top Gainers Table\n")
        print(df.to_string(index=False))

    except requests.exceptions.RequestException as e:
        print(f"❌ Request failed: {e}")
    except ValueError:
        print("❌ Failed to parse JSON response.")

if __name__ == "__main__":
    fetch_market_snapshot()
