from flask import Flask, render_template, request



app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

#get query from form box from an html file
@app.route('/output', methods=['POST'])
def output():
	query_list = request.form['query']
	print(query_list)
	#query_list string type turns into list type
	
	file = open("smallIndex.txt", "r")
	lines = file.readlines()
	outputResults = []
	outputResults = cosineScore(query_list)
	#loop through each word
	"""
	for word in query_list:
		word = word.strip() #remove spaces
		cosineScore()
		#go through small index
		for line in lines:
			#print("Line:", line.split()[0][0:-1])
			#first word in each index line is "str:", need to get rid of ":"
			if line.split()[0][0:-1].lower() == word.lower():
				#print("outputResults: ", line.split()[1:5])
				outputResults.append(line.split()[1:])
				break
	"""
	#print(outputResults)
	return render_template("output.html", output=outputResults)


import time
import ast
import collections

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

file = open("index.txt", "r")
# TF_IDFIndex = open("TF_IDFIndex.txt", "w")  # output file
lines = file.readlines()
numOfDocs = 55393


# line = "shaping: {0: [1, 1], 1: [1, 1]}"
def cosineScore(query: str) -> [str]:
	result = []
	result_dict = collections.defaultdict(int)
	first = []
	query = query.split(" ")
	for term in query:
		term = term.lower()
		for line in lines:
			word = line.split(":")[0]  # "shaping"
			if word != term:
				continue
			
			length = len(word) + 2
			
			strDict = line[length:]  # "{0: [1, 1], 1: [1, 1]}"
			wordDict = ast.literal_eval(strDict)  # converts str to dict; {0: [1, 1], 1: [1, 1]}
			
			# key = docID, value[0] = freq
			temp = {}
			temp_docID = []
			for key, value in wordDict.items():
				temp[key] = value[0] / docIDTotal[key]
				temp_docID.append(key)
			if first == []:
				first = temp_docID
			else:
				first = list(set(first) & set(temp_docID))
			result.append(temp)
	
	for tf_dict in result:
		for docID in first:
			result_dict[docID] += tf_dict[docID]
	
	top5result = []
	for i in range(5):
		key = max(result_dict, key=result_dict.get)
		top5result.append(key)
		del result_dict[key]
	
	top5result_url = []
	docID_map = open("docID_map.txt", "r")
	row = docID_map.readlines()
	for docID in top5result:
		top5result_url.append("".join(row[docID].strip().split(":")[1]+":"+row[docID].strip().split(":")[2]+"\n"))
	
	print(top5result_url)
	return "".join(top5result_url)


end = time.time()
print(end - start)

if __name__ == "__main__":
	app.run()
