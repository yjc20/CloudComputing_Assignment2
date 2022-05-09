import numpy as py;
import pandas as pd
import seaborn as sbn
sbn.set_theme()
#Covid HeatMap

#Read COVID related data
df_covid = pd.read_csv("./result_data/tweets_covid.csv")

#Generate heatmap for Covid related data
def generate_heatmap():
  ax = sbn.heatmap(df_covid[['subjectivity', 'polarity']])
  return ax


