import yfinance as yf
import pandas as pd
import numpy as np
import pymongo
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import json

app = FastAPI()
app.title = "Mi primera chamba"
app.version = "16-04-2024"

# Configuracion del cliente y base de datos
cliente = pymongo.MongoClient("mongodb://localhost:27017/")
bd = cliente['integrador']

# Deficnicion de lsitas
colecciones = list()
industrias = ['TSLA', 'SONY', 'META', 'AMZN', 'GOOG']

# Obtencion de informacion utilizando yf.Ticker
for indice in range(len(industrias)):
    industria = yf.Ticker(industrias[indice])
    contenido = industria.info
    reporte = industria.financials
    df =  pd.DataFrame(contenido)
    fecha = max(list(reporte.columns))
    
    # verificar que cada items no venga vacio o Nulo, de ser asi colocar Si Dato
    diccionario = dict(ticker = industrias[indice], country = df["country"][indice], industry = df["industry"][indice], sector = df["sector"][indice], 
                       name = df["companyOfficers"][indice]["name"], age = df["companyOfficers"][indice]["age"], title = df["companyOfficers"][indice]["title"], 
                       tax_rate = reporte[fecha]["Tax Rate For Calcs"], interest_expense = reporte[fecha]["Interest Expense"], 
                       interest_income = reporte[fecha]["Interest Income"], normalized_income = reporte[fecha]["Normalized Income"], 
                       total_ex = reporte[fecha]["Total Expenses"])
    colecciones.append(diccionario)

#Crear la tabla lista_colecciones e inserta los datos
#coleccion = bd['colecciones']
#coleccion.insert_many(colecciones)

# FastAPI

@app.get('/', tags=['home'])
def message():
    """Devuelve el mensaje de 'Hello Word'"""
    return HTMLResponse('<h1>Mi primera chamba</h1>')

@app.get('/colecciones', tags=['colecciones'])
def get_colecciones():
    return colecciones

@app.get('/colecciones/{ticker}', tags=['colecciones'])
def get_colecciones_filter_id(ticker: str):
    for item in colecciones:
        if item["ticker"] == ticker:
            return item
    return []
