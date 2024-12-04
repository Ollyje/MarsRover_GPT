from flask import Flask, render_template, request
from rovergpt import get_dalle_filename, get_prompt, get_rover_filename

app = Flask(__name__, static_url_path = '/static')

@app.route('/')
def index():
	dalle_file = get_dalle_filename()
	prompt = get_prompt()
	rover_file = get_rover_filename()
	return render_template("index.html", dalle_img_filepath=dalle_file, prompt=prompt, rover_img_filepath=rover_file)
