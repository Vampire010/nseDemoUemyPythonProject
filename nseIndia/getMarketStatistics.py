import requests
import json
from openpyxl import Workbook


# === Load access token from Authentication.json ===
with open("nseIndiaCookies.json", "r") as f:
    auth_data = json.load(f)
Cookie = auth_data.get("Cookie")


url = "https://www.nseindia.com/api/NextApi/apiClient?functionName=getMarketStatistics"

payload = {}
headers = {
  'accept': '*/*',
  'accept-language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7',  
  'referer': 'https://www.nseindia.com/', 
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
  'Cookie': f'{Cookie}'
}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()  # Convert response to dict

total = data['data']['snapshotCapitalMarket']['total']
unchange = data['data']['snapshotCapitalMarket']['unchange']
advances = data['data']['snapshotCapitalMarket']['advances']
declines = data['data']['snapshotCapitalMarket']['declines']
asOnDate = data['data']['asOnDate']

print("Stock Traded:", total)
print("Unchanged:", unchange)
print("Advances:", advances)
print("declines:", declines)
print("asOnDate:", asOnDate)

