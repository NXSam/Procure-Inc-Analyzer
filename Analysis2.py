from tkinter import *               #import UI Elements
import json                         #JSON Parser
import requests                     #HTTP GET library
import os
import pandas as pd
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter import messagebox
import functools
import datetime
import glob

class App:

    def __init__(self, master):

        #Initial Values/Variables

        self.master = master
        master.title("Analysis Generator")
        master.minsize(width=500, height=500)           #Set starting size.
        self.projectsToGet = []                         #Array of all projects to be downloaded
        self.dirName=""
        self.btn_dict= []
        self.data_dict=[]                                                                                              



        self.button_GetFiles = Button(master, text="Get Available Crawls", command=lambda: self.getFiles())              #Create Button to retrieve PH Projects
        self.button_GetFiles.grid(row=2, column=2)                                                                                     #Set position
        self.b_Color=self.button_GetFiles.cget("bg")                                                                         #Get Default BG Color
        self.f_Color=self.button_GetFiles.cget("fg")


        for x in range (0,5):
            root.columnconfigure(x, minsize=20, weight=1, pad=2)                                                                             #Configure Grid
                                              
    def getFiles(self):
        self.dirName=askdirectory()                                                                                              #Get all projects
        projects=[]
        index=0
        for item in glob.glob(self.dirName + "/*.csv"):
            try:
                print(os.path.basename(item))
                projects.append(pd.read_csv(item))
                projects[index].columns=projects[index].columns.str.replace('^.*\_', '')
                tempname=projects[index]['Competitor'][0] +"_RMultiplier"
                projects[index][tempname]="=C2/Procure Cost"
            except:
                    print(os.path.basename(item) + " has failed.")
            index+=1

        index=1
        self.assembled = projects[0]
        for data in projects:
            try:
                self.assembled= pd.merge(self.assembled, projects[index], on="Part", how="outer")
                #self.assembled = functools.reduce(lambda left, right: pd.merge(left, right, on="Part", how="outer"), self.data_dict[index])
            except:
                #print("ERROR Occured " + str(self.projectsToGet[index]))
                pass
            index+=1

        self.xp=projects                                                                      #Load "Projects" from PH JSON
        row=5                                                                                                          #Store starting row for button-array
        column = 0;
        i=0


        self.label_Setup=Label(self.master, text="Setup Analysis")
        self.label_Setup.grid(row=row+2, column=2,padx=5,pady=5)
        self.Button_SaveDir=Button(self.master, text="Set Save Directory", command= self.setSave, width=20)
        self.Button_SaveDir.grid(row=row+3, column=2, padx=5, pady=5)
        #self.Button_Download=Button(self.master, text="Download Crawls", command=self.Download, width=20)
        #self.Button_Download.grid(row=row+3, column=3, padx=5,pady=5)
        self.Button_VendorSheet=Button(self.master, text="Import Pricing", command= self.getVendor, width=20)
        self.Button_VendorSheet.grid(row=row+3, column=0, padx=5, pady=5)
        self.Button_MultiplierSheet=Button(self.master, text="Import Multiplier", command= self.getMult, width=20)
        self.Button_MultiplierSheet.grid(row=row+3, column=1, padx=5, pady=5)
        self.Button_MergeCost=Button(self.master, text="Apply Cost", command=self.applyCost, width=20)
        self.Button_MergeCost.grid(row=row+4, column=2, padx=4, pady=5)
        self.Button_Export=Button(self.master, text="Export Data", command=self.export, width=20)
        self.Button_Export.grid(row=row+5, column=2, padx=5, pady=5)

        self.Multiplier=StringVar()
        self.Multiplier.trace("w", lambda name, index, mode, MS=self.Multiplier: self.MUpdate(MS))
        self.input_Multiplier=Entry(self.master, textvariable=self.Multiplier)
        self.input_Multiplier.grid(row=row+3, column=4, padx=10, pady=10)


    def MUpdate(self, MS):
        self.aMultiplier=float(self.input_Multiplier.get())

    def setSave(self):
        self.dirName=askdirectory()

    def getVendor(self):
        fields = ['Part', 'Multiplier', 'List', 'Cost']
        #dtypes = {'Part':'object', 'Multiplier':'float', 'List':'float', 'Cost':'float'}
        self.vendorSheet=pd.read_csv(askopenfilename(), usecols=fields,)
        self.vendorSheet['List']=self.vendorSheet['List'].replace(to_replace='[^0-9][^.][^0-9]', value='', regex=True)
        self.vendorSheet['Cost']=self.vendorSheet['Cost'].replace(to_replace='[^0-9][^.][^0-9]', value='', regex=True)
        self.vendorSheet['Multiplier']=self.vendorSheet['Multiplier'].replace(to_replace='[^0-9][^.][^0-9]', value='', regex=True)
        self.vendorSheet.fillna(value=0)
        

        self.vendorSheet['Multiplier']=self.vendorSheet['Multiplier'].astype(float)
        self.vendorSheet['List']=self.vendorSheet['List'].astype(float)
        self.vendorSheet['Cost']=self.vendorSheet['Cost'].astype(float)

    def getMult(self):
        fields = ['Part', 'Rate']
        self.multSheet=pd.read_csv(askopenfilename(), usecols=fields)
        self.multSheet['Rate']=self.multSheet['Rate'].astype(float)

    def Download(self):
 
        messagebox.showinfo("TOUCH NOTHING!", "Data is processing. Another box will tell you when to continue.")
        index=0
        projectArg={'api_key':self.input_APIKEY.get(), 'format':'json'}

        for item in self.projectsToGet:
            #url='https://www.parsehub.com/api/v2/runs/' + str(self.projectsToGet[index]) + '/data'
            #self.data_dict.append(json.loads(requests.get(url,params=projectArg).text)['selection2'])
            url='https://www.parsehub.com/api/v2/runs/' + str(self.projectsToGet[index]) + '/data?'+ 'api_key=' + self.input_APIKEY.get() + "&format=csv"
            try:
                self.data_dict.append(pd.read_csv(url))
                self.data_dict[index].columns = self.data_dict[index].columns.str.replace('^.*\_', '')
                #self.data_dict[index]['competitor'] = self.data_dict[index]['competitor'].astype(object)
                tempname=self.data_dict[index]['Competitor'][0] +"_RMultiplier"
                self.data_dict[index][tempname]="=C2/Procure Cost"
            except:
                #errorTxt=str("Crawler " + self.projectsToGet[index] + " failed.")
                #messagebox.showinfo("Error", errorTxt)
                for item in self.xp:
                    if(item['last_run']['run_token'] == self.projectsToGet[index]):
                        print(item['title'] + " has failed." + " Downlaoded status: " + item['last_ready_run']['status'])

            index+=1
        #print(self.data_dict[0])
        index=0
        self.assembled = self.data_dict[0]
        for data in self.data_dict:
            try:
                self.assembled= pd.merge(self.assembled, self.data_dict[index], on="Part", how="outer")
                #self.assembled = functools.reduce(lambda left, right: pd.merge(left, right, on="Part", how="outer"), self.data_dict[index])
            except:
                #print("ERROR Occured " + str(self.projectsToGet[index]))
                pass
            index+=1

        messagebox.showinfo("All Clear", "Data Processing Complete. Close these dialogs and continue.")


    def applyCost(self):
        try:
            self.assembled = pd.merge(self.assembled, self.multSheet, on="Part")
            self.assembled= pd.merge(self.assembled, self.vendorSheet, on="Part")
        except:
            self.assembled= pd.merge(self.assembled, self.vendorSheet, on="Part")
            
        self.assembled['Multiplier'].fillna(float(self.input_Multiplier.get()))
        self.assembled['Cost'].fillna(self.assembled['List']*self.assembled['Multiplier'])
        self.assembled['Sell']="=D2*$D$1"
        #self.assembled['Cost']=self.assembled['List']*self.assembled['Multiplier']

        print(self.assembled)

    def export(self):
        self.assembled.to_csv(self.dirName + "/Analysis.csv")
        index = 0
        time = datetime.datetime.now()
        for item in self.data_dict:
            try:
                self.data_dict[index].to_csv(self.dirName + "/" + self.data_dict[index]['Competitor'][0] + "_ %d" + now.month + "-%d" + now.day + "-%d" + now.year + ".csv")
            except:
                self.data_dict[index].to_csv(self.dirName + "/" + "ErroredSheet_" + str(index) + ".csv")
            index +=1





root = Tk()
mainApp = App(root)
root.mainloop()