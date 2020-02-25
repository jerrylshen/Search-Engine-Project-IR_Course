from flask import Flask, render_template, request



app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html")

#get query from form box from an html file
@app.route('/output', methods=['POST'])
def output():
	query_list = [request.form['query']]
	#print(type(query_list))
	#query_list string type turns into list type
	
	file = open("smallIndex.txt", "r")
	lines = file.readlines()
	outputResults = []
	
	#loop through each word
	for word in query_list:
		word = word.strip() #remove spaces
		
		#go through small index
		for line in lines:
			#print("Line:", line.split()[0][0:-1])
			#first word in each index line is "str:", need to get rid of ":"
			if line.split()[0][0:-1].lower() == word.lower():
				#print("outputResults: ", line.split()[1:5])
				outputResults.append(line.split()[1:])
				break
	#print(outputResults)
	return render_template("output.html", output=outputResults)
"""
@app.route("/charts")
def charts():
	return render_template("charts.html")

@app.route("/sectors")
def sectors_view():
	fig = create_figure()
	#img = io.BytesIO()  # create the buffer
	fig = plt.gcf()
	#/home/jerrylshen/stock_scraper/
	fig.savefig('/home/jerrylshen/stock_scraper/static/plot.png', dpi=400)

	meta_data = sectors.Sectors().get_meta()
	return render_template('sectors.html',  meta_data=meta_data)

def create_figure():
	fig = Figure()
	df = sectors.Sectors().create_sector_dataframe()
	df.plot(kind='bar')
	plt.axhline(0, c='k', linewidth=0.5)
	plt.axis("tight")
	plt.title("Real-Time Performance of the Day")
	plt.xticks([])
	plt.legend(bbox_to_anchor=(1.04, 1), loc="upper left", prop={'size': 8, 'family': 'DejaVu Sans Mono'})
	
	plt.tight_layout()
	return fig

@app.route("/earnings")
def earnings():
	return render_template("earnings.html")

@app.route("/insider_trading")
def insider_trading():
	return render_template("insider_trading.html")

@app.route('/output_insider_trading', methods=['POST'])
def output_insider_trading():
	company = request.form['company']
	company = insider_trading_data.InsiderTrading(company)
	output = company.output_data()
	
	return render_template("output_insider_trading.html", output=output)

@app.route("/updates")
def updates():
	return render_template("updates.html")

@app.route("/about")
def about():
	return render_template("about.html")
"""

if __name__ == "__main__":
	app.run()
