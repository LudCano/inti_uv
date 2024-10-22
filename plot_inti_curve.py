import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as tck
import numpy as np
import matplotlib.image as mpimg
import os

today = dt.datetime.now()
today_date = today.date()
x0 = today.replace(hour = 6, minute=0, second=0, microsecond=0)
xf = today.replace(hour = 18, minute=0, second=0, microsecond=0)

df = pd.read_csv('intiuv_data.csv', skiprows=2, header = None)
df.columns = ['datetime','count','iuv']
df['datetime'] = pd.to_datetime(df.datetime, format = '%d/%m/%Y %H:%M')
df['date'] = df.datetime.dt.date
today_data = df[df.date == today_date]

lims = [0,4,6.5,9,13,20]
lims = [0,3,6,8,11,20]
clrs = ['green','yellow','orange','red','blueviolet']

if os.path.exists('inti_plot.png'):
    os.remove('inti_plot.png')

fig, ax = plt.subplots()
ax.plot(today_data.datetime, today_data.iuv, c = 'k')
ax.set_xlim(x0, xf)
ax.set_ylim(0,20)
ax.set_yticks(np.arange(0,21,5))
ax.yaxis.set_minor_locator(tck.MultipleLocator(1))
ax.grid(which='minor', alpha = .35)
ax.grid(which='major', alpha = .2, c = 'k')
for i in range(len(lims)-1):
    ax.fill_between([x0,xf],lims[i],lims[i+1], color = clrs[i], alpha = 0.35)
ax.xaxis.set_major_locator(mdates.HourLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
ax.set_xlabel('Hora Local')
ax.set_ylabel('Índice Ultravioleta')
ax.set_title(f'Indice UV Cota Cota {dt.datetime.strftime(today, "%d %b %Y")}')
ax.axhline(16, ls = '--', c = 'k', alpha = .35)


img = mpimg.imread('logo-lfa-original.png') 
x0im = x0 + dt.timedelta(hours = 2.4)
xfim = xf + dt.timedelta(hours = -2.4)
plt.imshow(img, extent=[x0im,xfim, 2, 18], aspect='auto', alpha=0.15)
fig.savefig('inti_plot.png',dpi=300)
plt.show()


