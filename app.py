from flask import Flask, render_template, request
from rovergpt import get_dalle_filename, get_prompt, get_rover_filename, get_rover_img_url

app = Flask(__name__, static_url_path = '/static')

default_date = 'yyyy-mm-dd'
default_prompt = 'default prompt'

@app.route('/')
def index():
	dalle_file = get_dalle_filename()
	prompt = get_prompt()
	rover_file = get_rover_filename()
	return render_template("index.html", dalle_img_filepath=dalle_file, prompt=prompt, rover_img_filepath=rover_file)

@app.route('/', methods=['POST'])
def index_post():
# TO DO!!! work out this below, and how to make it interactive, see index
	# user_date = request.form['req_date']
	# user_prompt = request.form['req_prompt']
	dalle_input = get_dalle_filename(user_prompt) # TO DO - i think these variables will go in these functions
	rover_input = get_rover_filename(user_date)
	return render_template('index.html')