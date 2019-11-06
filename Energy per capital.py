# -*- coding: utf-8 -*-

################################################################################################
#                                                                                              #
#                                      Python final project                                    #
#                                                                                              #
#                                        Reza Tavasoli                                         #
#                                                                                              #
################################################################################################



import numpy as np
import pandas as pd
import os
from decimal import Decimal
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt

os.chdir(r"...\Desktop\Python_Final_Project")
os.getcwd()

'''
Q1) [Advance]
a) Read the energy data from the file Energy Indicators.xls, 
which is a list of indicators of [energy supply and renewable electricity production] 
from the [United Nations]
 (http://unstats.un.org/unsd/environment/excel_file_tables/2013/Energy%20Indicators.xls)
 for the year 2013, and should be put into a Data Frame with the variable name of energy.
 Keep in mind that this is an Excel file, and not a comma separated values file. Also,
 make sure to exclude the footer and header information from the data file.
 The first two columns are unnecessary, so you should get rid of them,
 and you should change the column labels so that the columns are:
 
['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable]
'''



Energy= pd.read_excel('EnergyIndicators.xls',                   
             header=None,skiprows=18,
             skip_footer=(38),
             usecols=[2,3,4,5],
             names=['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'])
Energy.to_excel('Energy.xlsx')
#Energy.head()


'''
b) Rename the following list of countries. 

"Republic of Korea" to "South Korea",
"United States of America" to "United States",
"United Kingdom of Great Britain and Northern Ireland" to "United Kingdom",
"China, Hong Kong Special Administrative Region" to "Hong Kong"
 
There are also several countries with parenthesis in their name. Be sure to remove these,
 e.g. `'Bolivia (Plurinational State of)'` should be `'Bolivia'`. '''


#for removing index numbers from the end of country names
Energy.Country=Energy.Country.str.replace('\d+','')

change_name={"Republic of Korea" : "South Korea",
     "United States of America" : "United States",
     "United Kingdom of Great Britain and Northern Ireland" : "United Kingdom",
     "China, Hong Kong Special Administrative Region" : "Hong Kong"}

Energy['Country']=Energy.replace({'Country':change_name})
#energy['Country']=energy["Country"].replace(dic,inplace=True)

#for removing parentheses
Energy['Country']=Energy['Country'].str.replace(r"\(.*\)","")

#for space removal from the end of the country names
Energy['Country'] = Energy['Country'].str.replace(r"\(.*\)","").str.strip()

Energy.to_excel('Energy_modified.xlsx')
'''
c) Next, load the GDP data from the file world_bank.csv, which is a csv containing countries
' GDP from 1960 to 2015 from [World Bank] (http://data.worldbank.org/indicator/NY.GDP.MKTP.CD). 
Call this Data Frame GDP. Make sure to skip the header, and rename the following list of countries:
"Korea, Rep." to "South Korea", 
"Iran, Islamic Rep." to "Iran",
"Hong Kong SAR, China" to "Hong Kong"  '''


GDP=pd.read_csv("world_bank.csv",skiprows=4)

change_name1={"Korea, Rep." : "South Korea", 
      "Iran, Islamic Rep." : "Iran",
      "Hong Kong SAR, China" : "Hong Kong"}

GDP['Country Name']=GDP.replace({'Country Name':change_name1})


'''
d) Finally,
    load the [Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology]
    (http://www.scimagojr.com/countryrank.php?category=2102) from the file scimagojr-3.xlsx,
    which ranks countries based on their journal contributions in the aforementioned area.
    Call this Data Frame ScimEn.
'''
ScimEn=pd.read_excel('scimagojr-3.xlsx')

'''
e) Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of 
 country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries 
 by Scimagojr 'Rank' (Rank 1 through 15). The index of this Data Frame should be the name of the country,
 and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
 'Citations per document', 'H index', 'Energy Supply','Energy Supply per Capita', '% Renewable', '2006',
 '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].
  You should finally get a Data Frame with 20 columns and 15 entries.
'''


GDP=GDP[['Country Name','2006', '2007', '2008', '2009','2010','2011','2012','2013','2014','2015']]

ScimEn1=ScimEn.loc[ScimEn['Rank']<16]

df1=pd.merge(Energy,ScimEn1,on='Country')
df2=pd.merge(df1,GDP,left_on='Country',right_on='Country Name',how='inner')

df2=df2.set_index(['Country'])

df=df2.drop(['Country Name'],axis=1)

df.to_excel('df.xlsx')

'''
Q2) [Moderate] What are the top 15 countries for average GDP over the last 10 years?
    [NB: This function should return a Series named ‘avgGDP’ with 15 countries and their
    average GDP sorted in descending order.]
'''
def answer_2():    
    avgGDP = df[['2006','2007','2008','2009','2010','2011',
                 '2012','2013','2014','2015']].mean(axis = 1).rename('avgGDP').sort_values(ascending= False)      
    #avgGDP=pd.Series(avgGDP)
    return avgGDP

answer_2()


'''
Q3) [Moderate] By how much had the GDP changed over the 10 year span for the country 
    with the 6th largest average GDP? [NB: This function should return a single number.]
'''
def answer_3():
    sixth_delta=df.loc['United Kingdom','2015']-df.loc['United Kingdom','2006']
    sixth_delta="{:.2E}".format(Decimal(sixth_delta))
    return sixth_delta
    
answer_3()

'''
Q4) [Trivial] What is the mean energy supply per capita? [NB: 
    This function should return a single number.]

'''
def answer_4():
    mean_energy=df['Energy Supply per Capita'].mean()
#    df.loc[:,'Energy Supply per Capita'].mean()
    return mean_energy
answer_4()


