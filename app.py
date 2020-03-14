from flask import Flask, render_template, request
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance as dis
from decimal import *
import cProfile
import re
import time
import math
import ast
import time
import ast

app = Flask(__name__)
global topNum
@app.route("/")
def home():
	return render_template("home.html")

#get query from form box from an html file
"""
@app.route('/home', methods=['POST'])
def topNumOutput():
	num = request.form['query_num']
	topNum = max(num, 1)
	print(num)
	#return render_template("home.html")
"""
#get query from form box from an html file
@app.route('/output', methods=['POST'])
def output():
	global topNum
	topNum = 10
	if request.form['query_num'] >= "1":
		topNum = int(request.form['query_num'])

	query_list = request.form['query']
	print(query_list)
	#query_list string type turns into list type
	
	outputResults = cosineScore(query_list)
	
	#print(outputResults)
	return render_template("output.html", output=outputResults)





print("starting")
start = time.time()  # for measuring time

# Create dict where key=docID, value= total terms
docID_terms = open("docID_terms.txt", "r")
lines = docID_terms.readlines()
docIDTotal = {}
for line in lines:
	line = line.strip().split(":")
	docID = int(line[0])
	total = int(line[1])
	docIDTotal[docID] = total
	
# Create dict where key=docID, value= total terms
docID_map = open("docID_map.txt", "r")
lines = docID_map.readlines()
docIDMap = {}
for line in lines:
	index_colon = line.strip(", \n").index(":")
	docID = line[0:index_colon]
	url = line[index_colon+1:]
	docIDMap[docID] = url


numOfDocs = 39059

# token:docID[score],docID[score]
token_normalized = {}
# token:docID,docID
token_docID = {}
# token:[normalized,normalized]
token_only_normalized = {}


# save token_normalized into memory
# key = word, value= docID[TF-IDF score],docID[TF_IDF score]
def get_normalized_and_docID():
	file = open("Token_TFIDF_Normalized.txt", "r")
	lines = file.readlines()
	
	for line in lines:
		line = line.strip(", \n")
		index_colon = line.index(":")
		token = line[0:index_colon]
		try:
			token_normalized[token] = ast.literal_eval(line[index_colon + 1:])
		except:
			continue
	file.close()
	
	file = open("Token_docID.txt", "r")
	lines = file.readlines()
	
	for line in lines:
		line = line.strip(", \n")
		index_colon = line.index(":")
		token = line[0:index_colon]
		token_docID[token] = line[index_colon + 1:].split(",")
	file.close()
	
	file = open("Token_Normalized.txt", "r")
	lines = file.readlines()
	
	for line in lines:
		line = line.strip(", \n")
		index_colon = line.index(":")
		token = line[0:index_colon]
		token_only_normalized[token] = line[index_colon + 1:].strip(" \n").split(" ")
	file.close()
get_normalized_and_docID()


def cosineScore(query: [str]) -> [str]:
	# token:score
	all_token_score = {}
	# token:docID, docID
	all_token_docID = []
	new_query = []
	for token in query:
		try:
			if token_docID[token]:
				if not all_token_docID:
					all_token_docID.append(token_docID[token])
				else:
					all_token_docID = np.intersect1d(all_token_docID[0], token_docID[token])
				new_query.append(token)
		except:
			try:
				if token_docID[token.lower()]:
					if not all_token_docID:
						all_token_docID.append(token_docID[token])
					else:
						all_token_docID = np.intersect1d(all_token_docID[0], token_docID[token])
					new_query.append(token)
			except:
				continue
	
	if not all_token_docID:
		return []
	
	# print("og", len(all_token_docID))
	# [docID, docID]
	query_length = len(new_query)
	if 1 < query_length:
		all_token_docID = ",".join(list(set(all_token_docID[0]).intersection(*all_token_docID))).split(",")
	else:
		all_token_docID = all_token_docID[0]
	# print("all_token_docID", len(all_token_docID))
	
	tfidf_query = []
	for token in new_query:
		tfidf_query.append(
			(new_query.count(token) / query_length) * math.log((1 + numOfDocs) / len(token_docID[token])))
	
	# normalizing code; go thru all_tf_idf
	if len(tfidf_query) > 1:
		old_min = min(tfidf_query)
		old_range = max(tfidf_query) - old_min
		new_min = 0
		new_range = 1 + 0.9999999999
		# technically, range is 0 to 1.99999; +0.999 to prevent the top bucket 1 to e overrepresented
		tfidf_query = [[float((n - old_min) / old_range * new_range + new_min) for n in tfidf_query]]
	
	else:
		tfidf_query = [[1]]
	
	# docID:[score,score]
	all_scores_keys = []
	all_scores_values = []
	
	for docID in all_token_docID:
		temp_scores = []
		for token in new_query:
			# index_docID = token_docID[token].index(docID)
			# score = token_only_normalized[token][token_docID[token].index(docID)]
			temp_scores.append(float(token_normalized[token][int(docID)]))
		all_scores_keys.append(docID)
		all_scores_values.append(temp_scores)
	
	cosine_result = cosine_similarity(tfidf_query, all_scores_values)
	
	
	top_results = []
	for i in range(topNum):
		max_index = np.argmax(cosine_result)
		cosine_result = np.delete(cosine_result, max_index)
		top_results.append(docIDMap[all_scores_keys[max_index]])
		del all_scores_values[max_index]
		del all_scores_keys[max_index]
	# print("allscroes:", all_scores)
	
	return "".join(top_results)


end = time.time()
print(end - start)

if __name__ == "__main__":
	app.run()
