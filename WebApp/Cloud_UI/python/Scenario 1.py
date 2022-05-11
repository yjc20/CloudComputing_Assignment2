import numpy as py;
import pandas as pd
import seaborn as sbn
sbn.set_theme()

#Generate heatmap
def generate_heatmap():
  
  #Read COVID related data
  df_covid = pd.read_csv("./result_data/filename.csv")
  ax = sbn.heatmap(df_covid[['subjectivity', 'polarity']])
  return ax


