'''
Created on 21.01.2013

@author: phil
'''
import unittest
import random
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
        
        self.logger.info('latitude = %f' % self.latitude)
        self.logger.info('longitude = %f' % self.longitude)

        
    def test_get_station_by_coordinates(self):
        api = OpenWeatherMapApi()
        station_list = api.get_station_by_coordinates(self.latitude, self.longitude, 10)
        
        self.methodname = 'test_get_station_by_coordinates()'
        
        self.assertIsNotNone(station_list, '%s - station list must not be null' % (self.methodname))
        self.assertTrue(self.checklistlength(station_list, 1, 10), 
                        '%s - list length must be greater than 0 and less than equals 10' % (self.methodname))

        for element in station_list:
            self.logger.info(element)
            
            self.assertTrue(self.checkdatetime(element.dt), 
                            '%s - datetime isn\'t from the current day' % (self.methodname))
            self.assertEquals(element.get_type_string(), self.getstationstring(element.stationtype), 
                              '%s - station\'s string representation fails ' % self.methodname)
            self.assertTrue(self.checkid(element.identifier), 
                            '%s - identifier must be a an int greater than zero ' % self.methodname)
            self.assertTrue(self.checkcoordinates(element.get_coord_tuple()), 
                            '%s - latitude must be in range -90.0 to +90.0 and longitude must be in range -180.0 to +180.0' % self.methodname)
            self.assertTrue(self.checktemperatures(element.get_main_temp(), element.get_main_temp_c(), element.get_main_temp_f()), 
                            '%s - temperature conversion between kelvin, degree celsius and degree fahrenheit is wrong' % self.methodname)
            self.assertTrue(self.checkpressure(element.get_main_pressure()), 
                            '%s - pressure must be greather or equal to 0' % self.methodname)
            self.assertTrue(self.checkhumidity(element.get_main_humidity()), 
                            '%s - humidity must be greather or equal to 0' % self.methodname)
            self.assertTrue(self.checkwindspeed(element.get_wind_speed(), element.get_wind_speed_km()), 
                            '%s - conversion between windspeed in mps and kms fails')
            self.assertTrue(self.checkwindgust(element.get_wind_gust()), 
                            '%s - wind gust must be greather or equal to 0' % self.methodname)
            self.assertTrue(self.checkcloudconditions(element.get_clouds_conditions()), 
                            '%s - cloud condition has no valid value or value isn\'t valid' % self.methodname)
            
            
            
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
            

  #  def test_get_station_by_coordinates(self):
  #      api = OpenWeatherMapApi()
  #      stations = api.get_station_by_coordinates(59.56, 30.20, 10)
  #      print stations[0].get_datetime_string()
  #      print stations[0].get_coord_tuple()
  #      print stations[0].get_main_temp_c()
  #      print stations[0].get_main_temp_f()
        
  #  def test_get_city_weather_by_coordinates(self):
  #      api = OpenWeatherMapApi()
  #      cities = api.get_city_weather_by_coordinates(20.45, 40.34, 5)
        
  #  def test_get_forecast_by_id(self):
  #      api = OpenWeatherMapApi()
  #      forecast = api.get_forecast_by_id(524901)
  
  #  def test_get_forecast_by_id(self):
  #      api = OpenWeatherMapApi()
  #      forecast = api.get_forecast_by_id(524901)
  #      print 'test'


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()