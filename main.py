from flask import Flask,render_template
import pandas as pd 


app=Flask(__name__) 

@app.route("/")
def home():
    return render_template("home.html")  


@app.route("/api/v1/<station>/<date>")
def about(station,date):
    station=station.zfill(6) 
    data="data/TG_STAID"+station+".txt" 
    df=pd.read_csv(data,sep=',',skiprows=20,parse_dates=["    DATE"]) 
    df['TG0']=df['   TG'].mask(df['   TG']==-9999) /10 
    temperature=df.loc[df['    DATE']==date]['TG0'].squeeze()
    return {"station":station,
            "date":date,
            "temperature":temperature} 

if __name__=="__main__":
    app.run(debug=True) 


