import requests
import pandas as pd
import time
import json
from openpyxl import Workbook
from getCookiesFromNSEIndia import CookieManager


class NseTestDataExporter:

    def __init__(self):
        cm = CookieManager()  # Create instance of CookieManager
        self.cookies = cm.fetch_cookies()  # Fetch cookies
        print("Using cookies:", self.cookies)
       
        self.marketIndices = [
            "Broad Market Indices",
            "Sectoral Indices"
            # Add more if needed
        ]

        # === Load access token from Authentication.json ===
        with open("nseIndiaCookies_name_value.json", "r") as f:
                auth_data = json.load(f)
        _ga = auth_data.get("_ga")
        abck = auth_data.get("_abck")
        AKA_A2 = auth_data.get("AKA_A2")
        nsit = auth_data.get("nsit")
        nseappid = auth_data.get("nseappid")
        bm_mi = auth_data.get("bm_mi")
        bm_sz = auth_data.get("bm_sz")
        ak_bmsc = auth_data.get("ak_bmsc")
        _ga_87M7PJ3R97 = auth_data.get("_ga_87M7PJ3R97")
        bm_sv = auth_data.get("bm_sv")
        RT = auth_data.get("RT")
        _abck = auth_data.get("_abck")
        bm_sv = auth_data.get("bm_sv")

        self.broad_indices_url_template = "https://www.nseindia.com/api/heatmap-index?type={market_index}"
        self.gainers_url_template = "https://www.nseindia.com/api/heatmap-symbols?type={market_index}&indices={indices}"
        self.headers_broad_indices = {
            'accept': '*/*',
            'accept-language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7',
            'priority': 'u=1, i',
            'referer': 'https://www.nseindia.com/market-data/live-market-indices/heatmap',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Cookie': f'_ga={_ga};abck={abck};AKA_A2={AKA_A2};nsit={nsit};nseappid={nseappid};bm_mi={bm_mi};bm_sz={bm_sz};ak_bmsc={ak_bmsc};_ga_87M7PJ3R97={_ga_87M7PJ3R97};bm_sv={bm_sv};abck={abck};bm_sv={bm_sv}'
        }
        self.headers_gainers_url = {
                  'accept': '*/*',
                  'accept-language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7',
                  'priority': 'u=1, i',
                  'referer': 'https://www.nseindia.com/market-data/live-market-indices/heatmap',
                  'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
                  'sec-ch-ua-mobile': '?0',
                  'sec-ch-ua-platform': '"Windows"',
                  'sec-fetch-dest': 'empty',
                  'sec-fetch-mode': 'cors',
                  'sec-fetch-site': 'same-origin',
                  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
                  'Cookie': f'_ga={_ga};abck={abck};AKA_A2={AKA_A2};nsit={nsit};nseappid={nseappid};bm_mi={bm_mi};bm_sz={bm_sz};ak_bmsc={ak_bmsc};_ga_87M7PJ3R97={_ga_87M7PJ3R97};bm_sv={bm_sv};abck={abck};bm_sv={bm_sv}'
        }
        self.payload = {}

        # Use a session for persistent headers and cookies
        self.session = requests.Session()
        self.session.headers.update(self.headers_broad_indices)

    def fetch_broad_market_indices(self, market_index):
        url = self.broad_indices_url_template.format(market_index=market_index.replace(" ", "%20"))
        response = self.session.get(url)
        print(f"Fetching broad market indices for: {market_index}")
        print("Status Code:", response.status_code)
        if response.status_code == 200:
            try:
                data = response.json()
            except Exception as e:
                print("JSON decode error:", e)
                return []
            indices_list = []
            if isinstance(data, dict):
                for value in data.values():
                    if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                        indices_list = value
                        break
            else:
                indices_list = data if isinstance(data, list) else []
            return indices_list
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            print("Response:", response.text[:500])
            return []

    def fetch_gainers_for_indices(self, market_index, indices_list):
        all_data = []
        for index_info in indices_list:
            index_name = list(index_info.values())[0]
            url = self.gainers_url_template.format(
                market_index=market_index.replace(" ", "%20"),
                indices=index_name.replace(" ", "%20")
            )
            # Update session headers for gainers endpoint
            self.session.headers.update(self.headers_gainers_url)
            response = self.session.get(url)
            print(f"Requesting gainers for Indices: {index_name} ({market_index})")
            print("Status Code:", response.status_code)
            if response.status_code == 200:
                try:
                    gainers_data = response.json()
                    if isinstance(gainers_data, list):
                        for row in gainers_data:
                            combined_row = {**index_info, **row, "MarketIndex": market_index}
                            all_data.append(combined_row)
                except Exception as e:
                    print("JSON decode error:", e)
            else:
                print("Failed to fetch data. Status code:", response.status_code)
                print("Response:", response.text[:500])
            time.sleep(2)  # polite delay
        return all_data

    def export_to_excel(self, broad_indices_dict, gainers_dict, filename="nse_combined_data.xlsx"):
        with pd.ExcelWriter(filename) as writer:
            for market_index in self.marketIndices:
                broad_df = pd.DataFrame(broad_indices_dict.get(market_index, []))
                gainers_df = pd.DataFrame(gainers_dict.get(market_index, []))
                # Truncate sheet names to 31 characters
                broad_sheet = f"{market_index}_Broad"[:31]
                gainers_sheet = f"{market_index}_Gainers"[:31]
                broad_df.to_excel(writer, sheet_name=broad_sheet, index=False)
                gainers_df.to_excel(writer, sheet_name=gainers_sheet, index=False)
        print(f"Exported all responses to {filename}")

    def run(self):       
        broad_indices_dict = {}
        gainers_dict = {}
        for market_index in self.marketIndices:
            broad_indices = self.fetch_broad_market_indices(market_index)
            broad_indices_dict[market_index] = broad_indices
            gainers_data = self.fetch_gainers_for_indices(market_index, broad_indices)
            gainers_dict[market_index] = gainers_data
        self.export_to_excel(broad_indices_dict, gainers_dict)

if __name__ == "__main__":
    exporter = NseTestDataExporter()
    exporter.run()