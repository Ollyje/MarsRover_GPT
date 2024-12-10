from flask import Flask, render_template, request
from rovergpt import get_rover_img_url, get_dalle_image, gpt_describe #get_dalle_filename, get_rover_filename,

app = Flask(__name__, static_url_path = '/static')

default_date = 'yyyy-mm-dd'
default_rover_image = '/static/Rover_Image.png'
default_dalle_image = '/static/Dalle_Image.png'
@app.route('/')
def index():
	return render_template("index.html", date=default_date, rover_img_filepath=default_rover_image, dalle_img_filepath=default_dalle_image) # dalle_img_filepath=dalle_file, rover_img_filepath=rover_file)

@app.route('/', methods=['POST'])
def index_post():
# TO DO!!! work out this below, and how to make it interactive, see index
	user_date = request.form['req_date']
	rover_img_url = get_rover_img_url(user_date)
	dalle_img = get_dalle_image(rover_img_url)
	gpt_prompt = gpt_describe(rover_img_url)
	# user_prompt = request.form['req_prompt']
	# dalle_input = get_dalle_filename() # TO DO - i think these variables will go in these functions
	# rover_input = get_rover_filename()
	print(rover_img_url)
	print(dalle_img)
	return render_template('index.html', rover_img_filepath=rover_img_url, dalle_img_filepath=dalle_img, gpt_output=gpt_prompt)
