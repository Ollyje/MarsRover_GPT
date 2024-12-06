from openai import AzureOpenAI
import os
import requests
import json
from PIL import Image

# NASA ROVER 
with open('nasakey.txt', 'r') as nasa_file:
    nasa_key = nasa_file.read().strip()


def get_rover_img_url(rover_date): # DATE IN FUNCTION # TO DO - check this ufnciton for getting the URL of the image, to then feed into gpt
	# TO DO - how can this varible become interactive?
	# TO DO work out how to have the user input a date to update the rover pics on the website
	url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?earth_date={rover_date}&api_key={nasa_key}"
	print(rover_date)
	response = requests.get(url)
	data = response.json()
	# print(data)


	rover_img_url = data["photos"][0]["img_src"]
	print (rover_img_url)
	bot_response = gpt_describe(rover_img_url)
	print(bot_response)
	# THE ISSUE IS BOT_RESPONSE
	new_dalle_img = make_dalle_img(bot_response)
	return new_dalle_img

# rover_folder = 'static'
# rover_img_dir = os.path.join(os.curdir, rover_folder)

# if not os.path.isdir(rover_img_dir):  
#     os.mkdir(rover_img_dir)

# # Would like to save every image using a timestamp
# rover_filename = 'Rover_Image.png'
# rover_img_path = os.path.join(rover_img_dir, rover_filename)

# # rover_gen_image = requests.get(rover_img).content

# with open(rover_img_path, 'wb') as file:  
#     file.write(rover_gen_image)

# def get_rover_filename():
#     return f"/{rover_folder}/{rover_filename}"  

# DALLE

client = AzureOpenAI(
	api_key = os.getenv("AZURE_KEY"),
	api_version = "2023-12-01-preview",
	azure_endpoint = os.getenv("AZURE_ENDPOINT")
)

dalle_folder= 'static'
# setting up a file path inside the current folder called images, where the dalle repsonses will be stored.
dalle_image_dir = os.path.join(os.curdir, dalle_folder)

# if this folder doesn't already exist, make a new one
if not os.path.isdir(dalle_image_dir):
	os.mkdir(dalle_image_dir)

def make_dalle_img(gpt_response): 
	# generate an image using Dalle
	# my dalle prompt will be the GPT output
	dalle_prompt = gpt_response

	dalle_result = client.images.generate(
		model = "dalle3", 
		prompt = dalle_prompt,
		n=1
		)
	# convert the dalle repsone to json
	json_response = json.loads(dalle_result.model_dump_json())
	# print(dalle_result)

	# creating my file path 
	# the path of the folder + the file name
	dalle_filename = 'Dalle_Image.png'
	image_path = os.path.join(dalle_image_dir, dalle_filename)
	# get the url that openai gives us
	image_url = json_response['data'][0]['url']
	# revised_prompt = json_response['data'][0]['revised_prompt']

	# use the url to give me the actual image
	dalle_gen_image = requests.get(image_url).content

	# save the image in my images folder
	with open(image_path, 'wb') as file:
		file.write(dalle_gen_image)

	return dalle_filename

# this will have python open the image file - good for debugging and proof of concept
# image = Image.open(image_path)
# image.show()

def get_dalle_filename():
	return f"/{dalle_folder}/{dalle_filename}"

# makes the alt text the revised prompt
# def get_prompt():
	# return revised_prompt


# CHATGPT
def gpt_describe(rover_img):
	messages = [
		{"role": "user", "content": [
		{"type": "text", "text": "Analyze the provided image captured by the Mars Rover. In no more than 1500 characters, describe the terrain, colors, textures, and notable features in detail. Then, based on the environmental conditions depicted in the image, write a short paragraph of speculative fiction about a tool or piece of equipment necessary for human survival on Mars. Include its purpose and how it is designed to adapt to the specific challenges shown in the image."},
		{"type": "image_url", 
		"image_url": f"{rover_img}"}
		]
	}
	]

	response = client.chat.completions.create(
		model = "gpt-4o",
		messages = messages,
		tools = functions,
		# auto means chatgpt decides when to use external functions
		tool_choice = "auto"
		)
	return response.choices[0].message.content

functions = [
	{
		"type": "function", 
		"function": {
			"name": "get_img_url",
			"description": "Gets the image url from the Mars Rover Api",
			"parameters": {
					# letting chatgpt know that it's geting key-value pairs
				"type": "object",
				"properties": {
					"rover_date": {
						"type": "string",
						"description": "The date of the Mars Rover image i want to look up"
					},

				},
				"required":["rover_date"]
			}

		}
	}
]

# # print(response.choices[0].message)
# response_message = response.choices[0].message 
# gpt_tools = response.choices[0].message.tool_calls

# if gpt_tools:
# 	available_functions = {
# 			"get_img_url": get_rover_img_url
# 	}

# 	messages.append(response_message)
# 	for gpt_tool in gpt_tools:
# 		function_name = gpt_tool.function.name
# 		function_to_call = available_functions[function_name]
# 		function_parameters = json.loads(gpt_tool.function.arguments)
# 		function_response = function_to_call(function_parameters.get('rover_date'))
# 		messages.append(
# 			{
# 				"tool_call_id": gpt_tool.id,
# 				"role": "tool",
# 				"name": function_name,
# 				"content": function_response
# 			}
# 		)
# 		second_response = client.chat.completions.create(
# 			model = "gpt-4o",
# 			messages=messages
# 		)
# 		print(second_response.choices[0].message.content)

# else:
# 	print(response.choices[0].message.content)
