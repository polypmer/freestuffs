#This Object is anything so-called Free
class Stuff(object):
    thing = ""
    url = ""
    location = ""
    image = ""
		
    #constructor the de-structor!!  
    def __init__(self, thing, url, location, image):
        self.thing = thing
        self.url = 'http://montreal.craigslist.ca' + url
        self.location = location
        self.image = image #this isn't implemented yet

    #the stringifing printer.... Python is so pretty
    def __str__(self):
        return "what:%s \n where:%s \n link:%s \n image:%s" % (self.thing, self.location, self.url, self.image)
        
