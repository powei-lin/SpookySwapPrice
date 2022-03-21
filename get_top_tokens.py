import requests
from bs4 import BeautifulSoup
import json
from web3 import Web3

ftmscan_tokens = 'https://ftmscan.com/tokens'
res = requests.get(ftmscan_tokens)
soup = BeautifulSoup(res.text, "lxml")
res = soup.findAll('a', {'class': 'text-primary'})
d = {}
for r in res:
    token_address = r.get("href")
    if ("token" in token_address):
        token_address = Web3.toChecksumAddress(
            token_address[token_address.rfind("/") + 1:])
        d[token_address] = r.getText()

with open("top_tokens.json", 'w') as ofile:
    json.dump(d, ofile, indent=4)
# token_name = "NotFound"
# if (res):
#     token_name = res.getText()
