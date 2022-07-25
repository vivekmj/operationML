from datetime import *
import investpy
import pandas as pd
import yfinance as yf
import os
from ta import add_all_ta_features
import pandas as pd
from ta.utils import dropna


def calculateDataframeforlogic1(years,filename):

    start_number_years = (datetime.now() - timedelta(days=years*365)).strftime("%Y-%m-%d")

    #print(start_number_years)
    #print(end_number_years)

    #two_years_date= two_years.strptime('%Y-%m-%d')
    #print(number_years)

    df = pd.read_csv("stocks\\" + filename + ".csv")
    df = df.loc[(df['Date'] > start_number_years)]
    #print(len(df))
    #filter = df["Close"]>df["Open"]
    #df = df.loc(filter)
    #rslt_df = df
    df.loc[:, "1dayagoHigh"] = df["High"].shift(periods=1)
    df.loc[:, "1dayagoVolume"] = df["Volume"].shift(periods=1)
    df.loc[:, "1dayafterhighpercent"] = (df["High"].shift(periods=-1)-df["Close"])*100/df["Close"]
    rslt_df = df.loc[(df['Close'] > df["1dayagoHigh"])]
    rslt_df = rslt_df.loc[(df['others_dr'] > 2.0)]

    rslt_df = rslt_df.loc[(rslt_df['Volume'] > rslt_df["1dayagoVolume"])]

    return rslt_df

def getresultofquery(filename,years,percent,acceptablepercent):

    cumpositivepercent = 0.0

    rslt_df = calculateDataframeforlogic1(years,filename)
    #rslt_df.to_csv("endstocks\\" +filename + ".csv")
    positive = len(rslt_df.loc[rslt_df['1dayafterhighpercent'] > percent])

    total =len(rslt_df)



    if (total >0 and positive*100/total >acceptablepercent):
        #print(str(year) +  "years")
        #print(filename + ' '  + str(positive*100/total))
        cumpositivepercent = positive*100/total
    elif(total >0):
        cumpositivepercent = positive*100/total
    else:
        if(total >0):
            cumpositivepercent = positive*100/total
            #print(str(year) +  "years less than 80%")
            #print(filename + ' '  + str(positive*100/total))

        #print(year+1)

    if(cumpositivepercent >= acceptablepercent):
        print("cumulative percent for " + str(filename) +  "for " + str(years) + " years for " + str(percent) + " percent increase the next day  is " + str(cumpositivepercent))
        #print(year)





    #rslt_df.loc[:,"1dayafterHigh"] = rslt_df["High"].shift(periods=-1)
    #rslt_df.loc[:,"2dayafterHigh"] = rslt_df["High"].shift(periods=-2)
    #rslt_df["1dayafterHighpercent"] = (rslt_df["1dayafterHigh"]-rslt_df["Close"])*100/rslt_df["Close"]
    #rslt_df["2dayafterHighpercent"] = (rslt_df["2dayafterHigh"]-rslt_df["Close"])*100/rslt_df["Close"]
    #rslt_df = df.loc[(df['Close'] > df["Open"])]
    #rslt_df = rslt_df.loc[(rslt_df['Close'] > rslt_df["High"] *0.995)]

    #rslt_df = rslt_df.loc[(rslt_df['Low'] > rslt_df["1dayagoHigh"])]


    return rslt_df

    #return df.query('Close>Open and Close>=High*0.995')

def stock_success_percent():
    data = pd.read_csv('stockBook.csv')
    list_of_stocks = data['scrip']
    counter =0
    for stock in list_of_stocks:
        #scripname = data['scrip'].iloc[counter]
        #counter+=1
        #print(stock)

        df =getresultofquery(stock,2,1,80)
        #print(len(df))
    print('all stocks success checked')

def getresultofquery_details(filename):
    df = pd.read_csv("stocks\\" + filename + ".csv")
    #filter = df["Close"]>df["Open"]
    #df = df.loc(filter)
    #rslt_df = df
    df.loc[:, "1dayagoHigh"] = df["High"].shift(periods=1)
    df.loc[:, "1dayagoVolume"] = df["Volume"].shift(periods=1)
    df.loc[:, "1dayafterhighpercent"] = (df["High"].shift(periods=-1)-df["Close"])*100/df["Close"]
    rslt_df = df.loc[(df['Close'] > df["1dayagoHigh"])]
    rslt_df = rslt_df.loc[(df['others_dr'] > 2.0)]

    rslt_df = rslt_df.loc[(rslt_df['Volume'] > rslt_df["1dayagoVolume"])]

    #positive = len(rslt_df.loc[rslt_df['1dayafterhighpercent'] >1.0])

    #total =len(rslt_df)
    #if positive*100/total >80.0:
    #print(filename + ' '  + str(positive*100/total))
    rslt_df



    #rslt_df.loc[:,"1dayafterHigh"] = rslt_df["High"].shift(periods=-1)
    #rslt_df.loc[:,"2dayafterHigh"] = rslt_df["High"].shift(periods=-2)
    #rslt_df["1dayafterHighpercent"] = (rslt_df["1dayafterHigh"]-rslt_df["Close"])*100/rslt_df["Close"]
    #rslt_df["2dayafterHighpercent"] = (rslt_df["2dayafterHigh"]-rslt_df["Close"])*100/rslt_df["Close"]
    #rslt_df = df.loc[(df['Close'] > df["Open"])]
    #rslt_df = rslt_df.loc[(rslt_df['Close'] > rslt_df["High"] *0.995)]

    #rslt_df = rslt_df.loc[(rslt_df['Low'] > rslt_df["1dayagoHigh"])]


    return rslt_df

    #return df.query('Close>Open and Close>=High*0.995')

stock_success_percent()

getresultofquery_details('BEML')