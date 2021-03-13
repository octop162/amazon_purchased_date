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

# 1時間ごとにグルーピング
group = times.groupby(pd.Grouper(freq='60min')).count()

# 可視化
fig = plt.figure(figsize=(20,5))
ax = fig.add_subplot(1,1,1)
ax.plot(group)
ax.set(title='Purchase')
fig.savefig('figure.png')