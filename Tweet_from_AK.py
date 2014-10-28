#!/usr/bin/env python
from tweepy import *
import time, tweepy, sys
import os, urllib
import simplejson,json
import csv, string
#username = 'ukyresearch'
#password = '070605lastday'

OAUTH_TOKEN = ''
OAUTH_SECRET = ''
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_SECRET)
api = tweepy.API(auth)


class SListener(StreamListener):

    def __init__(self, api = None, fprefix = 'streamer'):
        self.api = api
        self.counter = 0
        self.fprefix = fprefix
        self.output  = open('data_AK/' + fprefix + '.'
                            + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
        self.delout  = open('data_AK/delete.txt', 'a')

    def on_data(self, data):
        if json.loads(data).has_key('coordinates') and json.loads(data)['coordinates'] :
            if  'in_reply_to_status' in data:
                self.on_status(data)
            elif 'delete' in data:
                delete = json.loads(data)['delete']['status']
                if self.on_delete(delete['id'], delete['user_id']) is False:
                    return False
            elif 'limit' in data:
                if self.on_limit(json.loads(data)['limit']['track']) is False:
                    return False
            elif 'warning' in data:
                warning = json.loads(data)['warnings']
                print warning['message']
                return False

    def on_status(self, status):
        self.output.write(status + "\n")

        self.counter += 1

        if self.counter >= 20000:
            self.output.close()
            self.output = open('../data_AK/' + self.fprefix + '.'
                               + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
            self.counter = 0

        return

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return
        
    def on_limit(self, track):
        sys.stderr.write(track + "\n")
        return

    def on_error(self, status_code):
        sys.stderr.write('Error: ' + str(status_code) + "\n")
        return False

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return
        
def main():
    print 'Streaming started'
    while True:
        try:
            stream = Stream(auth, SListener())
            stream.filter(track=['a','e','i','o','u'], locations=[-173.008060,53.293648,-142.070559,71.671710])
        except:
            time.sleep(10)

main()

