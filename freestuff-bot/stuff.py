###########################################################################
# Copyright (C) 2015 Fenimore Love 
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
###

"""
    This module houses the ever important Class Definition
    and the gather_stuff method which calls stuffify
    and returns a list of stuffs
    
    Example use, using ipython:
    
    import stuff
    import mappify
    
    stuffs = stuff.gather_stuff("montreal")
    mappify.post_map(stuffs)
"""

import requests, re
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import stuffify, mappify # Internal Modules

class Stuff(object):
    """A freestuff Craigslist object.
    
    Attributes:
        - thing -- title of object passed explicitly
        - url -- constructed from url, implicit
        - image -- passed explicitly
        - user_location -- passed explicitly, requires clean up
        - coordinates -- array of longitude and latitude
    """
    #  coordinates = []
    
    def __init__(self, thing, url, location, image, user_location):
        """Construct stuff object.
        
        Fill this object with the information from
        a craigslist page. (There is no price attribute,
        because it is designed for invaluable things).
        The precise coordinates are not initially set,
        because they require significantly more requests.
        See class method get_coordinates().
        
        Keyword arguements:
            - user_location -- use to construct url
        """
        self.thing = thing
        self.url = 'http://' + user_location + '.craigslist.ca' + url
        self.location = location
        self.image = image
        self.user_location = user_location

    def __str__(self):
        """Print stuff summary."""
        return "what: %s \n where: %s \n link: %s \n image: %s" % (self.thing, self.location, self.url, self.image)

    def refine_city_name(self, user_place):
        """Refine location of two word cities."""
        if user_place == 'newyork': # does this have to capitalized?
            loc = '#FreeStuffNY' # For tweeting
        elif user_place == 'washingtondc':
            loc = 'Washington D.C.'
        elif user_place == 'sanfrancisco':
            loc = 'San Francisco, USA'
        else:
            return loc

    def find_coordinates(self):
        """Get and set longitude and Latitude
        
        Scrape individual posting page, if no
        coordinates are found, cascade precision.
        Returns an array, first latitude and then
        longitude.
        """
        self.coordinates = []
        geolocator = Nominatim()
        follow_this = self.url
        follow_page = requests.get(follow_this)
        print(self.url)
        follow_soup = BeautifulSoup(follow_page.text, "html.parser")
        location = follow_soup.find("div", class_="viewposting")
        print(location)
        if location is not None:
            print('not none')
            lat = location['data-latitude']
            lon = location['data-longitude']
        else:
            print('none')
            try:
                lat = geolocator.geocode(self.location).latitude
                lon = geolocator.geocode(self.location).longitude
                print(int(lat))
            except:
                try:
                    lat = geolocator.geocode(self.user_location).latitude
                    lon = geolocator.geocode(self.user_location).longitude
                except:
                    lat = 0 #38.9047 # This is DC
                    lon = 0 #-77.0164
        self.coordinates.append(lat)
        self.coordinates.append(lon)
