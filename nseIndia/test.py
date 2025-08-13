import requests
import json

url = "https://www.nseindia.com/api/live-analysis-variations?index=gainers"

payload = {}
headers = {
  'accept': '*/*',
  'accept-language': 'en-GB,en-IN;q=0.9,en-US;q=0.8,en;q=0.7',
  'priority': 'u=1, i',
  'referer': 'https://www.nseindia.com/market-data/top-gainers-losers',
  'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
  'Cookie': '_ga=GA1.1.1106664733.1754978687; nsit=PcSEnuIWYbvVrk1_qJbgLkUk; bm_mi=DFDB12E28C9EB7BDA56B55D19657D370~YAAQhNcLFxZ9y5+YAQAA1owUohyuODbfWuROJsNckv6pyBz10JRyCnK+UENm94RtxtnfLI412WJV0zr5+wTZcEgDZk6iGFGanc6+6whvzy0DrZ5M8yqJuE6BoHkJEKjUGd+toibhGxiKewGB6w8pS1emlrlKaKRmK2UgNqkghV8XUc35X0zH77XhfNRXs90od2yj3aRZkJv/+rpcgHRgNcstuneE0sZ0fC+7fSVLnr7tHSGvCeVdb0LdUfbkKwwvQzQmFcSrNgmS5+TEpxoM6+6cstTpCQY+LLDQm0oPFNfG0CmDkpvpDJe+jHR7/T2UZ8MoFvay2gAgpF4UlpiOXxw42LMA2bkiEUhkptDis0PKkrI4kD8=~1; ak_bmsc=4CBF9DBDB05560F364C30B925D636C56~000000000000000000000000000000~YAAQhNcLFxJ+y5+YAQAAUJIUohzPg2vQQJTE7NqRP18XneIfttpvu2PwvPfQIiv/59FrCRGqRmYMo6bxMPnD7m3s9m2krTmHvdA5YkMpNMIfGwhg+0P/x9+RaIdhOG9rPiLj33qg/Q3UbWFGyP0SBNfYV3jVLdc3j9E69H95PC+M4xATn2YH4pv+wwlYJY/tJzP/cObv3HRYV3DNOFP3ok0tz0xG1jkbnRAoZnkwONOGYiVbYOCeplNPjJuy44TJURq7aKTbfscJaln1YSwBTo/A3HBvYN58vV4RcuGflh77O7hyRQSBn9KpnOPvoWkCd79y+JUAk8T87LoHG1gm9LEFNIezDN8/TJT3Fv4uIiQbi3XLT/C+LdM0s5F7zZlGgIgdJmYEPjiwcP7SuZVnG+HmhJ0cmYeCSOxpcTmmsPNmQdnWOfU2xS8qz8CFv1C5h0CQKdtW/W4xHQzSr2SODOfN9ZGKXABQerL3DYyPnQoVP9PObRNI9OaHb3zoeZM4m8sQP13xd11lGKcK2lGZBdmwqBKoz2E7; AKA_A2=A; _abck=346A27E6C086CA11FDB53173602C8D94~0~YAAQjdcLF2+TAJ6YAQAAC0o/og7ju41fbWL6pQJd6lt3deia0vdig5dTz7Ym4dhVhTdeY2h0+4NqOXQ8XJDfw+px62UWd9/8Qcd1URq0Ewyvu7+1SzdpDtbbWY5p5tLpdZWDKrfyhVsbElOHpZqROPdkDNbEBaTvXj/Vw8bs2ebS7aLfVxS1PRhJnuNIwMY8rTr6+9oLZPXGwHC9yfXgyi0MvGHXcR2MOdzhMU1M6sCmWwz+j6t9H8G9r9VxHKcbzdoCkxHdHE04ph1OeO/o48ZyRmKsu96AzNBVb4Py9wNgy/+8k5KCNwN4jPdCWzvNayIVBEBqq7T6YWShgmmAgTzrfPrVOr07PXp7KfYYJnq9crj3CkeNabVlRr5QhZrhBAlUrV/6Etn88xfj9aFh8kc4KxCcIz6VUk6dg5vRtNHLjWpMMh8lOG81YFj/UTlLTvBp9LZZxyA3eEWawEmdajtWAh21cWs9ba/eqcyvIcoCHtWFobhG0X6EfUjfWmlvCaoa6CZ+vA1QdqW60Chr5sUnCOWWjFFBZgJ1B5pDWYfAon8Y7rR1aGRs4hLsX0uBxLgv0Z9c0ZVK8VBZM6uc9Wm0TEH5DDIt1TMNbw/r7EgX3IL3eW8gowaxNs0mxasuA8IcFY4BV9s5SzzhiRRyURAsMLDLkgnA3gzs74mpTw==~-1~-1~-1; nseappid=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhcGkubnNlIiwiYXVkIjoiYXBpLm5zZSIsImlhdCI6MTc1NTA2ODkwMSwiZXhwIjoxNzU1MDc2MTAxfQ.MAT-7K-v8A5ZVfF6GCw97K9qHt5-ClnxrT1-yGL2B_A; bm_sz=B75DBBB6399435276CD17D5077768F2F~YAAQjdcLF6KSAp6YAQAAxypCohzQxzvhxpM1f7PpptIZu4D5EZzqssOOktQDW7XNUit5+/tCByonr0HNsvODhupZ74qw3K76jNAQYFSLTd1WM0X3m5m+E+blGAGyQtZLCNXtuoFm6toY5kjv93OF0hntS5TAwRJTHZu67HQ06gbPIAUhC+lXr/fX7uwxIhdg7yPs9TUoKcNXwUAFhSaNTmLpIDNWum9rOjUR1oWJojWm2VRbc7s3ygGAWacvfcD1MzV1U0+4AxE2QJQb0qKXw6WZQEWx7UFJe4Erhfx46oOUxs8fhNI6fSQFCQJi1AkSPkodOA+sMOoss2xvFRGagi9N5ejjIoe7khxOagVukYjP1IBFEhs9ScpXYkOW0gP7fEDyqyT063Hn5/BwlpDaZhvqNsut4e8dTFqju4x9u66NnX46YOafM3gZa7CTKMqOpEJR9n9H692UPY3TigiFpKKKc4GieHEEQKlHD9aS93IcILTBev5pKesj0qnHWaEFIvxbbZ+lgSwFYdEGT70EgDaQCU1VI4DLGrN1vfonLs0hlY0GKVApv+ubLKxm~4338480~3491395; RT="z=1&dm=nseindia.com&si=694af66d-7f19-4a71-9338-8847e0932ec7&ss=me9mnkd5&sl=0&se=8c&tt=0&bcn=%2F%2F684d0d41.akstat.io%2F"; bm_sv=3EC17073B3B7A39FA5BE6F23C55F4856~YAAQjdcLFwiUAp6YAQAA6SxCohz8u86exL8dp2toH/AVLm+aXiX5gkXiVXmNR3A+Gff/Dyw4U258B80z7s1IBAk+nZcr/WROYgyNNIMlvsrrbD98NyTSIIKpPAqQJlWcC7a5RYbr+uwol4Pgwje/BkqJi5phhqmApUIf3NiwCfOdYd+FFui2y/b1Tp40aJasTZB5LF+eAueQS4u8ElEJXb8hJoHnk6WTfLkgGmdjyTL6hYFsPpuCJAtTPEu8eHCH0NPABQ==~1; _ga_87M7PJ3R97=GS2.1.s1755063208$o5$g1$t1755068903$j59$l0$h0; _abck=346A27E6C086CA11FDB53173602C8D94~-1~YAAQjdcLF7jqDZ6YAQAAHjZSog7zc7Pa2UKmYXul9BVYD//SeIGqPki7mCP743nI+eyXmZh9JBYF6UlLn4TXaUDpqfTlzOe8WWcSr+4DraU4yyDaI1CuxBM6W2VOsS13Av5SUez8/eXb0pp1OHC6UtqRXlOsfF/1/caCj7LhRoM82YUBBzdAwQmpIr+zA9Krw77qWkuWdWTs5oscXNWxonmeV3ywAYUsxbcuuYp4Plyf/lGEcN7lmtfP0q2mASI6I0yd2ZpRpOHxF1cITHcxzSONMB+UpSJwro1HnQDCUKIm4nZ5AiNpD0+E1n7xhiKlBq3H/k1wjZliwWZ5XMyFOlOAV1OufMC1F9W2OgOXtlwRGCcs4sG+OrAeVunQtfKBYh4BhtaKYkqjB//0wZO25spKqiPK2Ex5vDwVgX6vyoulTY0SChaE87xAY9XJBLT5SrmJKL2rOkvuBvIsA6ElBHLJqX8Ew4AF/Dq8hp66EwhCtkGrALpbPIsGjFZwkfrc2ebULobh5ue+qSRk/pMzgvtOQQIarxvse5+jXa8zeyG/MpcImUe7QZvQMgybEetogDBvlVLGVRqLVeWV1TMToLvZu4jx/w+/Vk7KAc7hW8W6B44fBjxQjda4xmVf1Jezp9laF45zZ1Z6+3+4908M62p1kaqlHHz8PSVnVhpg0g==~0~-1~-1; bm_sv=3EC17073B3B7A39FA5BE6F23C55F4856~YAAQjdcLF7nqDZ6YAQAAHjZSohxxkLjoacnJ2YO3HtsuoOODQuk1s7VKLUy7B1hJrax+pJfD+BhTL+kJQ3ObFHqa9I5DmXWhVTsR09MU9YZKBYJSU+hwBgGXabHSW7VuAJj2x3tuWNlP1Hsui/Vc/7jclhj6S7D/gAPzb0bBjAdzbLx9jEhQtlXph2bcxYITg+7GvFEjI+esFsveg4OY2mW4+grzu/01gMslIRP9wWN80mgzVu+Vj93EFVVzfbmRh+y5XQ==~1'
}

# Step 1: Fetch data from NSE API
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"❌ Request failed: {response.status_code}")
    exit()

try:
    data = response.json()
except json.JSONDecodeError:
    print("❌ Could not parse JSON.")
    exit()

# Step 2: Extract gainers list
gainers_list = data.get("Gainers") or data.get("data", [])

# Step 3: Filter only required legends
allowed_legends = {"NIFTY 50", "BANK NIFTY", "NIFTY NEXT 50"}
filtered_data = [item for item in gainers_list if item.get("legend") in allowed_legends]

if not filtered_data:
    print("⚠ No matching records found.")
    exit()

# Step 4: Save to Excel
df = pd.DataFrame(filtered_data)
excel_filename = "nse_filtered_gainers.xlsx"
df.to_excel(excel_filename, index=False)

print(f"✅ Saved {len(filtered_data)} records to {excel_filename}")