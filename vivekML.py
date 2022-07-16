from datetime import *
import investpy
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
import os

def five_years_before():
    five_years = (datetime.now() - timedelta(days=5*365)).strftime("%d/%m/%Y")
    return five_years

def get_today():
    return datetime.now().strftime("%d/%m/%Y")

def generate_stock_csv(stock, stock_country):
    df = investpy.get_stock_historical_data(stock=stock, country=stock_country, from_date=five_years_before(), to_date=get_today())
    file_name = stock + "" + five_years_before().replace('/', '') + "" + get_today().replace('/', '')
    print(file_name, "created successfully", stock)
    df.to_csv('stocks\\' + file_name + '.csv')
    
def generate_index_csv(index, index_country):
    df = investpy.get_index_historical_data(index=index, country=index_country, from_date=five_years_before(), to_date=get_today())
    file_name = index + "" + five_years_before().replace('/', '') + "" + get_today().replace('/', '')
    print(file_name, "created successfully", index)
    df.to_csv('indices\\' + file_name + '.csv')

def stock_operator():
    data = pd.read_csv('stockBook.csv')
    list_of_stocks = data['StockId']

    for stock in list_of_stocks:
        search_country = investpy.search_quotes(text=stock, products=['stocks'], n_results=1)
        if stock=='RELI':
            generate_stock_csv(stock, 'india')
        else:
            generate_stock_csv(stock, search_country.country)

def index_operator():
    data = pd.read_csv('indexBook.csv')
    list_of_indexs = data['IndexName']

    for index in list_of_indexs:
        search_country = investpy.search_quotes(text=index, products=['indices'], n_results=1)
        generate_index_csv(index, search_country.country)
    

def apply_ta():
    folders = ['stocks', 'indices']
    for folder in folders:
        files = os.listdir(folder)
        for file in files:
            try:
                df = pd.read_csv(folder + '/' + file, sep=',')
                df = dropna(df)
                df = add_all_ta_features(df, open="Open", high="High", low="Low", close="Close", volume="Volume", fillna=True)
                df.to_csv(folder + '/' + file)
            except:
                print(folder, "ERROR", file)