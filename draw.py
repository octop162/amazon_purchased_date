import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 読み込み
df = pd.read_csv('created_dates.txt', header=None)
datetimes = pd.to_datetime(df[0], unit='ms')

# 時刻情報だけのデータに変換
times = datetimes.dt.time
times = pd.DataFrame(pd.to_datetime(times, format='%H:%M:%S', utc=True))
times.set_index(0, inplace=True)
times.index = times.index.tz_convert('Asia/Tokyo')
times[1] = 0
times = times.rename(columns={1: 'count'}, index={0: 'date'})
group = times.groupby(pd.Grouper(freq='60min')).count()

# 曜日のデータに変換
weeks = pd.DataFrame(pd.to_datetime(datetimes, utc=True)).set_index(0)
weeks.index = weeks.index.tz_convert('Asia/Tokyo')
weekdays = weeks.index.weekday
weekdays = pd.DataFrame(weekdays)
weekdays[1] = 1

# 可視化
fig = plt.figure(figsize=(20,10))
## 時間帯
x = group.index.strftime("%H:%M:%S")
y = group
ax = fig.add_subplot(2,1,1)
ax.bar(x, group['count'], color="brown", align="center")
ax.set_title('Every Hour')
ax.set_xticks(x)
ax.set_yticks(np.arange(0, y.max().item() ))

## 曜日
x = ["Sun","Mon","Tue","Wed","Thr","Fri","Sat"]
y = weekdays.groupby(0).count()[1]
ax2 = fig.add_subplot(2,1,2)
ax2.bar(x, y, color="green", align="center")
ax2.set_title('Every Date')
ax2.set_xticks(x)
ax2.set_yticks(np.arange(0, y.max() ))

fig.savefig("figure.png")