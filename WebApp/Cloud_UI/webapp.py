# Assignment-2 : COMP90024

# Cluster and Cloud Computing - Team 4 
import matplotlib.pyplot as plt
from flask import Flask, render_template, send_file, request, url_for, redirect
import json
import couchdb
import pandas as pd
from matplotlib import pyplot as plt
import plotly
import plotly.graph_objects as go
import numpy as np
from io import BytesIO
import plotly.express as px
from Scenario import twin_barplots, generate_heatmap, generate_bar_plots, generate_line_graphs, generate_pie_chart, generate_word_cloud

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
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def display_index():
  return render_template("Home.html")

@app.route('/scenario1')
def display_heatmap():
  data_value = generate_heatmap(df)
  heatmap = px.density_heatmap(data_value, x="polarity", y="subjectivity", template='presentation')
  heatmapJSON = json.dumps(heatmap, cls=plotly.utils.PlotlyJSONEncoder)
  return render_template('First_scenario.html', heatmapJSON = heatmapJSON)

@app.route('/scenario2')
def display_barplot():
  c = ['red', 'yellow', 'green', 'blue']
  x_value1, total_polarity, x_axis = generate_bar_plots(df) 
  
  plot = go.Figure()
  plot.add_trace(go.Bar(x=x_value1,y=total_polarity,name="<b>Mode of Transport vs Polarity<b>"))

  plot.update_traces(texttemplate='%{text:.2s}')
  plot.update_layout(legend_title_text='Legend', template='presentation')
  plot.update_yaxes(title_text="<b>Polarity</b>", autorange=True)
  
  barplotJSON = json.dumps(plot, cls = plotly.utils.PlotlyJSONEncoder)
  return render_template('Second_scenario.html', barplotJSON = barplotJSON)

@app.route('/scenario3')
def display_line_graphs():
  x, y1, y2 = generate_line_graphs(df)
  print([x, y1, y2])
  dic = {'regions':x,'polarity':y2,'low_income_value':y1}
  data = pd.DataFrame(dic) 
  plot = px.line(data, x='regions', y=data.columns[1:], title='Comparison of Polarity and Low Income')

  line_graphJSON = json.dumps(plot, cls= plotly.utils.PlotlyJSONEncoder)
  return render_template('Third_scenario.html', line_graphJSON = line_graphJSON)

@app.route('/scenario4')
def display_piechart():
  names = ['Labor Party', 'Liberal Party']
  color= ['red', 'blue']  
  pie, pie2019 = generate_pie_chart(df)
  pie_chart = px.pie(values=pie, names=names, color=names,color_discrete_map={names[0]: color[0], names[1]: color[1]},template='presentation')
  pie_chart2019 = px.pie(values=pie2019, names=names, color=names, color_discrete_map={names[0]: color[0], names[1]: color[1]}, template='presentation')

  pieJSON = json.dumps(pie_chart, cls= plotly.utils.PlotlyJSONEncoder)
  pieJSON2019 = json.dumps(pie_chart2019, cls = plotly.utils.PlotlyJSONEncoder)
  return render_template('Fourth_scenario.html', pieJSON = pieJSON, pieJSON2019 = pieJSON2019) 

@app.route('/wordcloud')
def wordcloud():
  wc_hashtags = generate_word_cloud(df)
  fig = plt.figure(figsize=(10,5))
  plt.imshow(wc_hashtags)
  plt.axis("off")
  plt.tight_layout(pad=0)
  img = BytesIO()
  fig.savefig(img)
  img.seek(0)
  plt.close()
  return send_file(img, mimetype='image/png')

@app.route('/scenario5')
def display_twin_barplots():
  x, y, gp = twin_barplots(df)
  x_axis = np.arange(len(x))

  plot = go.Figure()
  plot.add_trace(go.Bar(x=x,y=y,name="Polarity"))
  plot.add_trace(go.Bar(x=x, y=gp,name="Number of GP's per ten thousand people"))  
  plot.update_traces(texttemplate='%{text:.2s}')
  plot.update_layout(legend_title_text='Legend', template='presentation')
  plot.update_yaxes(title_text="<b>Polarity</b>", autorange=True)

  twinbarJSON = json.dumps(plot, cls = plotly.utils.PlotlyJSONEncoder)
  return render_template('Fifth_scenario.html', twinbarJSON = twinbarJSON)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True,use_reloader=True)

