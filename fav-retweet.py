import tweepy
import logging
import json
from config import create_api


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class FavRetweet(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"processing tweet id {tweet.id}")
        if tweet.user.id == self.me.id:
            return
        if not tweet.favorited:
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
                raise e
        if not tweet.retweeted:
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on retweet", exc_info=True)
                raise e
    
    def on_error(self, status):
        logger.error(status)
    

def main(keywords):
    api = create_api()
    tweets_listener = FavRetweet(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["pt"])


if __name__ == "__main__":
    main(['Python'])
