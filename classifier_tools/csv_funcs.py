import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime


def create_csv(df,df2=None):
    if  not isinstance(df2,type(None)):
        if df2.empty == False and df.empty == False:
            return pd.concat([df,df2],ignore_index=True).to_csv(index=False).encode('utf-8')
        elif df2.empty == False and df.empty == True:
            return df2.to_csv(index=False).encode('utf-8')
    return df.to_csv(index=False).encode('utf-8')

def create_csv_name(csv_filename:str=None)->str:
    today = datetime.now()
    if csv_filename is not None:
        if not csv_filename.endswith(".csv"):
            csv_filename += ".csv"
    elif csv_filename is None:
        d1 = today.strftime("%d_%m_%Y_hr_%H_%M")
        csv_filename = f"Sniffer_Output_" + d1 + ".csv"
    return csv_filename


