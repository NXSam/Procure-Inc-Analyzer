#from tkinter import *               #import UI Elements
#import json                         #JSON Parser
#import requests                     #HTTP GET library
import os
import pandas as pd
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox
import functools
#import datetime

sourceSheet=pd.read_csv(askopenfilename())
lookupSheet=pd.read_csv(askopenfilename())

outputsheet

output sheet=pd.merge(sourceSheet, lookupSheet, on="sku")