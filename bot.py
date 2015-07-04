#!/usr/bin/env python
# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Dann Blair <dann@bitspacedevelopment.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Using https://github.com/tweepy/tweepy

import tweepy, time, sys, random
import sqlite3 as lite

#Corresponding twitter info
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''

# Twitter Connections
def twitterConnect(ck, cs, ak, ast):
    print "Connecting to Twitter"
    auth = tweepy.OAuthHandler(ck, cs)
    auth.set_access_token(ak, ast)
    return tweepy.API(auth)

# Database Connection
def dbConnect():
    print "Connecting to Database"
    con = None
    try:
        con = lite.connect('test.db')
        cur = con.cursor()
        cur.execute('SELECT SQLITE_VERSION()')
        data = cur.fetchone()
        print "SQLite version: %s" % data
    except lite.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()
    return

#Retweet the tweet
def retweet(i):
    try:
        print "Retweeting " + i.author.screen_name
        api.retweet(i.id)
    except:
        print "That id isn't valid or something, no biggie"

#Follow the user's followers
def follow(screenName):
    for user in tweepy.Cursor(api.followers, screen_name=screenName).items():
        print user.screen_name
        if user.id != me.id:
            api.create_friendship(user.id)

# Follow our new friend
def createFriend(i):
    api.create_friendship(i.author.id)
    return

# Reply to the tweet
def replyTweet(i):
    un = "@%s" % (i.user.screen_name)
    m = un + " hello!"
    api.update_status(m, i.id)

# Search for our tags
def search():
    while True:
        search_text = "#winnipeg"
        search_number = 4
        search_result = api.search(search_text, rpp=search_number)
        for i in search_result:
            retweet(i)
            createFriend(i)

            time.sleep(100) # delays for 5 seconds

# Start our bot
api = twitterConnect(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)
me = api.me()

#Start the program
dbConnect()
search()
