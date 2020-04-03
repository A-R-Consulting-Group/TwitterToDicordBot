import tweepy
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
import time

keywords = ["GIVEAWAY","Giveaway","giveaway"]

cont = 0
sleepTime = 60 * 10
filename = 'links.txt'
webhook_Valhalla = 'https://discordapp.com/api/webhooks/671330429944594472/ltGgcznGuMX7D849k9CzOWrL5_Ec-D9R7_sfpXM1T1B3P_NTcCCRmDOaKfKs6I5uEuVE'
webhook_SnkrVandals = 'https://discordapp.com/api/webhooks/695387150920843305/lJv-uWFWHePUfOQZF4MurfmcBB7zFnI_5JoEpkDOwvpI58OEa3Y2V8rW6Ny5OjViTldc'

webhook_urls = [webhook_Valhalla, webhook_SnkrVandals]

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
#api = tweepy.API(auth)
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

def delete_links():
    with open(filename, "r") as f:
        lines = f.readlines()
        half = int(len(lines)/2)
    with open(filename, "w") as f:
        f.writelines(lines[half:])

# methods for user timelines
def get_links():
    timeline = api.home_timeline()
    for tweet in timeline:
        #print(tweet)
        text = tweet.text
        for keyword in keywords:
            if (text.find(keyword) != -1):
                link = "https://twitter.com/i/web/status/" + tweet.id_str
                check_link(link)
            else: 
                print("No Raffle found!")
            
def check_link(link):
    with open (filename, 'r') as rf:
        with open (filename, 'a') as af:
            read = rf.read()
            if link not in read:
                af.write("\n" + link)  
                send_raffle(link)
                print("Raffle sent!")
            else:
                print("No new link!")

#avatar_url= "http://i.imgur.com/faJ9n.jpg"
def send_raffle(link):
    webhook = DiscordWebhook(url=webhook_urls, username= "@NotifyGiveaway", content=link)
    response = webhook.execute()

while True:
    if (cont < 72):
        cont += 1
        get_links()
        time.sleep(sleepTime)
        print(cont)
    else:
        delete_links()
        cont = 0