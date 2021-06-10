# imports
from flask import *
import numpy as np
import pandas as pd

# initialize the flask app
app = Flask('myapi')

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def form():
    return render_template('form.html')

res = pd.read_csv('./assets/rec_web.csv')
cosine_sim = np.load('./assets/cosine_sim.npy')

@app.route('/searchid')
def get_id():
    user_input = request.args
    name = str(user_input['resname'])
    output = res[res['title'].str.contains(name, case=False)][['title', 'placeid', 'address']].head(75).reset_index(drop=True)
    output['Recommend Similar Restaurants'] = output['placeid'].apply(lambda x: '<a href="./recommend?placeid1={0}&placeid2=&placeid3=&location=28">Find!</a>'.format(x))
    output.rename({'title': 'Restaurant Name', 'placeid': 'ID', 'address':'Address'}, axis=1, inplace=True)
    searchno = len(output)
    output_table = output.to_html(escape=False, justify='left', index=False)
    return render_template('search.html', output_table=output_table, name=name, searchno=searchno)

def recommend(placeids, cluster='NA', cosine_sim=cosine_sim):
    placeids = [res[res['placeid'] == i].index[0] for i in placeids if i]
    if placeids==[]:
        output = res.loc[placeids, ['title', 'category', 'address', 'score', 'reviewsno', 'url']]
        output['Google Link'] = output['url'].apply(lambda x: '<a href="{0}">link</a>'.format(x))
        output.drop(columns='url', inplace=True)
        output.rename({'title': 'Restaurant Name', 'category': 'Category', 'address':'Address', 'score': 'Average Rating', 'reviewsno': 'No. of Reviews'}, axis=1, inplace=True)
    else:
        cosine_sim_series = pd.Series(np.empty(cosine_sim[0].shape))
        for i in placeids: 
            cosine_sim_series += pd.Series(cosine_sim[i])
        cosine_sim_series = cosine_sim_series/len(placeids)
        cos_series = pd.Series(cosine_sim_series).sort_values(ascending=False)
        length = 31
        if cluster!=28: 
            length = 51
        top_50_indexes = list(cos_series.iloc[len(placeids):length].index)
        df = res.iloc[top_50_indexes, :].sort_values(['score', 'reviewsno'], ascending=False)
        if cluster!=28:
            df = df[df['cluster']==cluster]
        df = df[df['reviewsno']>=5]
        df['Google Link'] = df['url'].apply(lambda x: '<a href="{0}">link</a>'.format(x))
        output = df[['title', 'category', 'address', 'score', 'reviewsno', 'Google Link']].head(10)
        output['reviewsno'] = output['reviewsno'].apply(lambda x: int(x))
        output.rename({'title': 'Restaurant Name', 'category': 'Category', 'address':'Address', 'score': 'Average Rating', 'reviewsno': 'No. of Reviews'}, axis=1, inplace=True)
    input = res.loc[placeids, ['title', 'category', 'address', 'score', 'reviewsno', 'url']]
    input['Google Link'] = input['url'].apply(lambda x: '<a href="{0}">link</a>'.format(x))
    input['reviewsno'] = input['reviewsno'].apply(lambda x: int(x))
    input.rename({'title': 'Restaurant Name', 'placeid': 'ID', 'address':'Address', 'score': 'Average Rating', 'reviewsno': 'No. of Reviews'}, axis=1, inplace=True)
    input.drop(columns='url', inplace=True)
    return input, output

@app.route('/recommend')
def make_recommendation():
    user_input = request.args
    placeids=[]
    placeid1 = str(user_input['placeid1'])
    placeid2 = str(user_input['placeid2'])
    placeid3 = str(user_input['placeid3'])
    cluster = int(user_input['location'])
    placeids.extend([placeid1, placeid2, placeid3])
    input, output = recommend(placeids=placeids, cluster=cluster)
    recommendno = len(output)
    output_table = output.reset_index(drop=True).to_html(escape=False, justify='left', index=False)
    input_table = input.reset_index(drop=True).to_html(escape=False, justify='left', index=False)
    return render_template('results.html', output_table=output_table, input_table=input_table, recommendno=recommendno)

# Call app.run(debug=True) when python script is called
if __name__ == '__main__':
    app.run(debug=True)