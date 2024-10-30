import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import numpy as np
import os


#if os.path.exists('inti_mes.png'):
#    os.remove('inti_mes.png')

today = dt.datetime.now()
month_ago = dt.datetime.now() - dt.timedelta(days = 30)
today_date = today.date()
ma_date = month_ago.date()
x0 = today.replace(hour = 6, minute=0, second=0, microsecond=0)
xf = today.replace(hour = 18, minute=0, second=0, microsecond=0)

df = pd.read_csv('intiuv_data.csv', skiprows=2, header = None)
df.columns = ['datetime','count','iuv']
df['datetime'] = pd.to_datetime(df.datetime, format = '%d/%m/%Y %H:%M')
df['date'] = df.datetime.dt.date
month_data = df[(df.date <= today_date) & (df.date >= ma_date)]


levels = [0,3,6,8,11,20]
colors = ['green','yellow','orange','red','blueviolet']
cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(levels, cmap.N)


month_data = month_data.resample('1h', on ='datetime')[['iuv']].mean().reset_index()
month_data = month_data[(month_data.datetime.dt.hour >= 6) & (month_data.datetime.dt.hour <= 18)]
lst_days = list(month_data.datetime.dt.date.unique())
print(len(month_data), len(lst_days))

month_data['day'] = month_data.datetime.dt.date
month_data['hrs'] = month_data.datetime.dt.hour - 6

arr = np.full((len(lst_days),13), np.nan)
for n,k in enumerate(lst_days):
    aux = month_data[month_data.day == k]
    for v,iu in zip(aux.hrs.to_list(), aux.iuv.to_list()):
        arr[n,v] = iu

ticks_cbar = [1.5,4.5,7,9.5,15.5]
lab_cbar = ['Bajo','Moderado','Alto','Muy Alto','Extremo']

lst_daysx = list(month_data.datetime.dt.day.unique())
#aa = [lst_days[i].day for i in range(0,len(lst_daysx),3)]
bb = [f'{lst_days[i].day}\n{dt.datetime.strftime(dt.datetime(2000,lst_days[i].month,1),"%b")}' for i in range(0,len(lst_daysx)+1,3)]
orgs = np.arange(0,31,3)

fig, ax = plt.subplots(figsize=(18,8))
plt.subplots_adjust(bottom=.02, top=.94, left=0.05, right=0.98)
msh = ax.pcolormesh(arr.T, cmap = cmap, norm = norm)
ax.invert_yaxis()
#cbar = fig.colorbar(msh, ticks=[int(i) for i in levels])
cbar = fig.colorbar(msh, orientation='horizontal',ticks=ticks_cbar, shrink=.4,fraction=0.1, pad=0.12)
cbar.set_label(label='Índice Ultravioleta', size=14)
cbar.ax.set_xticklabels(lab_cbar, fontsize=13)
ax.xaxis.set_minor_locator(mdates.DayLocator(interval=1))
ax.set_yticks(ticks=np.arange(0,13,1),labels=np.arange(6,19,1), fontsize=12)
ax.set_xticks(ticks=orgs, labels=bb, fontsize=12)
ax.grid(which='both')
ax.set_ylabel('Hora Local', fontsize=13)
ax.set_title('Índice Ultravioleta Cota Cota', fontsize=15)
fig.savefig('inti_mes.png', dpi = 300)
print('Figura matriz generada')
