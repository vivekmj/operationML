from datetime import *
import investpy

def five_years_before():
    five_years = (datetime.now() - timedelta(days=5*365)).strftime("%d/%m/%Y")
    return five_years

def get_today():
    return datetime.now().strftime("%d/%m/%Y")

def generate_csv(stock, stock_country):
    df = investpy.get_stock_historical_data(stock=stock, country=stock_country, from_date=five_years_before(), to_date=get_today())
    file_name = stock + "_" + five_years_before().replace('/', '') + "_" + get_today().replace('/', '') + '.csv'
    print(file_name, "created successfully", stock)
    df.to_csv(file_name + '.csv')
    
list_of_stocks = ['ICBK','RELI', 'DLF', 'BRTI','TISC']

for stock in list_of_stocks:
    search_country = investpy.search_quotes(text=stock, products=['stocks'], n_results=1)
    if stock=='RELI':
        generate_csv(stock, 'india')
    else:
        generate_csv(stock, search_country.country)
    