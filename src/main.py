import config
import tweepy
from tweepy import OAuthHandler, Stream
from tweepy.streaming import Stream
import socket
import json

class TweetListener(Stream):

    def __init__(self, csocket):
        self.client_socket = csocket
    
    def on_data(self, data):

        try:
            msg = json.loads(data)
            print(msg['text'].encode('utf-8'))
            self.client_socket.send(msg['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print("ERROR ", e)

        return True

    def on_error(self, status):
        print(status)
        return True

def send_data(c_socket):
    auth = OAuthHandler(config.API_KEY, config.API_KEY_SECRET)
    auth.set_access_token(config.BEARER_TOKEN)

    twitter_stream = Stream(auth, TweetListener(c_socket))
    twitter_stream.filter(track=['google'])

if __name__ == '__main__':
    s = socket.socket()
    host = '127.0.0.1'
    port = 5555
    s.bind((host, port))
    print('listening on port 5555')

    s.listen(5)
    c, addr = s.accept()
    send_data(c)