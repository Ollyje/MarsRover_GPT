from flask import Flask, render_template, request
from rovergpt import get_rover_img_url #get_dalle_filename, get_rover_filename,

app = Flask(__name__, static_url_path = '/static')

default_date = 'yyyy-mm-dd'

@app.route('/')
def index():
	# dalle_file = get_dalle_filename()
	# rover_file = get_rover_filename()
	return render_template("index.html") # dalle_img_filepath=dalle_file, rover_img_filepath=rover_file)

@app.route('/', methods=['POST'])
def index_post():
# TO DO!!! work out this below, and how to make it interactive, see index
	user_date = request.form['req_date']
	rover_img_url = get_rover_img_url(user_date)
	# user_prompt = request.form['req_prompt']
	# dalle_input = get_dalle_filename() # TO DO - i think these variables will go in these functions
	# rover_input = get_rover_filename()
	return render_template('index.html')