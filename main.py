from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

def downloadVideo(link, id):
    print(f"Downloading video {id} from: {link}")
    cookies = {
        '_ga': 'GA1.2.1748110569.1680802165',
        '_gid': 'GA1.2.101389470.1680802165',
        '_gat_UA-3524196-6': '1',
    }

    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '_ga=GA1.2.1748110569.1680802165; _gid=GA1.2.101389470.1680802165; _gat_UA-3524196-6=1',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'OFZyTmM1',
    }
    
    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    print("STEP 5: Saving the video :)")
    mp4File = urlopen(downloadLink)
    # Feel free to change the download directory
    with open(f"videos/{id}-{videoTitle}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

def wtoFile(url):
    with open("downloaded.txt", "a") as wfile:
        wfile.write(url+'\n')
        wfile.close()
    
    

print("STEP 1: Open Chrome browser")
driver = webdriver.Edge()
# Change the tiktok link
driver.get("https://www.tiktok.com/@funnyvideo_____")
# https://www.tiktok.com/@funny_animals329
#https://www.tiktok.com/@dailyfunny.clips  -->Full vid wala
#https://www.tiktok.com/@funnyclips321  --->short clips wala
#https://www.tiktok.com/@funny_uuu
#https://www.tiktok.com/@caught.on.cameraa --> full 1 min funny human short
    

# IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
# to 60 seconds, just enough time for you to complete the captcha yourself.
time.sleep(5)

scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

print("STEP 2: Scrolling page")
while True:
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    if (screen_height) * i > scroll_height:
        break 
    if i>5:
        break

soup = BeautifulSoup(driver.page_source, "html.parser")
# this class may change, so make sure to inspect the page and find the correct class
videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper"})


print(f"STEP 3: Time to download {len(videos)} videos")
with open("downloaded.txt","r") as file:
    reader=file.readlines()
    for index, video in enumerate(videos):
        flag=0
        for line in reader:
            if(video.a["href"] in line):
                flag=1
                break
        if(flag==0):
            print(f"Downloading video: {index}")
            downloadVideo(video.a["href"], index)
            wtoFile(video.a["href"])
            time.sleep(10)
                