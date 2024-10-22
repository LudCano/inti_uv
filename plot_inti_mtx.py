import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import numpy as np

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

levels = [0,4,6.5,9,13,20]
colors = ['green','yellow','orange','red','purple']
cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(levels, cmap.N)


month_data = month_data.resample('5min', on ='datetime')[['iuv']].mean().reset_index()
month_data = month_data[(month_data.datetime.dt.hour >= 6) & (month_data.datetime.dt.hour <= 18)]
month_data['mns'] = (month_data.datetime.dt.hour*60 + month_data.datetime.dt.minute)//5 - 72
month_data['day'] = month_data.datetime.dt.date

lst_days = list(month_data.datetime.dt.date.unique())
arr = np.full((len(lst_days),156), np.nan)
for n,k in enumerate(lst_days):
    aux = month_data[month_data.day == k]
    for v,iu in zip(aux.mns.to_list(), aux.iuv.to_list()):
        arr[n,v] = iu


lst_daysx = list(month_data.datetime.dt.day.unique())
#aa = [lst_days[i].day for i in range(0,len(lst_daysx),3)]
bb = [f'{lst_days[i].day}\n{dt.datetime.strftime(dt.datetime(2000,lst_days[i].month,1),"%b")}' for i in range(0,len(lst_daysx),3)]
orgs = np.arange(0,30,3)
print(len(bb), len(orgs))

fig, ax = plt.subplots()
msh = ax.pcolormesh(arr.T, cmap = cmap, norm = norm)
ax.invert_yaxis()
cbar = fig.colorbar(msh, ticks=levels)
ax.set_yticks(ticks=np.arange(0,156,12),labels=np.arange(6,19,1))
ax.set_xticks(ticks=orgs, labels=bb)
ax.grid()
#cbar.ax.set_yticklabels(['0-2', '2-6', '6-15'])  # Etiquetas para la barra de color
plt.show()