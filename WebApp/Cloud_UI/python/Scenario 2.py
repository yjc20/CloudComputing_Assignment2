import numpy as np;
import matplotlib.pyplot as plt;
import pandas as pd;

# Generate bar plots
def generate_bar_plots():
 
 # Read Data
 transport_df = pd.read_csv("./result_data/filename.csv")
 
 barWidth = 0.25
 x_value1 = ['Train', 'Tram', 'Bus', 'Traffic']
 x_axis = np.arange(len(x_value1))  
 c = ['red', 'yellow', 'green', 'blue'] 
  
 y_value1 = transport_df['train'].sum()
 y_value2 = transport_df['tram'].sum()
 y_value3 = transport_df['bus'].sum()
 y_value4 = transport_df['traffic'].sum()

 plt.bar(x_axis, y_value1, width = barWidth, color = c, edgecolor = 'black')
  
 #Initialize the values
 plt.xticks(x_axis, x_value1)
 plt.xlabel('Mode of Transport')
 plt.ylabel('Polarity')
 plt.show()
