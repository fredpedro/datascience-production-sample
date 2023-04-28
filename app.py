from flask import Flask, render_template, request , url_for, flash, redirect
from flask_restful import Resource,Api
from sklearn.externals import joblib
from werkzeug.utils import secure_filename
import pandas as pd

from bokeh.plotting import figure
from bokeh.embed import components

from plotting import create_figure_and_get_components

app=Flask(__name__)
api=Api(app)

app.config['SECRET_KEY'] = '4a6e601a204ea089231f5dff46ecb863ddb1d8f39380d595'

# web forms tutorial
# https://www.digitalocean.com/community/tutorials/how-to-use-web-forms-in-a-flask-application
# https://andresberejnoi.com/interactive-plots-with-bokeh-and-flask/

@app.route('/')
def index():
    return render_template('index.html', messages=messages)


@app.route('/processdata', methods=('GET', 'POST'))
def processdata():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        else:
            file = request.files['file']
            # https://sebhastian.com/xlrdbiffhxlrderror-excel-xlsx-file-not-supported/
            df = pd.read_excel(file, engine='openpyxl')
            filename = secure_filename(file.filename)

            
            coin = df['coin']
            marketcap = df['marketcap']

            # Creating Plot Figure
            p = figure(
                x_range=coin,
                height=400,
                title="Market Cap of Top 10 Coins",
                sizing_mode="stretch_width"
            )
            
            # Defining Plot to be a Vertical Bar Plot
            p.vbar(x=coin, top=marketcap, width=0.5)
            p.xgrid.grid_line_color = None
            p.y_range.start = 0

            script, div = components(p)
            
            kwargs = {'script': script, 'div': div}
            return render_template('index.html',**kwargs)


    return render_template('processdata.html')

if __name__=='__main__':
    app.run(debug=True)
