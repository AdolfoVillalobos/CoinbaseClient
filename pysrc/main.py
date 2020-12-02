import os
import requests 
import json 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
from api_auth import CoinbaseWalletAuth

API_KEY = os.environ["COINBASE_KEY"]
API_SECRET = os.environ["COINBASE_SECRET"]


def get_sell_price(auth, api_url, currency, money):
    r = requests.get(api_url+f"prices/{currency}-{money}/sell", auth=auth)
    resp = float(r.json()["data"]["amount"])
    return resp

def get_transactions(auth, api_url, account_id):
    r = requests.get(api_url+f"accounts/{account_id}/transactions", auth=auth)
    resp = r.json()["data"]
    return resp


if __name__ == "__main__":
    api_url = "https://api.coinbase.com/v2/"
    wallet = CoinbaseWalletAuth(API_KEY, API_SECRET)
    money = "USD"

    r = requests.get(api_url+"accounts", auth=wallet)
    resp = r.json()
  
    my_wallets = []
    for currency in resp["data"]:
        balance = float(currency["balance"]["amount"])
        name = currency["balance"]["currency"]
        if balance > 0:
            my_wallets.append(currency)
    for curr in my_wallets:
        balance = float(curr["balance"]["amount"])
        code = curr["currency"]["code"]
        rate = get_sell_price(wallet, api_url, currency=code, money=money)
        price = balance*rate
        account_id = curr["id"]
        
        transactions = get_transactions(wallet, api_url, account_id)
        
        original_value = sum([float(t["native_amount"]["amount"]) for t in transactions])
        roi = round(100*(price-original_value)/(original_value), 2)

        print(f"Currency: {code}, Balance: {balance}, Sell Price: {price} USD, ROI: {roi} %")
        





