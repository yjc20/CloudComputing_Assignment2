# Assignment 2 - COMP90024

# Cluster and Cloud Computing - Team 4
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import couchdb
from textblob import TextBlob
import re
from wordcloud import WordCloud

f = open('./ip.txt')
f = f.readline()
f = f.strip()
f ='http://'+f+':5984'

couchserver=couchdb.Server(url=f)
couchserver.resource.credentials=('admin','admin')

tweet_data = couchserver['tweet']
rows = tweet_data.view('_all_docs', include_docs=True)
data = [row['doc'] for row in rows]
df = pd.DataFrame(data)

#Twin bar plot
def twin_barplots(df):
 
 health_keywords = 'health|hospital|doctor|disease|medicine|GP|medicare|clinic|medical|nurse|ward|hygiene|COVID|Cancer|AIDS|Heart attack|Ambulance|death|illness|vitality|sick|sickness|diseases|doctors|healthy|hospitals|emergency|clinics|vaccine|vaccines|medicines|accident|fatal|obesity|mental|depression|anxiety|fever|headache|pain|first-aid|red cross|clinical'

 df_health = df[df['text'].str.contains(health_keywords, flags=re.IGNORECASE)] 
  
 df_city =  df_health.loc[df_health['city'].isin(['Melbourne', 'Frankston', 'Yarra', 'Geelong'])]  
 
 data = df_city.groupby('city').mean()
 x = list(data.index)

 #Read AURIN Data
 df_gp = pd.read_csv('income_gp.csv')

 df_gp = df_gp.loc[df_gp['lga_name'].isin(['Melbourne (C)', 'Frankston (C)', 'Yarra (C)', 'Greater Geelong (C)'])]
 gp = list(df_gp[' gps_per_1000_pop'])
 x_axis = np.arange(len(x))
 y = list(data['polarity']) 
 gp_scale = [x/10 for x in gp]
 return x, y, gp_scale
#Generate heatmap
def generate_heatmap(df):
 sports_keywords = "sports|sport|afl|footie|footy|soccer|cricket|tennis|hockey|AUSOPEN|AFL|Warner|BigBash|NRL|Rugby|Bundesliga|Warne|Ronaldo|Messi|ManU|Chelsea|Nadal|Djokovic|T20WC|Nick Kyrgios|T20|World Cup|MCG|Marvel Stadium|Athletics|CommonWealth Games|Olympics"
 df_sports = df[df['text'].str.contains(sports_keywords, flags=re.IGNORECASE)]
 return  df_sports

# Generating PieChart
def generate_pie_chart(df):
    labor_party_keywords = "labour party|australianlaborparty|australian labor party|australianlaborparty|australian labor|anthony albanese|bill shorten"
    liberal_party_keywords = "liberal|liberal party|scott morrison|scottmorrison"

    labor_df = df[df['text'].str.contains(labor_party_keywords, flags=re.IGNORECASE)]
    liberal_df = df[df['text'].str.contains(liberal_party_keywords, flags=re.IGNORECASE)]
    labor_polarity = labor_df['polarity'].mean()
    liberal_polarity = liberal_df['polarity'].mean()

    labor_polarity_normalised = labor_polarity / (labor_polarity + liberal_polarity)
    liberal_polarity_normalised = liberal_polarity / (labor_polarity + liberal_polarity)
    value = [labor_polarity_normalised, liberal_polarity_normalised]

    #Read AURIN Election Data
    df_election2019 = pd.read_csv('election.csv')
    labor_2019 = df_election2019['tpp_australian_labor_party_percentage'].mean()
    liberal_2019 = df_election2019[' tpp_liberal_national_coalition_percentage'].mean()

    value2019 = [labor_2019, liberal_2019]
    return value, value2019
 
# Generate bar plots
def generate_bar_plots(df):
 
 barWidth = 0.25
 train_keyword = "Train|Railway|Trains|Railways|Metro|Rail"
 tram_keyword = "Tram|Trams"
 bus_keyword = "Bus|Buses"
 traffic_keyword = "Traffic|Congestion|Road"
 
 x_value1 = ['Train', 'Tram', 'Bus', 'Traffic']
 x_axis = np.arange(len(x_value1))  
 c = ['red', 'yellow', 'green', 'blue'] 
  
 train_df = df[df['text'].str.contains(train_keyword, flags=re.IGNORECASE)]
 tram_df = df[df['text'].str.contains(tram_keyword, flags=re.IGNORECASE)]
 bus_df = df[df['text'].str.contains(bus_keyword, flags=re.IGNORECASE)]
 traffic_df = df[df['text'].str.contains(traffic_keyword, flags=re.IGNORECASE)]
 
 train_polarity  = train_df['polarity'].mean()
 tram_polarity  = tram_df['polarity'].mean()
 bus_polarity  = bus_df['polarity'].mean()
 traffic_polarity  = traffic_df['polarity'].mean()
 
 total_polarity = [train_polarity, tram_polarity, bus_polarity, traffic_polarity]
 return x_value1, total_polarity, x_axis 
  
#Generate Line Graph
def generate_line_graphs(df):
    
 df_city =  df.loc[df['city'].isin(['Melbourne', 'Frankston', 'Yarra', 'Geelong'])]

 #Read AURIN data 
 df_income = pd.read_csv('income_gp.csv')
 df_income = df_income.loc[df_income['lga_name'].isin(['Melbourne (C)', 'Frankston (C)', 'Yarra (C)', 'Greater Geelong (C)'])] 
 y1 =  list(df_income[' ppl_with_income_less_aud400_per_week_perc'])
 data = df_city.groupby('city').mean()
 y2 = list(data['polarity'])
 x = list(data.index) 
 y1_scale = [x/100 for x in y1] 
 return x, y1_scale, y2
  
def generate_word_cloud(df):

  text = ' '.join(i for i in df['text'])
  result = re.findall(r"#(\w+)", text)
  result = ' '.join(result)
  # Create and generate a word cloud image:
  wordcloud_hashtags = WordCloud(collocations = False).generate(result)
  return wordcloud_hashtags
