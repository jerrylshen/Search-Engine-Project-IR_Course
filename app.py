from flask import Flask, render_template, request
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import math
import ast
import collections
from nltk.stem import PorterStemmer

app = Flask(__name__)
global topNum
global docIDTotal
global docIDMap
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
	url = line[index_colon + 1:]
	docIDMap[docID] = url

# token:docID[score],docID[score]
global token_normalized
token_normalized = {}
# token:docID,docID
global token_docID
token_docID = {}
# token:[normalized,normalized]
global token_only_normalized
token_only_normalized = {}
# {docID : pagerank_score}
global pagerank
pagerank = {}
global PAGERANK_DOC
PAGERANK_DOC = "pagerank.txt"
global numOfDocs
numOfDocs = 39059
global ps
ps = PorterStemmer()


@app.route("/")
def home():
	return render_template("home.html")


# get query from form box from an html file
@app.route('/output', methods=['POST'])
def output():
	global topNum
	topNum = 10
	ps = PorterStemmer()
	
	if request.form['query_num'] >= "1":
		topNum = int(request.form['query_num'])
	
	query_list = request.form['query'].split()
	query_list = [ps.stem(i) for i in query_list]
	print(query_list)
	# query_list string type turns into list type
	# print("HoutputdocID", token_docID)
	outputResults = cosineScore(query_list)
	
	# print(outputResults)
	return render_template("output.html", output=outputResults)


# save token_normalized into memory
# key = word, value= docID[TF-IDF score],docID[TF_IDF score]
def get_normalized_and_docID():
	global token_normalized
	global token_docID
	global token_only_normalized
	global PAGERANK_DOC
	global pagerank
	
	file = open("Token_TFIDF_Normalized.txt", "r")
	lines = file.readlines()
	print("part1")
	for line in lines:
		line = line.strip(", \n")
		index_colon = line.index(":")
		token = line[0:index_colon]
		token_normalized[token] = ast.literal_eval(line[index_colon + 1:])
	
	file.close()
	print("part2")
	if os.path.isfile("Token_docID.txt"):
		with open("Token_docID.txt", "r") as f:
			for line in f:
				line = line.strip('\n').split()
				token = line[0]
				token_docID[token] = [i for i in line[1:]]
	print("part3")
	if os.path.isfile("Token_Normalized.txt"):
		with open("Token_Normalized.txt", "r") as f:
			for line in f:
				line = line.strip('\n').split()
				token = line[0]
				token_only_normalized[token] = [i for i in line[1:]]
	print("part4")
	if os.path.isfile(PAGERANK_DOC):
		with open(PAGERANK_DOC, "r") as f:
			for line in f:
				index = line.split()[0]
				score = line.split()[1]
				pagerank[int(index)] = float(score)


get_normalized_and_docID()


def cosineScore(query: [str]) -> [str]:
	global token_normalized
	global token_docID
	global token_only_normalized
	global PAGERANK_DOC
	global pagerank
	global all_token_docID
	# token:score
	all_token_score = {}
	# token:docID, docID
	all_token_docID = set()
	new_query = []
	# print("docIDL", token_docID)
	#print(token_docID)
	for token in query:
		if token in token_docID:
			if all_token_docID:
				all_token_docID = all_token_docID.intersection(token_docID[token])
			else:
				all_token_docID.update(token_docID[token])
			new_query.append(token)
		
		elif token.lower() in token_docID:
			if all_token_docID:
				all_token_docID = all_token_docID.intersection(token_docID[token.lower()])
			else:
				all_token_docID.update(token_docID[token])
			new_query.append(token)
	
	if not all_token_docID:
		return []
	
	query_length = len(new_query)
	tfidf_query = []
	tfidf_query_t = []
	for token in new_query:
		tfidf_query_t.append((new_query.count(token) / query_length))
	
	# normalizing code; go thru all_tf_idf
	if len(tfidf_query_t) == 1:
		tfidf_query = [[1]]
	else:
		tfidf_query.append(tfidf_query_t)
	
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
	
	count = 0
	for i in all_scores_keys:
		cosine_result[0][count] = pagerank[int(i)] * cosine_result[0][count]
		count += 1
	
	top_results = []
	size_result = len(cosine_result[0])
	for i in range(topNum):
		if i > size_result - 1:
			break
		max_index = np.argmax(cosine_result)
		cosine_result = np.delete(cosine_result, max_index)
		top_results.append(docIDMap[all_scores_keys[max_index]])
		del all_scores_values[max_index]
		del all_scores_keys[max_index]
	# print("allscroes:", all_scores)
	
	return "".join(top_results)


if __name__ == "__main__":
	print("start")
	app.run()
	print("end")