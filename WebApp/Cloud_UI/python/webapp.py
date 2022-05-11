
import matplotlib.pyplot as plt
from flask import Flask, render_template, send_file, request, url_for, redirect
import json

from scenario1 import generate_heatmap
from scenario2 import generate_bar_plots
from scenario3 import generate_line_graphs
from scenario4 import generate_pie_chart
from scenario5 import generate_word_cloud

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

if __name__ == '__main__':
    app.run(debug=True,use_reloader=True)

