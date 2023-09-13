from flask import Flask,render_template
import pandas as pd 


app=Flask(__name__) 

@app.route("/")
def home():
    df=pd.read_csv("data\stations.txt",skiprows=17)
    df=df[['STAID','STANAME                                 ']][:101]
    # The data takes in a parameter that is rendered in the html templates 
    # CHECK home.html and see how it was rendered
    # df.to_html() is a method used to convert the pandas table to html table
    return render_template("home.html",data=df.to_html())  


@app.route("/api/v1/<station>/<date>")
def temperature(station,date):
    # This allows the total digit to be up to 6 by adding extra zeros if necessary
    # So if we input 10 we will have 000010
    station=station.zfill(6) 
    data="data/TG_STAID"+station+".txt" 
    #the parse_dates renders the date column as a normal date format
    df=pd.read_csv(data,sep=',',skiprows=20,parse_dates=["    DATE"]) 
    # Creating another column called TGO. we divide it by 10 to get the actual value
    # the data was originally multiplied by 10
    # The MASK method masks values with -9999. It automatically replaces them with NAN
    df['TG0']=df['   TG'].mask(df['   TG']==-9999) /10 
    # The loc method is carefully explaioned in the tutorial.ipynb file
    temperature=df.loc[df['    DATE']==date]['TG0'].squeeze()
    return {"station":station,
            "date":date,
            "temperature":temperature}   

@app.route("/api/v1/<station>")
def all_data(station):
    station=station.zfill(6) 
    data="data/TG_STAID"+station+".txt"   
    df=pd.read_csv(data,sep=',',skiprows=20,parse_dates=["    DATE"]) 
    df['   TG']=df['   TG']/10 
    result=df.to_dict(orient="records")
    return result   

@app.route("/api/v1/yearly/<station>/<year>") 
def yearly(station,year):
    station=station.zfill(6) 
    data="data/TG_STAID"+station+".txt"   
    df=pd.read_csv(data,sep=',',skiprows=20) 
    # astype(str) converts the date column to string
    df['    DATE'] = df['    DATE'].astype(str)
    result=df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return result

if __name__=="__main__":
    app.run(debug=True) 


