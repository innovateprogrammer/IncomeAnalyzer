# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, render_template, request, redirect, url_for
from io import BytesIO

import requests
import pandas as pd
import datetime
import plotly.express as px
import json
import plotly
import plotly.graph_objects as go

d={
    'drparijat':'https://docs.google.com/spreadsheets/d/1bM4G32Ai7KO1mk9fkrEmRgelatBeStfog9SSuDSnDMU/edit#gid=',
    'BRGADRE':'https://docs.google.com/spreadsheets/d/1G-4ZquafAN2q2Nobn8Jh-Srw9O4Tdgei2l8U676IDrA/edit#gid='
}
refurl='https://docs.google.com/spreadsheets/d/18zvbTFdIPSVOtvhvxW0ClB6qM_jcTyTwhDaYxSxh7qs/edit#gid=0'
refurl =refurl.replace('/edit#gid=', '/export?format=xlsx&gid=')
def getuserurl(user,year):
    baseurl=d[user]
    baseurl =baseurl.replace('/edit#gid=', '/export?format=xlsx&gid=')
    dumpdf=pd.read_excel(refurl)
    usertable= dumpdf.groupby('username')
    for i in usertable.indices[user]:
        if(dumpdf['year'][i]==int(year)):
            id=dumpdf['sheetid'][i]
    return baseurl+str(id)

def piefunc(df,y,x,t):
  fig = px.pie(df, values=y, names=x, title=t)
  return fig
def mygraph(df,y,x,t):
  fig1 = px.bar(df, x=x, y=y,title=t)
  fig2 = px.line(df, x=x, y=y, title=t)
  fig3 = px.scatter(df, y=y, x=x, color=x)
  fig3.update_traces(marker_size=10)
  fig = go.Figure(data = fig1.data + fig2.data + fig3.data)
  return fig
def patientdensity(df,y,x,h):
  fig = px.scatter(df,size=y, color=x,hover_name=h, size_max=60)
  return fig


global iter
iter=True
global graphJSON
fig=go.Figure()
graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/incomeanalyzer', methods=["POST", "GET"])
def incomeanalyzer():
    if (request.method == 'POST'):
        global iter
        if(iter==True):
            print("hello")
            iter=False
        else:
            user=request.form['user']
            year=request.form['year']
            url=getuserurl(user,year)
            
            df=pd.read_excel(url)
            l=[]
            for i in df['Date']:
                l.append(i.split(" ")[1].strip())
            df['Month']=l
            df=df.drop(['Unnamed: 3','Unnamed: 4','Unnamed: 5','Date','Total Income'],axis=1)

            df2=pd.DataFrame()
            months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            value=[]
            for i in months:
                value.append(df['Amount'][df['Month']==i].sum())
            df2['Month']=months
            df2['Total']=value

            df3=pd.DataFrame()
            df3['Month']=list(set(df['Month']))
            l=[]
            for i in df3['Month']:
                l.append(df['Month'].value_counts()[i])
            df3['Counts']=l
            graphtype=request.form['graphtypes']
            if(graphtype=="1"):
                fig=piefunc(df,'Amount','Patient Name','%Income per Patient(Pie Chart) '+user+' '+year)
            elif(graphtype=="2"):
                fig=piefunc(df,'Amount','Month','%Income per Month(Pie Chart) '+user+' '+year)
            elif(graphtype=="3"):
                fig=patientdensity(df,'Amount','Patient Name','Patient Name')
            elif(graphtype=="4"):
                fig=mygraph(df2,'Total','Month','Monthly Income Chart '+user+' '+year)
            elif(graphtype=="5"):
                fig=piefunc(df3,'Counts','Month','Monthly Patient Footfall(Pie Chart) '+user+' '+year)
            elif(graphtype=="6"):
                fig=mygraph(df3,'Counts','Month','Monthly Patient Footfall(Bar Chart) '+user+' '+year)
            elif(graphtype=="7"):
                fig=patientdensity(df3,'Counts','Month','Month')
            
            global graphJSON
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            
        return render_template('incomeanalyzer.html',graphJSON=graphJSON)
    else:
        return render_template('incomeanalyzer.html',graphJSON=graphJSON)



# main driver function
if __name__ == '__main__':

    app.run(debug=False,host='0.0.0.0')
