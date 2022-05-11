import pandas as pd;
import matplotlib.pyplot as plt;
from wordcloud import WordCloud

def generate_word_cloud():
  #Read the data
  df_hashtags = pd.read_csv("/result_data/hashtags.csv")
  text = df_hashtags['hashtags'].to_string()
  
  # Create and generate a word cloud image:
  wordcloud = WordCloud().generate(text)

  # Display the generated image:
  plt.imshow(wordcloud, interpolation='bilinear')
  plt.axis("off")
  plt.show()
