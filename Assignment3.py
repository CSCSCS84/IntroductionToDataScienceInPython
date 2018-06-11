import pandas as pd
import numpy as np
import re

energy = pd.DataFrame()
gpd = pd.DataFrame()
ScimEn = pd.DataFrame()


def answer_one():
    columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy = pd.read_excel('Energy Indicators.xls', skiprows=17, header=0, usecols=[2, 3, 4, 5], skipfooter=38,
                           names=columns)

    energy = energy.replace(['\s*\(.*\)'], [''], regex=True)
    energy = energy.replace(['[0-9]*'], [''], regex=True)

    energy = energy.set_index('Country')
    energy.rename(index={'Republic of Korea': 'South Korea'}, inplace=True)
    energy.rename(index={'United States of America': 'United States'}, inplace=True)
    energy.rename(index={'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom'}, inplace=True)
    energy.rename(index={'"China, Hong Kong Special Administrative Region"': 'Hong Kong'}, inplace=True)

    energy = energy.replace(['...'], [np.NaN], regex=True)
    energy.astype(dtype={'Energy Supply': float, 'Energy Supply per Capita': float, '% Renewable': float},
                  errors='raise', copy=False)

    energy['Energy Supply'] = energy['Energy Supply'].multiply(1000000)

    gpd = pd.read_csv('world_bank.csv', skiprows=4, header=0)

    gpd = gpd.set_index('Country Name')
    gpd.rename(index={"Korea, Rep.": 'South Korea'}, inplace=True)
    gpd.rename(index={"Iran, Islamic Rep.": "Iran"}, inplace=True)
    gpd.rename(index={"Hong Kong SAR, China": "Hong Kong"}, inplace=True)

    ScimEn = pd.read_excel('scimagojr-3.xlsx', header=0)
    ScimEn = ScimEn.set_index('Country')

    gpdMergeRows = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    result = pd.merge(energy, gpd[gpdMergeRows], how='inner', left_index=True, right_index=True)
    result = pd.merge(result, ScimEn, how='inner', left_index=True, right_index=True)

    result.index.names = ['Country']
    return result.sort_values(by='Rank', ascending=True).head(15)


def answer_three():
    data = answer_one()
    years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    avgGDP = data[years].mean(axis=1)
    avgGDP.sort_values(ascending=False, inplace=True)
    return avgGDP


def answer_four():
    Top15 = answer_three()
    data = answer_one()
    country = Top15.index[5]
    return data.at[country, '2015'] - data.at[country, '2006']


def answer_five():
    data = answer_one()
    mean = data['Energy Supply per Capita'].mean()
    return mean


def answer_six():
    Top15 = answer_one()
    maxCountry = Top15['% Renewable'].idxmax()
    return (maxCountry, Top15.loc[maxCountry]['% Renewable'])


def answer_seven():
    Top15 = answer_one()
    Top15['Citations ratio'] = Top15['Self-citations'] / Top15['Citations']
    maxCountry = Top15['Citations ratio'].idxmax()
    return (maxCountry, Top15.loc[maxCountry]['Citations ratio'])


def answer_eight():
    Top15 = answer_one()
    Top15['Population'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15 = Top15.sort_values(by='Population', ascending=False)
    return Top15.index[2]


def answer_nine():
    Top15 = answer_one()
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']
    Top15['Citable docs per Capita'] = Top15['Citable documents'] / Top15['PopEst']
    corr = Top15['Citable docs per Capita'].corr(Top15['Energy Supply per Capita'])
    return corr


def answer_ten():
    Top15 = answer_one()
    median = Top15['% Renewable'].median()
    Top15['HighRenew'] = [1 if x >= median else 0 for x in Top15['% Renewable']]
    return Top15['HighRenew']


def answer_eleven():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply'] / Top15['Energy Supply per Capita']).astype(float)
    ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'}
    groups = Top15.groupby(ContinentDict)
    avg = groups['PopEst'].agg({'size': np.size,
                                'sum': np.sum,
                                'mean': np.mean,
                                'std': np.std
                                })

    avg.index.names = ['Continent']
    return avg

def answer_twelve():
    Top15 = answer_one()
    ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'}
    Top15['Continent'] = [ContinentDict[country] for country in Top15.index]
    Top15['bins']=pd.cut(Top15['% Renewable'],5)
    return Top15.groupby(['Continent', 'bins']).size()

def answer_thirteen():
    Top15 = answer_one()
    Top15['PopEst'] = (Top15['Energy Supply'] / Top15['Energy Supply per Capita']).astype(float)
    Top15['PopEst'] = Top15.apply(lambda x: "{:,}".format(x['PopEst']), axis=1)

    return Top15['PopEst']

print(answer_thirteen())

# print(answer_one())
# print(answer_three())
