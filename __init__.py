from flask import Flask, render_template, request, session
import ast
import csv
import random
import pandas as pd


app = Flask(__name__)
app.secret_key = 'secret_key'
@app.route('/')
def home():
    # Read in CSV file
    total = len(pd.read_csv('summaries.csv')) - 1
    x = random.randint(0,total)
    with open("summaries.csv", "r", encoding="utf8") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    box1_text = data[x]["summary"]
    # Shuffle the remaining values
    values = [data[x]["TextRank"], data[x]["KL"], data[x]["T5"], data[x]["BART"]]
    random.shuffle(values)

    summary_dict = {
        "box1_text": box1_text,
        "box2_text": values[0],
        "box3_text": values[1],
        "box4_text": values[2],
        "box5_text": values[3],
        "A": values.index(data[x]["TextRank"]) + 1,
        "B": values.index(data[x]["KL"]) + 1,
        "C": values.index(data[x]["T5"]) + 1,
        "D": values.index(data[x]["BART"]) + 1,
        "values": values,  # Pass values as a dictionary key
        "x":x
    }
    # render the home page template and pass in the box text and values
    return render_template('home.html', **summary_dict)

def mapper(rank1, rank2, rank3, rank4, df):
    if rank1 in df["TextRank"].values:
        rank1 = "TextRank"
    elif rank1 in df["KL"].values:
        rank1 = "KL"
    elif rank1 in df["T5"].values:
        rank1 = "T5"
    else:
        rank1 = "BART"
        
    if rank2 in df["TextRank"].values:
        rank2 = "TextRank"
    elif rank2 in df["KL"].values:
        rank2 = "KL"
    elif rank2 in df["T5"].values:
        rank2 = "T5"
    else:
        rank2 = "BART"    
    
    if rank3 in df["TextRank"].values:
        rank3 = "TextRank"
    elif rank3 in df["KL"].values:
        rank3 = "KL"
    elif rank3 in df["T5"].values:
        rank3 = "T5"
    else:
        rank3 = "BART"
        
    if rank4 in df["TextRank"].values:
        rank4 = "TextRank"
    elif rank4 in df["KL"].values:
        rank4 = "KL"
    elif rank4 in df["T5"].values:
        rank4 = "T5"
    else:
        rank4 = "BART"
    return rank1, rank2, rank3, rank4


@app.route('/submit', methods=['POST'])
def submit():
    # get user inputs
    rank1 = str(request.form['rank1'])
    rank2 = str(request.form['rank2'])
    rank3 = str(request.form['rank3'])
    rank4 = str(request.form['rank4'])
    rating = str(request.form['rating'])
    feedback = request.form['feedback']
    x = request.form['x']

    df = pd.read_csv('summaries.csv')
    df = df.astype(str)

    rank1, rank2, rank3, rank4 = mapper(rank1,rank2,rank3,rank4, df)
        
    # write data to csv
    with open('survey_data.csv', mode='a', newline='') as csvfile:
        fieldnames = ['Article','Rank1', 'Rank2', 'Rank3', 'Rank4','Rating', 'Feedback']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Article': x,'Rank1': rank1, 'Rank2': rank2, 'Rank3': rank3, 'Rank4': rank4, 'Rating': rating, 'Feedback': feedback})

    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)