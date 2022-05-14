
import matplotlib.pyplot as plt
from flask import Flask, render_template, send_file, request, url_for, redirect
import json

from Scenario import twin_barplots, generate_heatmap, generate_bar_plots, generate_line_graphs, generate_pie_chart, generate_word_cloud

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def display_index():
  return render.template("Home.html")

@app.route('/scenario1')
def display_heatmap():
  ax = generate_heatmap()
  return ax

@app.route('/scenario2')
def display_barplot():
  return generate_bar_plots()

@app.route('/scenario3')
def display_line_graphs():
  return generate_line_graphs()

@app.route('/scenario4')
def display_piechart():
  return generate_pie_chart()

@app.route('/wordcloud')
def wordcloud():
  return generate_word_cloud()

@app.route('/scenario5')
def display_twin_barplots():
  return twin_barplots()
if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)

