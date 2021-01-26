from flask import Flask, request, render_template, send_file, send_from_directory
from geopy.geocoders import ArcGIS as ag
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
	if request.method == 'POST':
		global file
		file = request.files["file_base"]
		try:
			df = pd.read_csv(file)
			if "Address" not in df.columns and "address" not in df.columns:
				return render_template("index.html", 
				text = "Please upload a csv file with an address column!")	
			nom = ag()
			df["Coordinates"] = df["Address"].apply(nom.geocode)
			df["Latitude"] = df["Coordinates"].apply(lambda x: x.latitude)
			df["Longitude"] = df["Coordinates"].apply(lambda x: x.longitude)
			df.drop("Coordinates", 1, inplace=True)
			df.to_csv("modified_" + file.filename)
		except UnicodeDecodeError:
			return render_template("index.html", 
				text = "Please upload a valid csv file!")
	return render_template("index.html", tables=[df.to_html()], 
		btn="download.html")

@app.route("/download")
def download():
	return send_file("modified_" + file.filename, attachment_filename="yourfile.csv",
		 as_attachment=True)

if __name__ == "__main__":
	app.debug = True
	app.run()