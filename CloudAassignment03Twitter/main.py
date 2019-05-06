import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from mymodel import GlobeTweet
from mymodel import Tweets
import os

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        mymodel = None
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            email = users.get_current_user().email()
            mymodel_key = ndb.Key('GlobeTweet', email)
            mymodel = mymodel_key.get()
            tweetkey=ndb.Key('Tweets','datastore')
            tw=tweetkey.get()
            if tw==None:
                tw=Tweets(id='datastore')
                tw.put()
            if mymodel == None:
                welcome = 'Welcome to the application'
                mymodel = GlobeTweet(id=email)
                mymodel.put()
            if mymodel.profilename ==None:
                self.redirect('/username ')
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
        query=query = GlobeTweet.query().fetch()
        nameprofile=self.request.get('usersearch')
        userfinal=None
        qry1=0
        searchtweet=self.request.get('tweetsearch')
        tweetfinal=[]
        tweetskey=None
        qry2=0
        act=self.request.get('button')
        if act=='Search':
            for i in query:
                if i.profilename == username:
                    qry1=qry1+1
                    userfinal=profilename
        if act=='Tweet Search':
            for i in query:
                for j in i.tweets:
                    if searchtweet in j:
                        qry2=qry2+1
                        tweetfinal.append(j)
        numfollowers=0
        numfollowing=0
        if mymodel!=None:
            for i in mymodel.followers:
                    numfollowers=numfollowers+1
            for j in mymodel.following:
                    numfollowing=numfollowing+1

        tweets_key = ndb.Key('Tweets', 'datastore')
        tweets_key = tweets_key.get()
        tweetsl=[]
        profilenametweets=[]
        if tweets_key!=None:
            for i in reversed(tweets_key.mytweets):
                tweetsl.append(i)
            tweetsl = tweetsl[:50]
            for j in reversed(tweets_key.userprofile):
                profilenametweets.append(j)
            profilenametweets=profilenametweets[:50]
        profiletweets = map(' --> '.join,zip(profilenametweets,tweetsl))

        template_values = {'url' : url,'url_string' : url_string,'user' : user,'welcome' : welcome,'mymodel' : mymodel,'qry1':qry1,'userfinal':userfinal,'qry2':qry2,'tweetfinal':tweetfinal,'numfollowers':numfollowers,'numfollowing':numfollowing,'profiletweets':profiletweets}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))



class Username(webapp2.RequestHandler):
    def get(self):
        email = users.get_current_user().email()
        mymodel_key = ndb.Key('GlobeTweet', email)
        mymodel = mymodel_key.get()
        self.response.out.write("<html><head></head><body>")
        self.response.out.write("""<form align='center' method='get' act='/username'>""")
        self.response.out.write("""USERNAME:<br/><input type='text' name='input' required='True'/><br/>""")
        self.response.out.write("""BIO:<br/><input align='center' style="height:200px;width:1000px;font-size:14pt;" type='text' name='input1' required='True' maxlength="280"/><br/>""")
        self.response.out.write("""<input align='center' type='submit' name='button' value='Submit'/>""")
        self.response.out.write("""</form>""")
        act=self.request.get('button')
        url = users.create_logout_url(self.request.uri)
        if act == 'Submit':
                profilename=self.request.get('input')
                status=self.request.get('input1')
                mymodel.profilename=profilename
                mymodel.status=status
                mymodel.put()
                self.redirect("/")
        self.response.write('<br/><a href="/"><b>Logout</b></a>')
        self.response.out.write("</body></html>")


class Edit(webapp2.RequestHandler):
    def get(self):
        emailid = users.get_current_user().email()
        mymodel_key = ndb.Key('GlobeTweet', emailid)
        mymodel = mymodel_key.get()
        self.response.out.write("<html><head></head><body>")
        self.response.out.write("<b><i> Edit your information below:</i></b><br/>")
        self.response.out.write("""<form method='get' action='/edit' align="center">""")
        qry1=mymodel.status
        self.response.out.write("""<b>BIO:</b><br/><input align=center style="height:200px;width:1000px;font-size:20pt;" type='text' name='input1' required='True' maxlength="280" placeholder="%s"/><br/>"""%(qry1))
        self.response.out.write("""<input align=center type='submit' name='button' value='Submit'/>""")
        self.response.out.write("""</form>""")
        self.response.out.write("<a href='/'>Home</a>")
        act=self.request.get('button')
        if act == 'Submit':
            status=self.request.get('input1')
            mymodel.status=status
            mymodel.put()
            self.redirect('/')
        self.response.out.write("</body></html>")
    def post(self):
        email = users.get_current_user().email()
        mymodel_key = ndb.Key('GlobeTweet', email)
        mymodel = mymodel_key.get()
        act=self.request.get('button')
        tweets_key = ndb.Key('Tweets', 'datastore')
        tweets = tweets_key.get()
        name=mymodel.profilename
        if act == 'Submit':
            tweet=self.request.get('tweet')
            mymodel.tweets.append(tweet)
            tweets.mytweets.append(tweet)
            tweets.userprofile.append(name)
            tweets.put()
            mymodel.put()
            self.redirect('/')

