#NLTK Summarisation Python Program
import nltk #Importing NLTK Library and its pre-requisite modules
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import heapq  # Import Heapq for Finding the Top N Sentences

def nltk_summariser(raw_text):
	stopWords = set(stopwords.words("english")) #Setting up the stopwords - in this case, english
	word_frequencies = {}  #Initialising the word frequencies method
	for word in nltk.word_tokenize(raw_text):  #Tokenising the text with a for loop
	    if word not in stopWords:
	        if word not in word_frequencies.keys():
	            word_frequencies[word] = 1
	        else:
	            word_frequencies[word] += 1

	maximum_frequncy = max(word_frequencies.values()) #Getting the maximum frequency of each word

	for word in word_frequencies.keys():  
	    word_frequencies[word] = (word_frequencies[word]/maximum_frequncy) #Normalising the word frequencies

	sentence_list = nltk.sent_tokenize(raw_text) #Tokenising the text into sentences
	sentence_scores = {}  #Initialising the sentence scores method with a for loop
	for sent in sentence_list:  
	    for word in nltk.word_tokenize(sent.lower()):
	        if word in word_frequencies.keys():
	            if len(sent.split(' ')) < 30: #Setting the maximum length of a sentence to be 30 words
	                if sent not in sentence_scores.keys():
	                    sentence_scores[sent] = word_frequencies[word]
	                else:
	                    sentence_scores[sent] += word_frequencies[word]



	summary_sentences = heapq.nlargest(20, sentence_scores, key=sentence_scores.get) #Getting the top 20 sentences

	summary = ' '.join(summary_sentences)  
	return summary