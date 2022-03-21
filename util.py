import requests
from bs4 import BeautifulSoup
import json


def get_toekn_name(ftm_scan_token_url, token_address):
    res = requests.get(ftm_scan_token_url + token_address)
    soup = BeautifulSoup(res.text, "lxml")
    res = soup.find('span', {'class': 'text-secondary small'})
    token_name = "NotFound"
    if (res):
        token_name = res.getText()
    return token_name


def load_json(file_path):
    with open(file_path, 'r') as ifile:
        d = json.load(ifile)
    return d
