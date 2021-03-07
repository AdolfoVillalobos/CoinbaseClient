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
        self._name = currency_data["balance"]["currency"]
        self._balance = float(currency_data["balance"]["amount"])
        self.code = currency_data["currency"]["code"]
        self.account_id = currency_data["id"]

    def calculate_price(self, rate):
        price = self._balance*rate
        return price

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
            if coin._balance > 0:
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

            roi = round(100*(sell_price-investment)/(investment), 2)
            print(f"Currency: {coin.code} has a Balance: {coin._balance}. The Sell Price: {round(sell_price, 2)} {money_denomination}, ROI: {roi} %")

            sells += sell_price
            purchases += investment

        overall_roi = round(100*(sells-purchases)/(purchases), 2)
        print(f"------ Overall Portfolio Return {overall_roi}")
            

        

if __name__ == "__main__":

    my_wallet = Wallet(API_KEY, API_SECRET)
    my_wallet.calculate_return()
    # api_url = "https://api.coinbase.com/v2/"
    # wallet = CoinbaseWalletAuth(API_KEY, API_SECRET)
    # money = "USD"

    # r = requests.get(api_url+"accounts", auth=wallet)
    # resp = r.json()
  
    # my_wallets = []
    # for currency in resp["data"]:
    #     balance = float(currency["balance"]["amount"])
    #     name = currency["balance"]["currency"]
    #     if balance > 0:
    #         my_wallets.append(currency)
    # for curr in my_wallets:
    #     balance = float(curr["balance"]["amount"])
    #     code = curr["currency"]["code"]
    #     rate = get_sell_price(wallet, api_url, currency=code, money=money)
    #     price = balance*rate
    #     account_id = curr["id"]
        
    #     transactions = get_transactions(wallet, api_url, account_id)
        
    #     original_investment = sum([float(t["native_amount"]["amount"]) for t in transactions])
    #     roi = round(100*(price-original_investment)/(original_investment), 2)

    #     print(f"Currency: {code}, Balance: {balance}, Sell Price: {price} USD, ROI: {roi} %")
        





