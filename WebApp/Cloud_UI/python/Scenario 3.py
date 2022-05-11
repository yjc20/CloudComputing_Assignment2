import numpy as py;
import pandas as pd;
import matplotlib.plot as plt:

#Generate Line Graph
def generate_line_graphs():
  
  #Read the data
  df_income = pd.read_csv("/results_data/filename.csv")
  
  #Initialize with district values
  x = ['labela', 'labelb', 'labelc']
  
  #Need to further check this
  y1 = df_income['subjectivity']
  y2 = df_income['polarity']
  
  plt.plot(x, y1, label = 'Subjectivity Score')
  plt.plot(x, y2, label = 'Polarity Score')
  plt.legend()
  plt.show()
