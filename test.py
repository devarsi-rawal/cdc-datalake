import findspark
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral5, Category20_20, Turbo256
from bokeh.transform import factor_cmap
from bokeh.models.tools import HoverTool
import math

bokeh_doc = curdoc()

findspark.init('/usr/lib/spark/')
spark = SparkSession.builder.appName('Wonder').getOrCreate()
df = spark.read.load('./CaseCounts.csv', format='com.databricks.spark.csv', header='true', inferSchema='true')
# newdf = df.select(df['year reported'], df['case counts']).groupBy('year reported').sum()
# newdf = df.filter(df["disease"]=="Spotted Fever Rickettsiosis")
newdf = df.groupBy(df['disease']).sum()
# newdf = newdf.filter(newdf["disease"]=="Spotted Fever Rickettsiosis")
newdf = newdf.toPandas()
newdf.rename(columns = {'sum(case counts)':'case_counts'}, inplace = True)
print(newdf.head())

# Bokeh stuff
# p = figure(plot_height=600, plot_width=600, title="Case Counts per Year")
source = ColumnDataSource(newdf)
diseases = source.data['disease'].tolist()
diseases.sort()
diseases = list(map(str, diseases))
#  print(diseases)
plot = figure(plot_height=800, plot_width=1000, x_range=diseases)

# print(source)

# color_map = factor_cmap(field_name="disease", palette=Turbo256, factors=diseases)
plot.vbar(x='disease', top="case_counts", source=source, width=0.70) #, color=color_map)
plot.title.text = "Case Counts per Disease"
plot.xaxis.axis_label = "Disease"
plot.yaxis.axis_label = "Case Counts"
plot.xaxis.major_label_text_font_size = "5pt"
plot.xaxis.major_label_orientation = "vertical"

hover = HoverTool()
hover.tooltips = [
    ("Disease", "@disease"),
    ("Count", "@case_counts")
]

hover.mode = "vline"
plot.add_tools(hover)

bokeh_doc.add_root(plot)

bokeh_doc.title = "Case Counts per Disease"