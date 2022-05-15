from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request

#Import NLP Packages
from spacy_summarisation import text_summariser
from nltk_summarisation import nltk_summariser
from gensim.summarization import summarize

#Import Time Package
import time

#Import Default NLP Model
import spacy
nlp = spacy.load("en_core_web_sm")

#App Name
app = Flask(__name__)

# Web Scraping Pkg for URL
from bs4 import BeautifulSoup
# From urllib.request import urlopen
from urllib.request import Request, urlopen

# Sumy NLP Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Sumy Function to Summarise Text
def sumy_summary(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summariser = LexRankSummarizer()
	summary = lex_summariser(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result


# Reading Time Function
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime

# Read Text data From a Url
def get_text(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	#Finds all the paragraph tags in the page of the url and stores them in a list
	fetched_text = ''.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

#Functions
@app.route('/')
def index():
	return render_template('index.html')


@app.route('/analyse',methods=['GET','POST'])
def analyse():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		#Summarisation
		final_summary = text_summariser(rawtext)
		#Reading Time Check
		final_reading_time = readingTime(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

@app.route('/analyse_url',methods=['GET','POST'])
def analyse_url():
	start = time.time()
	if request.method == 'POST':
		#Get the URL from the form
		raw_url = request.form['raw_url']
		rawtext = get_text(raw_url)
		#Reading Time Check
		final_reading_time = readingTime(rawtext)
		final_summary = text_summariser(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)



@app.route('/compare_summary')
def compare_summary():
	return render_template('compare_summary.html')

@app.route('/comparer',methods=['GET','POST'])
def comparer():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary_spacy = text_summariser(rawtext)
		summary_reading_time = readingTime(final_summary_spacy)
		# Gensim Summariser
		final_summary_gensim = summarize(rawtext)
		summary_reading_time_gensim = readingTime(final_summary_gensim)
		# NLTK
		final_summary_nltk = nltk_summariser(rawtext)
		summary_reading_time_nltk = readingTime(final_summary_nltk)
		# Sumy
		final_summary_sumy = sumy_summary(rawtext)
		summary_reading_time_sumy = readingTime(final_summary_sumy) 

		end = time.time()
		final_time = end-start
	return render_template('compare_summary.html',ctext=rawtext,final_summary_spacy=final_summary_spacy,final_summary_gensim=final_summary_gensim,final_summary_nltk=final_summary_nltk,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time,summary_reading_time_gensim=summary_reading_time_gensim,final_summary_sumy=final_summary_sumy,summary_reading_time_sumy=summary_reading_time_sumy,summary_reading_time_nltk=summary_reading_time_nltk)



@app.route('/about')
def about():
	return render_template('about.html')

if __name__ == '__main__':
	app.run(debug=True)
