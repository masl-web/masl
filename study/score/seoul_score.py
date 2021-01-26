# -*- coding: utf-8 -*-
"""seoul_score.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hqlCaD8hLrBk67LA-ZfxV-L3ocTuMvw5
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

km = pd.read_csv('/content/drive/My Drive/elice_miniProject/seoul_500m.csv')

df = pd.read_csv('/content/drive/My Drive/elice_miniProject/seveneleven_seoul.csv')
df.columns = ['지점명','지점주소','x','y']
df = df.sort_values('y',ascending=True)
df = df.reset_index(drop=True, inplace=False)
df

a = km['seven11']

#km = km.sort_values('bottom_left_y',ascending=True)

# km['seven11']=0
# km['gs25']=0
# km['olive0']=0
# km['mcdonalds']=0

km

## 매장 좌표가 1구획의 좌하단 and 우상단 좌표 내에 포함되어 있으면 +1 
def score(df,km,a):
  for i in range(len(km['bottom_left_x'])):
    for j in range(len(df['x'])):
      if km['bottom_left_x'][i] <= df['x'][j] and km['bottom_left_y'][i] <= df['y'][j] and km['top_right_x'][i] > df['x'][j] and km['top_right_y'][i] > df['y'][j]:
        a[i] = a[i] + 1

## 범위 내에 들어온 매장 수 합계
  n=0
  for c in range(len(a)):
    if a[c] > 0:
      n = n + a[c]
  print('total:',n)

  return km

score(df,km,a)

km.to_csv('/content/drive/My Drive/elice_miniProject/seoul_score.csv',index=False,encoding='utf-8')

[km['bottom_left_y'][0],km['bottom_left_x'][0]]

