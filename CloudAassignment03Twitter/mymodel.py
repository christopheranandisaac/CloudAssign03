from google.appengine.ext import ndb
class GlobeTweet(ndb.Model):
      profilename = ndb.StringProperty()
      status = ndb.StringProperty()
      tweets = ndb.StringProperty(repeated=True)
      followers= ndb.StringProperty(repeated=True)
      following = ndb.StringProperty(repeated=True)

class Tweets(ndb.Model):
    mytweets=ndb.StringProperty(repeated=True)
    userprofile=ndb.StringProperty(repeated=True)
