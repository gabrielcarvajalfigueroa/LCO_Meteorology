import requests

from bs4 import BeautifulSoup
import pandas as pd
import time
from io import BytesIO
from PIL import Image, ImageDraw
from datetime import datetime, timedelta

import os

# os.getcwd() :
#/home/gcarvajal/LCO_Meteorology/meteorologyProject

def make_gif():
    print("sdffffffffdsfsfsd",os.path.abspath(os.path.join(os.path.dirname( __file__ ), '../../..', 'static/dpd/assets/dashboards/Dash_Apps/meteorology_subplots')))

    print("------>",os.getcwd())

    print(os.listdir('static/dpd/assets/dashboards/Dash_Apps/meteorology_subplots'))
    
    list_of_files = os.listdir('static/dpd/assets/dashboards/Dash_Apps/meteorology_subplots/imgs')
    full_path = ["static/dpd/assets/dashboards/Dash_Apps/meteorology_subplots/imgs/{0}".format(x) for x in list_of_files]

    
    #if len(list_of_files) == 3):
    #    oldest_file = min(full_path, key=os.path.getctime)
    #    shutil.rmtree(oldest_file) 
    

    # URL of the satellite website to scrape
    url = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/'

    # Send an HTTP GET request to the website
    response = requests.get(url)

    # Parse the HTML code using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')


    # Extract the relevant information from the HTML code
    # The date follows this format YYYY0DDHHMM
    # Example: 20240171150
    # TODO: Check why the datetime has a 3 hour diference
    today = datetime.now() - timedelta(hours=3, minutes=0)

    todays_day = today.strftime("%d")

    todays_hour = today.strftime("%H%M")

    folder_name = 'static/dpd/assets/dashboards/Dash_Apps/meteorology_subplots/imgs/' + today.strftime("%Y_%m_%d_%H:%M")

    pics = []
    for row in soup.find_all('a', href=True):

        link_to_img = row['href']
        date_in_tag = link_to_img[:11]

        # Conditionals explanation
        # -------------------------
        # date_in_tag.isnumeric(): the are values that are not numbers after the scrape
        # 5424: because it only works with the 5424x5424 imgs
        # todays_day: Filters only the pictures from today
        # todays_hour: it helps to get the data within 3 hours aprox
        if date_in_tag.isnumeric() and link_to_img[35:39] == "5424" and date_in_tag[5:7] == todays_day and  int(date_in_tag[7:11]) > int(todays_hour):
            pics.append([date_in_tag, link_to_img])
            

    # Store the information from the web scraping in a pandas dataframe
    # The dataframe should contain around 15 rows
    df = pd.DataFrame(pics, columns=['Date', 'Link_to_img'])

    #Check the directory name exist or not
    if os.path.isdir(folder_name) == False:
        #Create the directory
        os.mkdir(folder_name)


    #font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf', size = 19)

    # Start processing the images
    image_list = []
    print("Downloading images . . .")
    img_number = 1
    for index, row in df.iterrows():
        url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/" + row['Link_to_img']
        
        response = requests.get(url)

        image = Image.open(BytesIO(response.content))
        imageZoom = image.crop((2801, 4105, 3001, 4305))
        imageBigZoom = imageZoom.resize((250, 250))
        image3018 = image.resize((3018, 3018))
        
        image680 = image3018.crop((1274, 2000, 1954, 2680))
        image680.paste(imageBigZoom, (430, 430))    

        rectangle = Image.new('RGB', (122, 17))
        tDraw = ImageDraw.Draw(rectangle, 'RGB')
        tDraw.rectangle([(0, 0), (122, 17)], fill=(0, 0, 0))

        image680.paste(rectangle, (0, 663))
        del tDraw

        draw = ImageDraw.Draw(image680)
        draw.text((1, 661), row['Date'], fill=(255, 255, 255))
        draw.line([(430, 430), (430, 679), (679, 679), (679, 430), (430, 430)], (255, 255, 255))
        draw.ellipse([(344, 342), (348, 346)], fill='red')
        draw.ellipse([(564, 550), (576, 562)], outline='red')
        del draw

        # Appends the cropped image
        image_list.append(image680)

        #Saves image to folder
        image680.save(folder_name + '/' + row['Date'] + ".png")

        print("Image", img_number, ", downloaded succesfully")
        img_number += 1


    print("Starting gif creation . . .")
    # Save the first image as a GIF file
    image_list[0].save(
                'static/dpd/assets/dashboards/Dash_Apps/meteorology_subplots/sa4tanim.gif',
                save_all=True,
                append_images=image_list[1:], # append rest of the images
                duration=100, # in milliseconds
                loop=0)    
    

'''
    # URL of the satellite website to scrape
    url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/"

    # Send an HTTP GET request to the website
    response = requests.get(url)

    # Parse the HTML code using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')


    # Extract the relevant information from the HTML code
    # The date follows this format YYYY0DDHHMM
    # Example: 20240171150
    # TODO: Check why the datetime has a 3 hour diference
    today = datetime.now() - timedelta(hours=3, minutes=0)

    todays_day = today.strftime("%d")

    todays_hour = today.strftime("%H%M")

    pics = []
    for row in soup.find_all('a', href=True):

        link_to_img = row['href']
        date_in_tag = link_to_img[:11]

        # Conditionals explanation
        # -------------------------
        # date_in_tag.isnumeric(): the are values that are not numbers after the scrape
        # 5424: because it only works with the 5424x5424 imgs
        # todays_day: Filters only the pictures from today
        # todays_hour: it helps to get the data within  3 hours aprox
        if date_in_tag.isnumeric() and link_to_img[35:39] == "5424" and date_in_tag[5:7] == todays_day and  int(date_in_tag[7:11]) > int(todays_hour):
            pics.append([date_in_tag, link_to_img])            

            

    # Store the information from the web scraping in a pandas dataframe
    # The dataframe should contain around 15 rows
    df = pd.DataFrame(pics, columns=['Date', 'Link_to_img'])

    # Start processing the images
    image_list = []
    print("Downloading images . . .")
    print(df)
    img_number = 1
    for index ,row in df.iterrows():
        print("before url")
        url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/" + row['Link_to_img']
        
        response = requests.get(url)

        print("after request")
        image = Image.open(BytesIO(response.content))
        imageZoom = image.crop((2801, 4105, 3001, 4305))
        imageBigZoom = imageZoom.resize((250, 250))
        image3018 = image.resize((3018, 3018))
        
        image680 = image3018.crop((1274, 2000, 1954, 2680))
        image680.paste(imageBigZoom, (430, 430))

        draw = ImageDraw.Draw(image680)    
        draw.line([(430, 430), (430, 679), (679, 679), (679, 430), (430, 430)], (255, 255, 255))
        draw.ellipse([(344, 342), (348, 346)], fill='red')
        draw.ellipse([(564, 550), (576, 562)], outline='red')

        # Appends the cropped image
        image_list.append(image680)
        print("Image", img_number, ", downloaded succesfully")
        img_number += 1


    print("Starting gif creation . . .")
    print("OS CWD", os.getcwd())
    # Save the first image as a GIF file
    image_list[0].save(
                'dashboards/Dash_Apps/test_data/satanim.gif',
                save_all=True,
                append_images=image_list[1:], # append rest of the images
                duration=100, # in milliseconds
                loop=0)    
    '''                