class Profile(webapp2.RequestHandler):
    def get(self,id):
        self.response.headers['Content-Type'] = 'text/html'
        myprofile=id
        query = GlobalTweet.query(GlobalTweet.profilename == myprofile)
        mylist=[]
        for i in query:
            for j in reversed(i.tweets):
                mylist.append(j)
        mylist = mylist[:50]
        template_values={'query':query,'mylist':mylist}
        template=JINJA_ENVIRONMENT.get_template('profile.html')
        self.response.write(template.render(template_values))
    def post(self,id):
        email = users.get_current_user().email()
        mymodel_key = ndb.Key('GlobeTweet', email)
        mymodel = mymodel_key.get()
        profilename=mymodel.username
        mylist=id
        emailid=None
        finalusername=None
        query = mymodel.query(mymodel.profilename == mylist)
        for i in query:
            emailid=i.key.id()
        act=self.request.get('button')
        if act == 'FOLLOW':
                mymodel_keys = ndb.Key('MyUser', emails)
                myuserlist = mymodel_keys.get()
                finalusername=myuserlist.profilename
                if profilename==myusers.profilename:
                        self.redirect('/profile/%s'%(mylist))
                else:
                    if profilename in myusers.numfollowers:
                            self.redirect('/profile/%s'%(mylist))
                    else:
                            myusers.numfollowers.append(profilename)
                            mymodel.numfollowing.append(finalusername)
                            mymodel.put()
                            myusers.put()
                            self.redirect('/profile/%s'%(mylist))
        if act == 'UNFOLLOW':
            mymodel_keys = ndb.Key('GlobalTweet', emails)
            myuserlist = mymodel_keys.get()
            finalusername=myusers.profilename
            if profilename in myusers.numfollowers:
                myuserlist.numfollowers.remove(profilename)
                myuserlist.put()
                if finalusername in mymodel.numfollowing:
                    mymodel.numfollowing.remove(finalusername)
                    mymodel.put()
            self.redirect('/profile/%s'%(my))

class DeleteEdit(webapp2.RequestHandler):
    def get(self,id):
        self.response.headers['Content-Type'] = 'text/html'
        mylist=id
        emailid = users.get_current_user().email()
        mymodel_key = ndb.Key('GlobeTweet', emailid)
        mymodel = mymodel_key.get()
        mylist=mymodel.tweets
        mylist=mylist[::-1]
        template_values={'mymodel':mymodel,'mylist':mylist}
        template=JINJA_ENVIRONMENT.get_template('deletedit.html')
        self.response.write(template.render(template_values))
    def post(self,id):
        act = self.request.get('button')
        emailid = users.get_current_user().email()
        mymodel_key = ndb.Key('GlobeTweet', emailid)
        mymodel = mymodel_key.get()
        datastore_key = ndb.Key('Tweets', 'datastore')
        datastore = datastore_key.get()
        myid=id
        twt=None
        if action == 'delete':
            myid=mymodel.tweets
            mylist=mylist[::-1]
            del mylist[int(self.request.get('index')) - 1]
            mylist=mylist[::-1]
            mymodel.tweets=l
            mymodel.put()
            twt=self.request.get('users_name')
            datastore.mytweets.remove(tw)
            datastore.put()
            self.redirect('/deletedit/%s'%(myid))
        if act=='Edit':
            twt=self.request.get('users_name')
            mylist1=mymodel.tweets
            mylist1=mylist1[::-1]
            twt1=mylist1[int(self.request.get('index'))-1]
            mylist=mymodel.tweets
            mylist=mylist[::-1]
            mylist[int(self.request.get('index'))-1]=self.request.get('users_name')
            mylist=mylist[::-1]
            mymodel.tweets=l
            mymodel.put()
            datastore.mytweets[datastore.mytweets.index(twt1)]=twt
            datastore.put()
            self.redirect('/deletedit/%s'%(myid))


app = webapp2.WSGIApplication([('/', MainPage),('/username', Username),('/edit',Edit),('/profile/(.*)',Profile),('/deletedit/(.*)',DeleteEdit)], debug=True)
