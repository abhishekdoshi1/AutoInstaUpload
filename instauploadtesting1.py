from instabot import Bot
import os
import openai
import openai_secret_manager
import random
import cv2
import numpy as np
import requests
import json
from PIL import Image,ImageDraw,ImageFont,ImageOps
from io import BytesIO
from bs4 import BeautifulSoup
import PIL.Image
import urllib.request
from urllib.request import Request, urlopen
from twilio.rest import Client
import textwrap
import time


openai.api_key = os.environ['OPENAI_API_KEY']

prompt = (f"Generate a fitness quote.")
model = "text-davinci-002"

response = openai.Completion.create(
    engine=model,
    prompt=prompt,
    max_tokens=20,
    n=1,
    stop=None,
    temperature=0.5,
)

quote = response.choices[0].text.strip()

print(quote)


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
fitness_quotes = [
    "Sweat is fat crying.",
    "The only bad workout is the one that didn't happen.",
    "Success is what comes after you stop making excuses.",
    "Strength doesn't come from what you can do. It comes from overcoming the things you once thought you couldn't.",
    "The only way to do great work is to love what you do.",
    "Yoga is the journey of the self, through the self, to the self.",
    "Yoga is the art of getting lost in yourself.",
    "Yoga teaches us to cure what need not be endured and endure what cannot be cured.",
    "Yoga is not a religion. It is a science, science of well-being, science of youthfulness, science of integrating body, mind, and soul.",
    "Yoga is not about touching your toes, it is what you learn on the way down.",
    "Yoga is a light, which once lit will never dim. The better your practice, the brighter the flame.",
    "Yoga is the perfect opportunity to be curious about who you are.",
    "Yoga is not a work-out, it is a work-in. And this is the point of spiritual practice; to make us teachable; to open up our hearts and focus our awareness so that we can know what we already know and be who we already are.",
    "Yoga is not a hobby. It is a way of life.",
    "Yoga is not just repetition of few postures – it is more about the exploration and discovery of the subtle energies of life.",
    "Yoga is the fountain of youth. You’re only as young as your spine is flexible.",
    "Yoga is not about self-improvement, it’s about self-acceptance.",
    "Yoga is the practice of quieting the mind.",
    "Yoga is the dance of every cell with the music of every breath that creates inner serenity and harmony.",
    "Yoga is the journey of the self, to the self, through the self.",
    "Yoga is the space where flower blossoms.",
    "Yoga is a powerful vehicle for change. As you build strength, you start to believe in your own potential.",
    "Yoga is a mirror to look at ourselves from within.",
    "Yoga is a light, which once lit will never dim. The better your practice, the brighter your flame.",
    "Yoga is the perfect opportunity to be curious about who you are."
]
#quote = random.choice(fitness_quotes)

# Create a Pillow ImageDraw object and set font properties

font_size = int(image.size[1] * 0.07)
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
lines = split_lines(quote, font, text_width)
text_height = sum(font.getsize(line)[1] for line in lines)

#Border width
border = 20

# Calculate the position of the top-left corner of the text box

text_position = (border,(image.height))

#Create new image with original image and extended image for rectangle
new_img = Image.new("RGB", (image.width, image.height + text_height))

#Paste the original image onto new image
new_img.paste(image, (0, 0))

# Create a Pillow ImageDraw object
draw = ImageDraw.Draw(new_img)

#Draw the rectangle below the image
draw.rectangle((0,image.height,image.width,image.height+text_height),fill="#FFFF00",outline=None)



# Draw the quote text on the image, with text wrapping within the box width
for line in lines:
    line_width, line_height = font.getsize(line)
    draw.text((int(text_position[0] + (box_width - line_width) / 2), int(text_position[1])), line, fill=(0,0,0), font=font,stroke_width=1,text_color_bg=(255, 0, 0),align='center')
    text_position = (text_position[0], text_position[1] + line_height)

new_img = ImageOps.expand(new_img,border=border,fill='yellow')

#Name of the image
image_name = "fitness_quote" + str(time.time()) + ".png" 

#To decrease the opacity of image 255: max
new_img.putalpha(255)



# Save the image with the quote

new_img.save("instaPhotos/"+image_name)
print("image saved")


## Now Uploaded onto instagram

#Bot started
bot = Bot()

time.sleep(2.4)

#Bot Logged into instagram with username and password
bot.login(username="Go_DeepInto_Motivation", password="MotivationalArea@123")

#time.sleep(retry)

#find the folder 
dir_image = "instaPhotos/"

bot.upload_photo(dir_image+image_name , caption=quote)

#uploaded into instagram
#for image in os.listdir(dir_image):
 #bot.upload_photo(dir_image+image , caption=quote)


print("image uploaded")

bot.logout()

account_sid = 'ACe9e2d6401acf4b4947ad1361148780f1'
auth_token = '2b47c92b5d5b9fbf641d624c790be1b2'
client = Client(account_sid, auth_token)


#Delete the .REMOVE File Frist

'''def DeleteFile(filepath):
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
        print("not exist")'''

#DeleteFile("instaPhotos/fitness_quote.jpg.REMOVE_ME")
#print("file deleted")





