#!/usr/bin/python
#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit

def makeplot(df, dmax, trange, c, ylim=False):
    # add column elapsed days
    d = []
    for r in df['date']:
        d.append((r - df['date'][df.index[0]]).days)
    df['days'] = d
    
    # number of infected individuals during the early stages of an SIR outbreak
    # https://kingaa.github.io/clim-dis/parest/parest.html
    def i(t, i0, a):
        return i0 * np.exp(a*t)

    fig, ax = plt.subplots()

    ax.plot(df['days'], df['total'], 'bo', label='observed cases')
    ax.legend()

    t = np.arange(0, dmax)
    for n in trange:
        j = df.index[0]
        while df['days'][j] < n:
            j += 1
        df_test = df.head(j)
        popt, pcov = curve_fit(i, df_test['days'], df_test['total'])
        if n > trange[-2]:
            symbol = '-'
        else:
            symbol = '--'
        ax.plot(t, i(t, popt[0], popt[1]), symbol, label='regression using timeframe [0:{}]'.format(n))
        ax.legend()

    ax.set(title = 'Impact of Epidemiological Measures (COVID-19 {})\n(early stage SIR exponential model, calculated on {:%Y-%m-%d})'.format(c, df['date'][df.index[-1]]))
    ax.set(xlabel = 'days passed since outbreak ({:%Y-%m-%d})'.format(df['date'][df.index[0]]))
    ax.set(ylabel = 'total number of infected individuals')
    ax.axvline(x=trange[-1], color='r', ls=':')
    
    if ylim:
        plt.ylim(ylim)
    plt.grid()
    return plt

def atoi(x):
    return int(re.sub("\D", "", x.encode('ascii', errors='ignore').decode()))

if __name__ == "__main__":
    # fill up dataframe with observarions
    # https://hu.wikipedia.org/wiki/2020-as_COVID-19_koronav%C3%ADrus-j%C3%A1rv%C3%A1ny_Magyarorsz%C3%A1gon
    # https://koronavirus.gov.hu/
    
    df = pd.read_csv('data-hun.csv', sep=';', names=['date', 'infectious', 'died', 'recovered', 'total', 'remark'], parse_dates=['date'])
    p = makeplot(df, dmax=23, trange=[6, 11, 16, 22], c="Hungary", ylim=(0,300))
    p.savefig('plot-hun.png', dpi=150)
    p.show()
    p1 = makeplot(df, dmax=30, trange=[6, 11, 16, 22], c="Hungary")
    p1.savefig('plot-hun-large.png', dpi=200)
    p1.show()

    # https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Spain
    df2 = pd.read_csv('data-spain.csv', sep=';', names=['date', 'time', 'AN','AR', 'AS', 'IB', 'CN', 'CB', 'CM', 'CL', 'CT', 'CE', 'VC', 'EX', 'GA', 'MD', 'ML', 'MU', 'NA', 'PV', 'RI', 'i_new', 'total', 'd_new', 'died', 'ICU', 'recovered', 'tested', 'refs'], parse_dates=['date'], converters={"total": atoi})
    makeplot(df2, dmax=35, trange=range(9, 30, 10), c="Spain", ylim=(0, 80000)).show()
    
