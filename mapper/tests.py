import unittest
from mapper.models import *

class SiteTest(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_insert(self):
        site = Site.objects.create(name='My website', 
                 url='http://www.website.com',)
        self.assertEquals(site.id,1)