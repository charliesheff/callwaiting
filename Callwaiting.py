
import os
import urllib
import jinja2
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


# Where to store the data collected
RECORDS = 'Recordsofcompanies'


# Setting they key for the stored data
def datastore_key(list=RECORDS):
    """Constructs a Datastore key for a Companies entity.

    We use list as the key.
    """
    return ndb.Key('Companies', list)


   
# Where to store the typed values in the datastore
class Datainsert(ndb.Model):
    """A main model for representing an individual Companies Datainsert."""
    nameofcompany = ndb.StringProperty(indexed=False)
    minutesofcall = ndb.StringProperty(indexed=False)
    dateofcall = ndb.StringProperty(indexed=False)
    timeofcall = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)




# Retreive from the datastore, the last 3 entries submitted to the site
class MainPage(webapp2.RequestHandler):

    def get(self):
        list = self.request.get('BT',
                                          RECORDS)
        Datainserts_query = Datainsert.query(
            ancestor=datastore_key(list)).order(-Datainsert.date)
        Datainserts = Datainserts_query.fetch(3)

        template_values = {
            'Datainserts': Datainserts,
            'list': urllib.quote_plus(list),
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))



# Code that takes what is inserted in the html and puts it into the datastore.
class Companies(webapp2.RequestHandler):

    def post(self):
        list = self.request.get('list',
                                          RECORDS)
        datainsert = Datainsert(parent=datastore_key(list))

     
        datainsert.nameofcompany = self.request.get('nameofcompany')
        datainsert.dateofcall = self.request.get('dateofcall')
        datainsert.timeofcall = self.request.get('timeofcall')
        datainsert.minutesofcall = self.request.get('minutesofcall')
        datainsert.put()

        query_params = {'list': list}
        self.redirect('/?' + urllib.urlencode(query_params))




app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Companies),
], debug=True)

