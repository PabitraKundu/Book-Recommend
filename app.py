from flask import Flask,render_template, request
import pandas as pd
import numpy as np
import pickle
popular_df = pickle.load(open('popular.pkl','rb'))

pt = pickle.load(open('pt.pkl','rb'))
books= pickle.load(open('books.pkl','rb'))
similarity_scores= pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/top')
def top():
    return render_template('top.html',
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           ratings=list(popular_df['avg_ratings'].values))
#@app.route("/products")
#def products():
    #return "<p>This is product page</p"
@app.route('/recommend')
def recommend():
    return render_template('recom.html') 
@app.route('/result',methods=['post'])
def result():
    user_input = request.form.get('user_input')
    
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse = True)[1:5]
    #distances = similarity_scores[index]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        
        data.append(item)

    print(data)
    
   
    
    return render_template('recom.html' , data=data)
   


if __name__ == '__main__':
    app.run(debug=True,port=8000)