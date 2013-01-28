#!/usr/bin/env python

import unittest
import logging
import re
from datetime import datetime
from pyowm import OpenWeatherMapApi


class Test(unittest.TestCase):
    
    def setUp(self):
        self.logger = logging.getLogger()
        self.orig_handlers = self.logger.handlers
        self.logger.handlers = []
        self.level = self.logger.level
        
        logging.basicConfig(format='%(levelname)s %(message)s', level=logging.INFO)
        self.latitude = 20#random.uniform(-90.0, 90.0)
        self.longitude = 50#random.uniform(-180.0, 180.0)
        
        #self.logger.info('latitude = %f' % self.latitude)
        #self.logger.info('longitude = %f' % self.longitude)
        

        
    def testgetstationbycoordinates(self):
        api = OpenWeatherMapApi()
        stationlist = api.getstationbycoordinates(self.latitude, self.longitude, 10)
        
        self.assertIsNotNone(stationlist, 'station list must not be null')
        self.assertTrue(self.checklistlength(stationlist, 1, 10), 
                        'list length must be greater than 0 and less than equals 10')

        for station in stationlist:
            self.logger.info(station)
            
            self.assertTrue(self.checkdatetime(station.dt), 
                            'datetime isn\'t from the current day')
            self.assertEquals(station.gettypestring(), self.getstationstring(station.stationtype), 
                              'station\'s string representation fails ')
            self.assertTrue(self.checkid(station.identifier), 
                            'identifier must be a an int greater than zero ')
            self.assertTrue(self.checkcoordinates(station.getcoordtuple()), 
                            'latitude must be in range -90.0 to +90.0 and longitude must be in range -180.0 to +180.0')
            self.assertTrue(self.checktemperatures(station.getmaintemp(), station.getmaintempc(), station.getmaintempf()), 
                            'temperature conversion between kelvin, degree celsius and degree fahrenheit is wrong')
            self.assertTrue(self.checkpressure(station.getmainpressure()), 
                            'pressure must be greather or equal to 0')
            self.assertTrue(self.checkhumidity(station.getmainhumidity()), 
                            'humidity must be greather or equal to 0')
            self.assertTrue(self.checkwindspeed(station.getwindspeed(), station.getwindspeedkm()), 
                            'conversion between windspeed in mps and kms fails')
            self.assertTrue(self.checkwindgust(station.getwindgust()), 
                            'wind gust must be greather or equal to 0')
            self.assertTrue(self.checkcloudconditions(station.getcloudsconditions()), 
                            'cloud condition has no valid value or value isn\'t valid')
            
    def testgetcityweatherbycoordinates(self):
        api = OpenWeatherMapApi()
        citylist = api.getcityweatherbycoordinates(self.latitude, self.longitude, 10)
        
        
        self.assertIsNotNone(citylist, '%s - city list must not be null')
        self.assertTrue(self.checklistlength(citylist, 1, 10), 
                        '%s - list length must be greater than 0 and less than equals 10')
        
        for city in citylist:
            self.logger.info(city)
            
            self.assertTrue(self.checkid(city.identifier), 'identifier must be an int greater than zero')
            self.assertTrue(self.checkname(city.name), 'city name must match regex [A-Za-z]+\s*[A-Za-z]*')
            self.assertTrue(self.checkclouds(city.getclouds()), 'city clouds must be greater equal 0')
            self.assertTrue(self.checkcoordinates(city.getcoordtuple()), 
                            'latitude must be in range -90.0 to +90.0 and longitude must be in range -180.0 to +180.0')
            self.assertTrue(self.checktemperatures(city.getmaintemp(), city.getmaintempc(), city.getmaintempf()), 
                            'temperature conversion between kelvin, degree celsius and degree fahrenheit is wrong')
            
            
            
        
        
            
    def checkclouds(self, clouds):
        if clouds >= 0:
            return True
            
    def checklistlength(self, listToCheck, minLength, maxLength):
        if len(listToCheck) >= minLength and len(listToCheck) <=maxLength:
            return True
            
    def checkdatetime(self, dt):
        dtToCheck = datetime.fromtimestamp(dt)
        currentDate = datetime.now()
        
        if (currentDate.year == dtToCheck.year and currentDate.month == dtToCheck.month and dtToCheck.day == dtToCheck.day):
            return True
        
    def checkid(self, identifier):
        if (int(identifier) > 0):
            return True
        
    def checkcoordinates(self, coordinates):
        latitude = coordinates[0]
        longitude = coordinates[1]
        
        if (latitude > -90.0 and latitude < 90.0 and longitude > -180.0 and longitude < 180.0):
            return True
        
    def checktemperatures(self, temp, temp_c, temp_f):
        if (temp_c + 273.15 == temp and (temp_f -32) * 5 / 9):
            return True
        
    def checkpressure(self, pressure):
        if (pressure == None):
            return True
        if (pressure >= 0):
            return True
        
    def checkhumidity(self, humidity):
        if (humidity == None):
            return True
        if (humidity >= 0):
            return True
        
    def checkwindspeed(self, windspeedmps, windspeedkms):
        if (windspeedmps == None):
            return True
        if (windspeedmps == windspeedkms / 1.609344):
            return True
        
    def checkwinddeg(self, degree):
        if (degree >=0 and degree < 360):
            return True
        
    def checkwindgust(self, gust):
        if gust == None:
            return True
        if (gust >= 0):
            return True
        
    def checkclouddistance(self, distance):
        pass
    
    def checkcloudconditions(self, conditions):
        
        for key in conditions.iterkeys():
            if not self.getcloudconditions(key) == True or not conditions[key] >= 0:
                return False
            
        return True
    
    def checkname(self, name):
        result = re.match('[A-Za-z]+\s*[A-Za-z]*', name)
        
        if result != None:
            return True
    
    def checkrainhours(self, rain):
        pass
    
    
        
    def getstationstring(self, stationType):
        
        if (stationType == 1):
            return 'Airport station'
        elif (stationType == 2):
            return 'SWOP station'
        elif (stationType == 3):
            return 'SYNOP station'
        elif (stationType == 4):
            return 'DIY station'
        
    def getcloudconditions(self, condition):
        if condition == None:
            return True
        if condition in ('NCT', 'NSC', 'SKC', 'CLR', 'FEW','OVC', 'BKN', 'CAVOK', 'SCT' ):
            return True
            

if __name__ == "__main__":
    unittest.main()