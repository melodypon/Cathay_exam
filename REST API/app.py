from flask import Flask,jsonify,render_template,request,redirect,render_template_string
from pymongo import MongoClient
import json
from bson.json_util import dumps
from bson.json_util import loads
import pandas as pd

conn = MongoClient()
db = conn.rent591
collection = db.rent591Taipei

app = Flask(__name__)

#get
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result.php", methods=['POST'])
def result():
	query = {}
	region = request.form['region']
	person = request.form['person']
	identity = request.form['identity']
	phone = request.form['phone']
	building_type = request.form['building_type']
	current_condition = request.form['current_condition']
	gender = request.form['gender']
	if region != "":
		query.update({"地區":region})
	if len(person)==1:
		query.update({"出租者":{"$regex":person+'..'}})
	elif person=="女性":
		query.update({"$or":[{"出租者":{"$regex":".小姐"}},{"出租者":{"$regex":".太太"}},{"出租者":{"$regex":".媽媽"}}]})
	elif person=="男性":
		query.update({"出租者":{"$regex":".先生"}})
	elif person != "":
		query.update({"出租者":person})
	if "非屋主" in identity:
		query.update({"$or":[{"出租者身份":"仲介"},{"出租者身份":"代理人"}]})
	elif identity != "":
		query.update({"出租者身份":identity})
	if phone != "":
		query.update({"聯絡電話":phone})
	if building_type != "":
		query.update({"型態":building_type})
	if current_condition != "":
		query.update({"現況":current_condition})
	if "男" in gender:
		query.update({"$or":[{"性別要求":"男女生皆可"},{"性別要求":"男生"},{"性別要求":{"$type":10}}]})
	records_fetched = collection.find(query)
	df = pd.DataFrame(data=records_fetched)
	try:
		df = df.drop(columns=["_id","url"])
	except:
		pass
	# return str(loads(dumps(records_fetched)))
	
	return render_template_string(df.to_html())


if __name__ == "__main__":
    app.run(debug=True)