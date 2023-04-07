from instabot import Bot
import os
import openai
import openai_secret_manager
import random
import cv2
import numpy as np
import requests
import json
from PIL import Image,ImageDraw, ImageFont
from io import BytesIO
from bs4 import BeautifulSoup
import PIL.Image
import urllib.request
from urllib.request import Request, urlopen
from twilio.rest import Client
import textwrap




#Authenticate with OpenAI API   

secrets = os.getenv("openai")
openai.api_key = "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"

#model_engine = "text-davinci-002" # set the GPT-3 model to use

# Define the prompt for the GPT-3 model
#msg = "bhagavad gita"
prompt = "give me a quote of fitness"


# Define the GPT-3 model and parameters
model_engine = "text-davinci-003"
max_tokens = 1024
temperature = 0.5

completions = openai.Completion.create(
  engine=model_engine,
   prompt=prompt,
   max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.7,
)

message = completions.choices[0].text.strip() #quote stored in message variable

print(message)


# Define the endpoint URL and parameters
url = "https://api.unsplash.com/photos/random"
params = {
    "query": "fitness",
    "orientation": "landscape",
    "client_id": "Urm2K_WBtpYv2l500desi8UMDvdhjAz5t8wohl2qPvA"
}

# Send a GET request to the API endpoint
response = requests.get(url, params=params)

# Parse the JSON response and extract the image URL
data = json.loads(response.text)
image_url = data["urls"]["regular"]

# Download the image and create a Pillow Image object
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))

# Generate a random fitness quote
fitness_quotes = message
quote = fitness_quotes #random.choice(fitness_quotes)

# Create a Pillow ImageDraw object and set font properties
draw = ImageDraw.Draw(image)
font_size = int(image.size[1] * 0.05)
font = ImageFont.truetype("arial.ttf", font_size)
print("font properties created")

# Define the text and box widths for text wrapping
text_width = int(image.size[0] * 0.8)
box_width = int(image.size[0] * 0.9)

# Define a function to split the quote into lines that fit within the box width
def split_lines(text, font, width):
    words = text.split()
    lines = []
    current_line = words[0]
    for word in words[1:]:
        if font.getsize(current_line + ' ' + word)[0] < width:
            current_line += ' ' + word
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    return lines

# Split the quote into lines and calculate the total height of the text
lines = split_lines(quote, font, box_width)
text_height = sum(font.getsize(line)[1] for line in lines)

# Calculate the position of the top-left corner of the text box
text_position = ((image.size[0] - box_width) / 2, (image.size[1] - text_height) / 2)

# Draw the quote text on the image, with text wrapping within the box width
for line in lines:
    line_width, line_height = font.getsize(line)
    draw.text((text_position[0] + (box_width - line_width) / 2, text_position[1]), line, fill=(255, 255, 255), font=font)
    text_position = (text_position[0], text_position[1] + line_height)

# Save the image with the quote
image.save("instaPhotos/fitness_quote.jpg")
print("image saved")



## Now Uploaded onto instagram

#Bot started
bot = Bot()

#Bot Logged into instagram with username and password
bot.login(username="testpycode", password="Satara@123")

#find the folder 
dir_image = "instaPhotos/"

#uploaded into instagram
for image in os.listdir(dir_image):
 bot.upload_photo(dir_image + image , caption=message)


print("image uploaded")

account_sid = 'ACe9e2d6401acf4b4947ad1361148780f1'
auth_token = '2b47c92b5d5b9fbf641d624c790be1b2'
client = Client(account_sid, auth_token)


    #Delete the .REMOVE File Frist

def DeleteFile(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        print("delted")
##        message = client.messages.create(
##            from_ = "whatsapp:+15673992184",
##            to='whatsapp:+918888456211',
##            body= "A new photo has been uploaded to Instagram..!!!")
        ##print(message.sid)
        ##print(account_sid , auth_token)
        print("Message")
    else:
        print("not exist")

DeleteFile("instaPhotos/fitness_quote.jpg.REMOVE_ME")
print("file deleted")





