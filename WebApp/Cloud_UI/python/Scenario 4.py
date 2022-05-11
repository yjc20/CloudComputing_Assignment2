import numpy as np
import matplotlib.pyplot as plt

def generate_pie_chart():
  #Read the data
  df_election = pd.read_csv("./result_data/election.csv")
  result = df_election['tpp_australian_labor_party_percentage', ' tpp_liberal_national_coalition_percentage']].loc[0]
  labels = ['tpp_australian_labor_party_percentage', ' tpp_liberal_national_coalition_percentage']
  plt.pie(result, labels = labels, shadow = True, autopct='%1.1f%%')
  plt.legend()
  plt.show()
