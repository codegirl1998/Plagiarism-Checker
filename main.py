from flask import Flask, render_template, request, url_for
import urllib
from urllib.parse import quote
from lxml import html
import requests
import string
import time
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters;


app = Flask(__name__)

@app.route('/')
def form():
    return render_template('input.html')

@app.route('/plagiarismChecker/', methods=['POST'])
def plagiarismChecker():
        text=request.form['text_to_check']
        if (text.lstrip().rstrip() == ''):
                return render_template('input.html')
        punkt_parameters = PunktParameters()
        sentence_splitter = PunktSentenceTokenizer(punkt_parameters)
        sentences = sentence_splitter.tokenize(text)
        probability_of_plagiarism = 0
        for a_sentence in sentences:
                time.sleep(0.1)
                content = list(filter(lambda x: x in string.printable, a_sentence))
                str1=''.join(content)
                print(str1)
                # temp=list(content)
                # print(str(temp))
                the_term = urllib.parse.quote('+' + '"' + str1 + '"')
                page = requests.get('https://www.bing.com/search?q='+the_term)
                print(page.url)
                if ((not "There are no results for" in page.text) and (not "No hay resultados para" in page.text) and (not "are no results for" in page.text)):
                    probability_of_plagiarism += 1;
        percent_plagiarised = str((probability_of_plagiarism / len(sentences)) * 100) + '%'
        return render_template('results.html', text=text, percent_plagiarised=percent_plagiarised)


if __name__ == "__main__":
    app.run(debug=True)
