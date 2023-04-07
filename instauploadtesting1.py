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

# Calculate the size of the quote text and position it in the center of the image
text_size = draw.textsize(quote, font=font)
text_position = ((image.size[0] - text_size[0]) / 2, (image.size[1] - text_size[1]) / 2)
print("size calculated")

# Draw the quote text on the image
draw.text(text_position, quote, fill=(255, 255, 255), font=font)
print("image draw")

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
auth_token = '0b0dd37814164cbcce2078e34c581014'
client = Client(account_sid, auth_token)


# Delete the .REMOVE File Frist
def DeleteFile(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        print("delted")
        message = client.messages.create(
            from_ = "+15673992184",
            to='+917219739402',
            body= "A new photo has been uploaded to Instagram..!!!")
        ##print(message.sid)
        ##print(account_sid , auth_token)
        print("Message Send")
    else:
        print("not exist")

DeleteFile("instaPhotos/fitness_quote.jpg.REMOVE_ME")
print("file deleted")






