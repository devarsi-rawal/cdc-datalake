import os
import findspark
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, MultiSelect, RangeSlider
from bokeh.palettes import Spectral5, Category20_20, Turbo256
from bokeh.transform import factor_cmap
from bokeh.models.tools import HoverTool
from bokeh.layouts import column, row, layout
import math

# def select_disease(attrname, old, new):
#     new_source = ColumnDataSource(pddf[pddf["disease"].isin(multi_select.value)])
#     source.data.update(new_source.data)
#     new_diseases = new_source.data['disease'].tolist()
#     new_diseases.sort()
#     new_diseases = list(map(str, new_diseases))
#     plot.x_range.factors = new_diseases
    
def filter_update(attrname, old, new):
    filter_df = orig_pddf[orig_pddf["age"].between(age_slider.value[0], age_slider.value[1])]
    filter_df = filter_df[filter_df['disease'].isin(multi_select.value)]
    print(filter_df)
    filter_df = filter_df.groupby(['disease']).sum()
    print(filter_df)
    # print(filter_df.head())
    new_source = ColumnDataSource(filter_df)
    new_diseases = new_source.data['disease'].tolist()
    new_diseases.sort()
    new_diseases = list(map(str, new_diseases))
    plot.x_range.factors = new_diseases
    source.data.update(new_source.data)
    

bokeh_doc = curdoc()

# Read csv using spark
findspark.init(os.environ["SPARK_HOME"])
spark = SparkSession.builder.appName('Wonder').getOrCreate()
df = spark.read.load('./data/CaseCounts.csv', format='com.databricks.spark.csv', header='true', inferSchema='true')
orig_pddf = df.toPandas()
pddf = orig_pddf.groupby(['disease']).sum()
# pddf.rename(columns = {'sum(case counts)':'case_counts'}, inplace = True) # Accomodate for bokeh typing issues

# Bokeh stuff
source = ColumnDataSource(pddf)
diseases = source.data['disease'].tolist()
diseases.sort()
diseases = list(map(str, diseases))
plot = figure(plot_height=800, plot_width=1000, x_range=diseases, sizing_mode="stretch_both")

# Create disease multiselect
multi_select = MultiSelect(title="Diseases", value=diseases, options=diseases, height=100, sizing_mode="stretch_both")
multi_select.on_change('value', filter_update)

# Create age slider
ages = df.select("age").rdd.flatMap(lambda x: x).collect()
ages.sort()
age_slider = RangeSlider(title="Age", start=ages[0], end=ages[-1], value=(ages[0], ages[-1]), step=5, sizing_mode="stretch_both")
age_slider.on_change("value", filter_update)

# Add plot details
plot.vbar(x='disease', top="case counts", source=source, width=0.70)
plot.title.text = "Case Counts per Disease"
plot.xaxis.axis_label = "Disease"
plot.yaxis.axis_label = "Case Counts"
plot.xaxis.major_label_text_font_size = "5pt"
plot.xaxis.major_label_orientation = "vertical"

hover = HoverTool()
hover.tooltips = [
    ("Disease", "@disease"),
    ("Count", "@{case counts}")
]

hover.mode = "vline"
plot.add_tools(hover)
filters = column([multi_select, age_slider], width=500, height=1000)
bokeh_doc.add_root(row([filters, plot]))

bokeh_doc.title = "CDC Data Lake"