'''
Q5) [Trivial] Which country has the maximum % Renewable and what is the percentage?
[NB: This function should return a tuple with the name of the country and the percentage.]

'''
def answer_5():
    Renewable_max=df['% Renewable'].max()
    i= df.index[df["% Renewable"]== Renewable_max][0]
#   df.loc[(df['% Renewable']==df['% Renewable'].max()),'Rank']
    return (i,Renewable_max)
answer_5()

'''
Q6) [Trivial] Create a new column that is the ratio of Self-Citations to Total Citations.
    What is the maximum value for this new column, and which country has the highest ratio?
    [NB: This function should return a tuple with the name of the country and the ratio.]
'''
def answer_6():
    df['Ratio']=df['Self-citations']/df['Citations']
    df.to_excel('df.xlsx')   
    max_ratio=df['Ratio'].max()
    max_ratio="{:.2E}".format(Decimal(max_ratio))
    df.loc[(df['Ratio']==df['Ratio'].max()),'Rank']
    return('China',max_ratio) 
answer_6()

'''
Q7) [Moderate] Create a column that estimates the population using Energy Supply and
    Energy Supply per capita. What is the third most populous country according to this estimate?
    [NB: This function should return a single string value.]
'''
def answer_7():
    df["pop"] = round(df["Energy Supply"] / df["Energy Supply per Capita"])
    nlarge = df["pop"].nlargest(3)
    i = df.index[df["pop"] == nlarge.min()][0]
    return i

print(answer_7()) #Brazil

'''
Q8) [Moderate] Create a column that estimates the number of citable documents per person.
    What is the correlation between the number of citable documents per capita and the energy
    supply per capita? Use the “.corr()” method, (Pearson's correlation). 
    [NB: This function should return a single number.] Plot to visualize the relationship between
    Energy Supply per Capita vs. Citable docs per Capita.
'''

def answer_8():
    df['Citable docs per Capita']=df['Citable documents']/df['pop']
    from scipy.stats.stats import pearsonr
    docs_col = df['Citable docs per Capita'].values
    energy_col = df['Energy Supply per Capita'].values
    corr , _ = pearsonr(docs_col, energy_col)
    corr="{:.2E}".format(Decimal(corr))
    return corr
answer_8()
df.to_excel('df.xlsx') 


plt.scatter(df['Citable docs per Capita'],df['Energy Supply per Capita'],c='b',marker='o')

plt.xlabel('Citable docs per Capita', fontsize=10)
plt.ylabel('Energy Supply per Capita', fontsize=10)

plt.title('scatter plot - Citable docs per Capita vs Energy Supply per Capita',fontsize=12)
plt.show()



#df[['Citable docs per Capita','Energy Supply per Capita']].corr(method='pearson')

'''
Q9) [Moderate] Create a new column with a 1 if the country's % Renewable value is at or above 
    the median for all countries in the top 15, and a 0 if the country's % Renewable value is 
    below the median. [NB: This function should return a series named “HighRenew” whose index 
    is the country name sorted in ascending order of rank.]
'''
#Get column index from column name in 
index_Renewable=df.columns.get_loc("% Renewable")

df=df.sort_values('Rank')

def answer_9():
    med = df.iloc[:,index_Renewable].median()
    df['HighRenew']  = None
    index_HighRenew=df.columns.get_loc("HighRenew")
    for i in range(len(df)):
        if df.iloc[i,index_Renewable] > med:
            df.iloc[i,23] = 1
        else:
            df.iloc[i,23] = 0       
    return pd.Series(df['HighRenew'])
answer_9()

df.to_excel('df.xlsx')

'''
Q10) [Advanced] Use the following dictionary to group the Countries by Continent,
    then create a dataframe that displays the sample size (the number of countries
    in each continent bin), and the sum, mean, and std deviation for 
    the estimated population of each continent.
    
 ContinentDict  = {'China':'Asia', 
                   'United States':'North America', 
                   'Japan':'Asia', 
                   'United Kingdom':'Europe', 
                   'Russian Federation':'Europe', 
                   'Canada':'North America', 
                   'Germany':'Europe', 
                   'India':'Asia',
                   'France':'Europe', 
                   'South Korea':'Asia', 
                   'Italy':'Europe', 
                   'Spain':'Europe', 
                   'Iran':'Asia',
                   'Australia':'Australia', 
                   'Brazil':'South America'}
[NB: This function should return a DataFrame with index named Continent ['Asia', 'Australia',
  'Europe', 'North America', 'South America'] and with columns ['size', 'sum', 'mean', 'std'].]
''''


ContinentDict  = {'China':'Asia', 
                   'United States':'North America', 
                   'Japan':'Asia', 
                   'United Kingdom':'Europe', 
                   'Russian Federation':'Europe', 
                   'Canada':'North America', 
                   'Germany':'Europe', 
                   'India':'Asia',
                   'France':'Europe', 
                   'South Korea':'Asia', 
                   'Italy':'Europe', 
                   'Spain':'Europe', 
                   'Iran':'Asia',
                   'Australia':'Australia', 
                   'Brazil':'South America'}

def answer_10():
    groups = pd.DataFrame(columns = ['size', 'sum', 'mean', 'std'])
    
    for group, frame in df.groupby(ContinentDict):
        groups.loc[group] = [len(frame), frame['pop'].sum(),frame['pop'].mean(),frame['pop'].std()]
    return groups

answer_10()

'''
def answer_10():
    df["Continent"] = pd.Series(ContinentDict)
    contin = df.groupby("Continent")["pop"].agg(['count', 'sum', 
                           'mean', 'std']).rename(columns={'count': 'size'})
    return contin
    
answer_10
'''  

############################################################################################

