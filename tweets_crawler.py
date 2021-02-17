from threading import Thread
from collections import deque
from twython import TwythonStreamer
from requests.exceptions import ChunkedEncodingError
from config import * #import the file with the authentication keys
import gmplot



#create class TwitterStream
class TwitterStream(TwythonStreamer):

    def __init__(self, consumer_key, consumer_secret, token, token_secret, tqueue):
        self.tweet_queue = tqueue
        super(TwitterStream, self).__init__(consumer_key, consumer_secret, token, token_secret)

    def on_success(self, data):
        if 'text' in data:
            self.tweet_queue.append(data)

    def on_error(self, status_code, data):
        print(status_code)
        #  to stop trying to get data because of the error
        self.disconnect()



def stream_tweets(tweets_queue):
    
    try:
        stream = TwitterStream(APP_KEY,APP_SECRET,OAUTH_TOKEN, OAUTH_TOKEN_SECRET, tweets_queue)
        # filter by location
        stream.statuses.filter(locations=f"{LONG_MIN},{LAT_MIN},{LONG_MAX},{LAT_MAX}")
        stream.statuses.sample(language='en')
    except ChunkedEncodingError:
        # Sometimes the API sends back one byte less than expected which results in an exception in the
        # current version of the requests library
        stream_tweets(tweet_queue)

def process_tweets(tweets_queue):
    
    tweet=[]
    i=0
    while True:
        if len(tweets_queue) > 0:
            i+=1
            if i>1000: # stops if it found more than 1000 tweets
                break
            
            tweet.append(tweets_queue.popleft())
            print(i)
    return(tweet)
            
if __name__ == '__main__':
   
   
   tweet_queue = deque()

   tweet_stream = Thread(target=stream_tweets, args=(tweet_queue,), daemon=True)
   tweet_stream.start()
   data=process_tweets(tweet_queue)
   print(len(data))
   
   # Create the gmap plotter:
   gmap = gmplot.GoogleMapPlotter(MAP_LAT, MAP_LONG, MAP_RADIUS, apikey=GMAPS_API_KEY)
   # iterate over tweets 
   for i,t in enumerate(data):
       
       if t.get('geo') and t['geo'].get('coordinates'):
           # get latitude and longitude
           lat, lon =  t['geo']['coordinates']
           print(t['geo']['coordinates'])
           # if coordinate are specific enough
           if (lat, lon) != (41.9, 12.5):

               # add a marker @ lat, lon, with an info windows containg the tweet
               usr = t['user']['name']
               date = t.get('created_at',"")
               text = t.get('text',"")
               img = ""

               info_box = f'<h4>{usr}@{date}</h4><p>{text}</p>{img}'

               # add a marker on tweet position, with infobox containing date, user and text
               gmap.marker(lat,lon, color='cornflowerblue',info_window=info_box)

               

   # Draw the map to an HTML file:
   gmap.draw('map.html')
