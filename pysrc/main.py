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


class CryptoCurrency:
    def __init__(self, currency_data):
        self.name = currency_data["balance"]["currency"]
        self.balance = float(currency_data["balance"]["amount"])
        self.code = currency_data["currency"]["code"]
        self.account_id = currency_data["id"]
        self.sell_price = None

    def calculate_price(self, rate):
        self.sell_price = self.balance*rate
        return self.sell_price

    def calculate_return(self, investment):
        self.roi =round(100*(self.sell_price-investment)/(investment), 2)
        return self.roi

    def __str__(self):
        out = f"{self.name} ({self.code}) coin: \n"
        out += f"\t - Balance: {self.balance} \n"
        out += f"\t - Sell Price: {round(self.sell_price, 2)} \n"
        out += f"\t - ROI: {self.roi} % \n"
        return out

class Wallet:
    def __init__(self, api_key, api_secret):

        self.api_url = "https://api.coinbase.com/v2/"
        self.__auth = CoinbaseWalletAuth(api_key, api_secret)
        self.my_coins = []

        self.load_wallet()
    
    def load_wallet(self):
        r = requests.get(self.api_url+"accounts", auth=self.__auth)
        resp = r.json()

        for currency in resp["data"]:
            coin = CryptoCurrency(currency_data=currency)
            if coin.balance > 0:
                self.my_coins.append(coin)
        print("Wallet data has been loaded")

    def load_coin_transactions(self, coin):
        r = requests.get(self.api_url+f"accounts/{coin.account_id}/transactions", auth=self.__auth)
        resp = r.json()["data"]
        resp = [float(t["native_amount"]["amount"]) for t in resp]
        return resp 

    def get_sell_price(self, coin, money_denomination):
        r = requests.get(self.api_url+f"prices/{coin.code}-{money_denomination}/sell", auth=self.__auth)
        resp = float(r.json()["data"]["amount"])
        return resp

    def calculate_return(self, money_denomination="USD"):
        sells = 0
        purchases = 0
        for coin in self.my_coins:
            rate = self.get_sell_price(coin, money_denomination)
            sell_price = coin.calculate_price(rate)
            coin_purchases = self.load_coin_transactions(coin)
            investment = sum(coin_purchases)

            roi = coin.calculate_return(investment)
            print(coin)

            sells += sell_price
            purchases += investment

        overall_roi = round(100*(sells-purchases)/(purchases), 2)
        print(f"------ Overall Portfolio Return {overall_roi} %")
            

        

if __name__ == "__main__":

    my_wallet = Wallet(API_KEY, API_SECRET)
    my_wallet.calculate_return()

        





