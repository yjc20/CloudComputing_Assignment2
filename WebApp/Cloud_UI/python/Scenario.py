import re

import couchdb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sbn
from wordcloud import WordCloud

from WebApp.Cloud_UI.python.webapp import wordcloud

sbn.set_theme()

f = open('./ip.txt')
f = f.readline()
f = f.strip()
f = 'http://' + f + ':5984'

couchserver = couchdb.Server(url=f)
couchserver.resource.credentials = ('admin', 'admin')

tweet_data = couchserver['tweet']
rows = tweet_data.view('_all_docs', include_docs=True)
data = [row['doc'] for row in rows]
df = pd.DataFrame(data)


# Twin bar plot
def twin_barplots(df):
    health_keywords = 'health|hospital|doctor|disease|medicine|GP|medicare|clinic|medical|nurse' \
                      '|ward|hygiene|COVID|Cancer|AIDS|Heart attack|Ambulance|death|illness' \
                      + 'vitality|sick|sickness|diseases|doctors|healthy|hospitals|emergency' \
                        '|clinics|vaccine|vaccines|' + \
                      'medicines|accident|fatal|obesity|mental|depression|anxiety|fever|headache' \
                      '|pain|first-aid|red cross|clinical '

    df_health = df[df['text'].str.contains(health_keywords, flags=re.IGNORECASE)]

    df_city = df_health.loc[
        df_health['city'].isin(['Melbourne', 'Frankston', 'South Yarra', 'Geelong'])]
    # Initialize with region values
    x = ['Melbourne', 'Frankston', 'South Yarra', 'Geelong']

    polarity = df_city['polarity'].groupby('city').mean()
    # Read AURIN Data
    gp = [1, 2, 3, 4]

    x_axis = np.arange(len(X))

    plt.bar(x_axis - 0.2, polarity, 0.4, label='Polarity')
    plt.bar(x_axis + 0.2, gp, 0.4, label="Number of GP's per thousand people")

    plt.xticks(x_axis, x)
    plt.xlabel("Regions")
    plt.ylabel("Polarity")
    plt.title("Health Analysis")
    plt.legend()
    plt.show()


# Generate heatmap
def generate_heatmap(df):
    sports_keywords = "sports|sport|afl|footie|footy|soccer|cricket|tennis|hockey|AUSOPEN|AFL" \
                      "|Warner|BigBash|NRL| "
    +"Rugby|Bundesliga|Warne|Ronaldo|Messi|ManU|Chelsea|Nadal|Djokovic|T20WC|Nick Kyrgios|T20|World Cup|MCG|Marvel Stadium|Athletics|CommonWealth Games|Olympics"

    df_sports = df[df['text'].str.contains(sports_keywords, flags=re.IGNORECASE)]

    polarity = list(df_sports['polarity'])
    subjectivity = list(df_sports['subjectivity'])

    heatmap, xedges, yedges = np.histogram2d(np.array(polarity), np.array(subjectivity),
                                             bins=(10, 20))
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    plt.rcParams["figure.figsize"] = (10, 5)
    plt.clf()
    plt.imshow(heatmap.T, extent=extent, origin='lower', cmap='plasma')
    plt.title("Sports Subjectivity vs Polarity")
    plt.ylabel("Subjectivity")
    plt.xlabel("Polarity")
    # plt.figure(figsize=(100, 100))
    plt.show()


# Generating PieChart
def generate_pie_chart(df):
    labor_party_keywords = "labour party|australianlaborparty|australian labor " \
                           "party|australianlaborparty|australian labor|anthony albanese|bill " \
                           "shorten "
    liberal_party_keywords = "liberal|liberal party|scott morrison|scottmorrison"

    labor_df = df[df['text'].str.contains(labor_party_keywords, flags=re.IGNORECASE)]
    liberal_df = df[df['text'].str.contains(liberal_party_keywords, flags=re.IGNORECASE)]
    labor_polarity = labor_df['polarity'].mean()
    liberal_polarity = liberal_df['polarity'].mean()

    labor_polarity_normalised = labor_polarity / (labor_polarity + liberal_polarity)
    liberal_polarity_normalised = liberal_polarity / (labor_polarity + liberal_polarity)
    value = [labor_polarity_normalised, liberal_polarity_normalised]
    return value


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

    train_polarity = train_df['polarity'].mean()
    tram_polarity = tram_df['polarity'].mean()
    bus_polarity = bus_df['polarity'].mean()
    traffic_polarity = traffic_df['polarity'].mean()

    total_polarity = [train_polarity, tram_polarity, bus_polarity, traffic_polarity]

    plt.bar(x_axis, total_polarity, width=barWidth, color=c, edgecolor='black')

    # Initialize the values
    plt.xticks(x_axis, x_value1)
    plt.xlabel('Mode of Transport')
    plt.ylabel('Polarity')
    plt.show()


# Generate Line Graph
def generate_line_graphs(df):
    df_city = df.loc[df['city'].isin(['Melbourne', 'Frankston', 'South Yarra', 'Geelong'])]
    # Initialize with region values
    x = ['Melbourne', 'Frankston', 'South Yarra', 'Geelong']

    # Read AURIN data
    y1 = [0, 1, 2, 3]
    y2 = df_city['polarity'].groupby('city').mean()

    plt.plot(x, y1, label='Subjectivity Score')
    plt.plot(x, y2, label='Polarity Score')
    plt.legend()
    plt.show()


def generate_word_cloud(df):
    text = ' '.join(df['text'])
    result = re.findall(r"#(\w+)", text)
    result = ' '.join(result)
    # Create and generate a word cloud image:
    wordcloud_hashtags = WordCloud().generate(result)

    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
