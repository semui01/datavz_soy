#  import libraries
import pandas as pd
import numpy as np
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#  ------------------------------------------- from csv to dataframe--------------------------#
# import chardet python character encoding detector
import chardet
with open('soybean.csv', 'rb') as rawdf:
    result = chardet.detect(rawdf.read())
print(result)

# read csv file
df = pd.read_csv('soybean.csv',encoding = "SHIFT_JIS")
df.info()
print(df)

#  ------------------------------------------- Images process--------------------------#
# Opening the image
# (R prefixed to string in order to deal with '\' in paths)
image = Image.open("soy.jpg")

# Blurring image by sending the ImageFilter.
# GaussianBlur predefined kernel argument /adjust radius value to change the blurness
image = image.filter(ImageFilter.GaussianBlur(radius=2))

# save image in png format
image.save('output1.png')

# Displaying the image
image.show()  # not working in colab
# image  or # display(image)  # both working

#  ------------------------------------------- Data cleaning--------------------------#

# convert row as new header
new_header = df.iloc[10]
df_clean = pd.DataFrame(df.values[11:], columns=new_header)
df_clean['年度'] = df_clean['年度'].loc[:].str.strip('年度')

print(df_clean)

# convert strings to float type
df_clean = df_clean.replace('-', '0', regex=True)
df_clean = df_clean.replace(',', '', regex=True)
for x in df_clean.columns[1:]:
    df_clean[x] = df_clean[x].astype('float')

df_clean.info()

#  ------------------------------------------- Data visualisation--------------------------#
# Open the image from local path
im = Image.open('output1.png')

fig = go.Figure(
    data=[
        go.Scatter(
            name="Local consumption",
            x=df_clean["年度"],
            y=df_clean["国内消費仕向量【1000トン】"],
            # offsetgroup=0,
        ),
        go.Bar(
            name="Local production",
            x=df_clean["年度"],
            y=df_clean["国内生産量【1000トン】"],
            offsetgroup=1,
        ),
        go.Bar(
            name="Imports",
            x=df_clean["年度"],
            y=df_clean["外国貿易_輸入量【1000トン】"],
            offsetgroup=1,
            base=df_clean["国内生産量【1000トン】"],
        ),
        go.Bar(
            name="Exports",
            x=df_clean["年度"],
            y=df_clean["外国貿易_輸出量【1000トン】"] * (-1),
            offsetgroup=1,
            # base=df_clean["国内生産量【1000トン】"],
        ),
    ],
    layout=go.Layout(
        title="Soy beans supply and demand in Japan",
        yaxis_title="volume",
    )
)

fig.update_layout(font_size=20,
                  title={'text': 'Japan soybean production and consumption(in thousand metric tons)', 'y': 0.95,
                         'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}, yaxis={'categoryorder': 'total ascending', },
                  paper_bgcolor='rgb(248,248,255)',
                  plot_bgcolor='rgb(248,248,255)')

## Add data source
fig.add_annotation(text="Source: e-Stat https://www.e-stat.go.jp",
                   xref="paper", yref="paper",
                   x=-0.05, y=-0.2, showarrow=False, font=dict(family='Arial', size=12,
                                                               color='rgb(150, 150, 150)'))

## Hide legend
fig.update(layout_showlegend=False)

## Add image as background image
fig.add_layout_image(
    dict(source=im,
         xref="paper",
         yref="paper",
         x=-0.5,
         y=2,
         sizex=5,
         sizey=5,
         # sizing="stretch",
         opacity=0.2,
         # layer ='below'
         )
)

## Add text annotation
fig.add_annotation(xref='paper', yref='paper', x=0.4, y=1.1,
                   text="Local consumption",
                   font=dict(family='Arial', size=16,
                             color='rgb(0,0,250)'),
                   showarrow=False,
                   arrowhead=3, arrowsize=2, arrowwidth=1, ax=50, ay=-50, arrowcolor='blue')

## Add text annotation
fig.add_annotation(xref='paper', yref='paper', x=0.5, y=1.1,
                   text="Import",
                   font=dict(family='Arial', size=16,
                             color='rgb(0,200,100)'),
                   showarrow=False,
                   arrowhead=2, arrowsize=2, arrowwidth=1, ax=20, ay=-50, arrowcolor='rgb(0,200,100)')

## Add text annotation
fig.add_annotation(xref='paper', yref='paper', x=0.62, y=1.1,
                   text="local production",
                   font=dict(family='Arial', size=16,
                             color='rgb(250,0,0)'),
                   showarrow=False,
                   arrowhead=2, arrowsize=2, arrowwidth=1, ax=20, ay=-50, arrowcolor='rgb(200,0,100)')

fig.show()



