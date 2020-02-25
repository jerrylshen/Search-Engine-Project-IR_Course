from requests import get



class InsiderTrading:
	def __init__(self, company):
		self.company = company.upper()
	
	def get_insider_trading_data(self):
		url = "https://api.unibit.ai/api/insidertrading/TICKER?AccessKey=QpFJ7orXOJo3lgTzIX2UtaE2csyJMPqM"
		new_url = url.replace("TICKER", self.company)
		#print("url", new_url)
		response = get(new_url).json()
		
		return response
	
	
	def output_data(self):
		response = self.get_insider_trading_data()["Insider Transaction"]
		output_text = ""
		#print("response", response)
		for trade in response:
			
			date = trade["trade_date"]
			#print("date",date)
			name = trade["insider_name"]
			title = trade["insider_title"]
			type = trade["trade_type"]
			price = trade["price"]
			quantity = trade["qty"]
			owned = trade["owned"]
			value = trade["value"]
			
			row1 = ["Date: "  + date,  "Price:"     + price]
			row2 = ["Name: "  + name,  "Quantity: " + quantity]
			row3 = ["Title: " + title, "Owned: "    + owned]
			row4 = ["Type: "  + type,  "Value: "    + value]
			
			"""
			if type[0] == "S":
				type = '<p class="sale">' + type + "</p>"
			else:
				type = '<p class="purchase">' + type + "</p>"
			"""

			output_text = output_text + "\n" + \
			              ('{:30s} {:35s}'.format(row1[0], row1[1])) + "\n" + \
			              ('{:30s} {:35s}'.format(row2[0], row2[1])) + "\n" + \
			              ('{:30s} {:35s}'.format(row3[0], row3[1])) + "\n" + \
			              ('{:30s} {:35s}'.format(row4[0], row4[1])) + "\n"
			
			#print(output_text)
		
		return output_text
