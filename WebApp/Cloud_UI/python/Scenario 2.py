import numpy as py;
import plotly as plot;
import matplotlib.pyplot as plt;
import pandas as pd;

# Read Data
 crime_df = pd.read_json("/results_data/tweets_crime")
  
# Generate bar plots
def generate_bar_plots():
 
  barWidth = 0.4

  #Need to initialize
  x_value1 = 
  x_value2 = 
  
  #Need to check this
  y_value1 = crime_df['results']
  y_value2 = crime_df['results']

  plt.bar(x_value1, y_value1, width = barWidth, color = 'blue', edgecolor = 'black', capsize=7, label='Subjectivity Score')
  
  plt.bar(x_value2, y_value2, width = barWidth, color = 'red', edgecolor = 'black', capsize=7, label='Crime rate')
  
  #Initialize the values
  plt.xticks(, ['', '', '', '', ''])
  plt.ylabel()
  plt.legend()
  
  plt.show()
