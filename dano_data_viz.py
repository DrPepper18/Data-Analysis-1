import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.basemap import Basemap
import plotly.graph_objects as go
import seaborn as sns

data = pd.read_excel('DANO_viz_data.xlsx')
'''
#Процент прибыли с разных сегментов покупателей
con = data[data['Segment'] == 'Consumer']['Profit'].sum()
corp = data[data['Segment'] == 'Corporate']['Profit'].sum()
home = data[data['Segment'] == 'Home Office']['Profit'].sum()
y = [con, corp, home]
explode = (0.05, 0.05, 0.05)
plt.pie(y, 
        labels = ['Consumer', 'Corporate', 'Home Office'], 
        explode = explode,
        autopct = '%1.1f%%', 
        pctdistance = 0.85,
        startangle = 90, 
        colors = ['#9970B6', '#FFFB94', '#FC893F'], 
        shadow = True)
centre_circle = plt.Circle((0,0),0.60,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('Процент прибыли от каждого сегмента покупателей')
plt.legend()
plt.show()
''''''
#Прибыль с каждой категории товаров
category = data.Category.unique()
profit = [data[data['Category'] == category[i]]['Profit'].sum() for i in range(len(category))]
sales = [data[data['Category'] == category[i]]['Sales'].sum() for i in range(len(category))]
plt.style.use('ggplot')
plt.bar(category, profit, color = '#9970B6')
for i in range(len(category)):
    plt.text(i, profit[i], str(round((profit[i]/sales[i])*100, 2))+'% от дохода', ha = 'center', Bbox = dict(facecolor = '#FF7171', alpha =.8))
plt.title('Прибыль от каждой категории')
plt.show()
''''''
#Прибыль с каждого штата
regions = data.State.unique()
profit = []
for i in regions:
    profit += [[i,data[data['State'] == i]['Profit'].sum()]]
profit = sorted(profit, key = lambda x: x[1], reverse = True)
profit = profit[:5]+profit[-5:]
regions = [profit[i][0] for i in range(len(profit))]
profit = [profit[i][1] for i in range(len(profit))]
color = []
for i in profit:
    if i > 0:
        color += ['#9970B6']
    else:
        color += ['#FC893F']
plt.style.use('ggplot')
plt.bar(regions, profit, color = color)
plt.xticks(rotation=60, fontsize = 'small', horizontalalignment = 'right')
plt.legend(title = 'Топ-5 самых прибыльных/неприбыльных штатов')
plt.grid(True)
plt.show()
''''''
regions = data.State.unique()
profit = []
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')
df = pd.DataFrame(
{
    'state': list(df['state']),
    'code': list(df['code']),
    'profit': [0]*len(df['code'])
})
for i in regions:
    profit += [[i,data[data['State'] == i]['Profit'].sum()]]
for i in range(len(profit)):
    df['profit'][df['state'] == profit[i][0]] = profit[i][1]
    
#colorscale = ["rgb(230, 51, 51)", "rgb(255, 255, 150)", "rgb(94, 179, 39)", "rgb(67, 136, 33)", "rgb(33, 74, 12)"]
#colorscale = ['rgb(120,0,120)', 'rgb(255,255,0)', 'rgb(255,100,0)', 'rgb(255,50,0)', 'rgb(255,0,0)']
colorscale = ['#FC893F', '#FFFB94', '#E0CEED', '#C59DE2', '#9970B6']
fig = go.Figure(data=go.Choropleth(
    locations=df['code'], # Spatial coordinates
    z = df['profit'].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale=colorscale,
    colorbar_title = "Profit, USD",
))
fig.update_layout(
    title_text = 'Profit from every state',
    geo_scope='usa', # limite map scope to USA
)
fig.show()
'''
sales = data['Sales'].sum()
profit = data['Profit'].sum()
explode = (0, 0.1)
plt.pie([sales-profit, profit], 
        labels = ['Расходы', 'Прибыль'], 
        autopct = '%1.1f%%', 
        startangle = 75, 
        colors = ['#C8BFE7', '#FFC90E'],
        explode = explode,
        shadow = True)
plt.title('Итог: отношение прибыли к расходам')
plt.legend(loc = 'lower right')
plt.show()
'''
print(data[data['Profit'] < 0].head(20))
x = data['Profit']
y = data['Discount']
#plt.style.use('ggplot')
plt.scatter(x,y)
z = np.polyfit (x, y, 1)
p = np.poly1d (z)
plt.plot (x, p(x), color = 'grey')
plt.show()
''''''
subcategory = data['Sub-Category'].unique()
profit = [data['Profit'][data['Sub-Category'] == i].sum() for i in subcategory]
profit = [profit[i]/(data['Sales'][data['Sub-Category'] == subcategory[i]].sum()-profit[i]) for i in range(len(profit))]
profit = [[subcategory[i], profit[i]] for i in range(len(subcategory))]
profit.sort(key = lambda x: x[1])
for i in profit:
    plt.bar([i[0]], [i[1]], color = 'purple')
plt.xticks(rotation=90)
plt.show()
'''