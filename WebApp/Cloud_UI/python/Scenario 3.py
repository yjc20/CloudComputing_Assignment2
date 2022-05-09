import numpy as py;
import plotly as plot;
import pandas as pd;
import matplotlib.plot as plt:

#Read the data
df_income = pd.read_csv("/results_data/tweets_income")

#Generate Line Graph
def generate_line_graphs():
  
  #Initialize with district values
  x = ['Melbourne', '', '', '', '', '']
  #Need to further check this
  y1 = df_income['results']
  y2 = df_income['results']
  
  plt.plot(x, y1, label = 'Avg Income')
  plt.plot(x, y2, label = 'Polarity Score')
  plt.legend()
  plt.show()
