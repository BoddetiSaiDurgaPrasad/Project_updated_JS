from flask import *
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import string
import nltk
import re
from nltk.corpus import stopwords
stopword=set(stopwords.words('english'))
app = Flask(__name__)

@app.route("/")
@app.route('/received_data',methods=['GET','POST'])
def home():
    try:
        f = request.files['file']
        f.save("static/sample.csv")
        data = pd.read_csv(r"static/sample.csv",encoding = 'latin1')
        #nltk.download('stopwords')
        stemmer = nltk.SnowballStemmer("english")
        def clean(text):
            text = str(text).lower()
            text = re.sub('\[.*?\]', '', text)
            text = re.sub('https?://\S+|www\.\S+', '', text)
            text = re.sub('<.*?>+', '', text)
            text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
            text = re.sub('\n', '', text)
            text = re.sub('\w*\d\w*', '', text)
            text = [word for word in text.split(' ') if word not in stopword]
            text=" ".join(text)
            text = [stemmer.stem(word) for word in text.split(' ')]
            text=" ".join(text)
            return text
        data["Review"] = data["Review"].apply(clean)
        text = " ".join(i for i in data['Review'])
        stopwords = set(STOPWORDS)
        wordcloud = WordCloud(stopwords=stopwords,background_color="white").generate(text)
        #nltk.download('vader_lexicon')
        sentiments = SentimentIntensityAnalyzer()
        data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["Review"]]
        data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["Review"]]
        data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["Review"]]
        data = data[["Review", "Positive", "Negative", "Neutral"]]
        
        x = sum(data["Positive"])
        y = sum(data["Negative"])
        z = sum(data["Neutral"])
        answer=x+y+z
        x=(x/answer)*100
        y=(y/answer)*100
        z=(z/answer)*100
        x=round(x,2)
        y=round(y,2)
        z=round(z,2)
        data.to_csv('final.csv')
        return jsonify({'res': 1, 'x': x, 'y': y, 'z': z})
    except:
        return render_template("index.html")

@app.route('/download')
def download():
    fe='final.csv'
    return send_file(fe,as_attachment=True)



if __name__ == '__main__':
	app.run(debug=True)
