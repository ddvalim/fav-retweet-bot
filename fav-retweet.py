import tweepy
import logging
import json
from config import create_api


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class FavRetweet(tweepy.Stream):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"processing tweet id {tweet['id']}")
        if tweet['user']['id'] == self.me.id:
            return
        if not tweet['favorited']:
            try:
                self.api.create_favorite(tweet['id'])
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
                return
        if not tweet['retweeted']:
            try:
                self.api.retweet(tweet['id'])
            except Exception as e:
                logger.error("Error on retweet", exc_info=True)
                return
    
    def on_exception(self, status):
        print('Something went wrong! :c')
        logger.error(status)
    
    def on_data(self, obj):
        print('Receiving data from Twitter API =)')
        self.on_status(json.loads(obj))
    
    def on_connect(self):
        print('Bot is Online! :)')

def main(keywords):
    api = create_api()
    tweets_listener = FavRetweet(api)
    stream = tweepy.Stream(api.auth, listener=tweets_listener)
    stream.filter(track=keywords, languages=["pt"])


if __name__ == "__main__":
    main(['lula'])
