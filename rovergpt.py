from openai import AzureOpenAI
import os
import requests
import json
from PIL import Image

# NASA ROVER 
with open('nasakey.txt', 'r') as nasa_file:
    nasa_key = nasa_file.read().strip()

date = "2016-6-3"
# TO DO work out how to have the user input a date to update the rover pics on the website
url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={date}&api_key={nasa_key}"

response = requests.get(url)
data = response.json()
# print(data)

rover_img = data["photos"][0]["img_src"]
# print(rover_img)

rover_folder = 'static'
rover_img_dir = os.path.join(os.curdir, rover_folder)
if not os.path.isdir(rover_img_dir):
	os.mkdir(rover_img_dir)

# would like to save every image using a timestamp
rover_filename = 'Rover_Image.png'
rover_img_path = os.path.join(rover_img_dir, rover_filename)

rover_gen_image = requests.get(rover_img).content

with open(rover_img_path, 'wb') as file:
	file.write(rover_gen_image)

def get_rover_filename():
	return f"/{rover_folder}/{rover_filename}"

# DALLE

client = AzureOpenAI(
	api_key = os.getenv("AZURE_KEY"),
	api_version = "2023-12-01-preview",
	azure_endpoint = os.getenv("AZURE_ENDPOINT")
)

# generate an image using Dalle
prompt = "A highly detailed and futuristic speculative tool designed for survival on Mars. The image should only feature the tool in a visually striking Martian landscape, with no text, no logos, and no visible markings or symbols. Focus on intricate, realistic design details."

dalle_result = client.images.generate(
	model = "dalle3", 
	prompt = prompt,
	n=1
	)

# print(dalle_result)

# convert the dalle repsone to json
json_response = json.loads(dalle_result.model_dump_json())

dalle_folder= 'static'
# setting up a file path inside the current folder called images, where the dalle repsonses will be stored.
dalle_image_dir = os.path.join(os.curdir, dalle_folder)

# if this folder doesn't already exist, make a new one
if not os.path.isdir(dalle_image_dir):
	os.mkdir(dalle_image_dir)

# creating my file path 
# the path of the folder + the file name
dalle_filename = 'Dalle_Image.png'
image_path = os.path.join(dalle_image_dir, dalle_filename)
# get the url that openai gives us
image_url = json_response['data'][0]['url']
revised_prompt = json_response['data'][0]['revised_prompt']

# use the url to give me the actual image
dalle_gen_image = requests.get(image_url).content

# save the image in my images folder
with open(image_path, 'wb') as file:
	file.write(dalle_gen_image)

# this will have python open the image file - good for debugging and proof of concept
# image = Image.open(image_path)
# image.show()

def get_dalle_filename():
	return f"/{dalle_folder}/{dalle_filename}"

# makes the alt text the revised prompt
def get_prompt():
	return revised_prompt

# def get_date():
