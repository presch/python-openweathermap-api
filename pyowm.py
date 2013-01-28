#!/usr/bin/env python

from json import load
from urllib2 import urlopen
from pyowmdata import Station
from pyowmdata import City
from pyowmdata import Forecast
from pyowmdata import ForecastItem
from pyowmdata import ForecastItemcompact
from pyowmdata import Forecastcompact
from utilities import *
import simplejson

class OpenWeatherMapApi(object):
    
    OPENWEATHERMAP_FIND_URL = 'http://openweathermap.org/data/2.1/find/'
    OPENWEATHERMAP_CITY_URL = 'http://openweathermap.org/data/2.1/weather/city/'
    OPENWEATHERMAP_FORECAST_URL = 'http://openweathermap.org/data/2.1/forecast/city/'
    
    def getstationbycoordinates(self, latitude, longitude, count):
        ''' return a list of stations next to the latitude and longitude given'''
        
        querypart = 'station?lat=%f&lon=%f&cnt=%d' % (latitude, longitude, count)
        queryurl = self.OPENWEATHERMAP_FIND_URL + querypart
        
        #stations = self.open_url_decode_json(query_url)
        stations = self.openurldecodesimplejson(queryurl)
        
        return self.getstationlistfromdictionary(stations)
        
    
    def getcityweatherbycoordinates(self, latitude, longitude, count):
        ''' return a list of cities next to the latitude and longitude given'''
        
        querypart = 'city?lat=%f&lon=%f&cnt=%d' % (latitude, longitude, count)
        queryurl = self.OPENWEATHERMAP_FIND_URL + querypart
        
        #cities = self.open_url_decode_json(query_url)
        cities = self.openurldecodesimplejson(queryurl)
        
        return self.getcitylistfromdictionary(cities)
        
    
    def getstationbyboundingbox(self, bbox):
        ''' return a list of stations whose geographic coordinates lay within the rectangle bbox'''
        
        querypart = 'station?bbox=%s&cluster=yes' % bbox
        queryurl = self.OPENWEATHERMAP_FIND_URL + querypart
        
        #stations = self.open_url_decode_json(query_url)
        stations = self.openurldecodesimplejson(queryurl)
        
        return self.get_stationlistfromdictionary(stations)
    
    def getcityweatherbyboundingbox(self, bbox):
        ''' return a list of cities whose geographic coordinates lay 
        within the rectangle bbox'''
        
        querypart = 'city?bbox=%s&cluster=yes' % bbox
        queryurl = self.OPENWEATHERMAP_FIND_URL + querypart
        
        cities = self.openurldecodesimplejson(queryurl)
        
        return self.getcitylistfromdictionary(cities)
    
    def getstationbycoordinatesradius(self, latitude, longitude, radius):
        ''' return a list of stations whose coordinates lay within a circle, 
        circle is defined by a center point and a radius'''
        
        querypart = 'station?lat=%f&lon=%f&radius=%d' % (latitude, longitude, radius)
        queryurl = self.OPENWEATHERMAP_FIND_URL + querypart
        
        stations = self.openurldecodesimplejson(queryurl)
        
        return self.getstationlistfromdictionary(stations)
    
    def getcityweatherbycoordinatesradius(self, latitude, longitude, radius):
        ''' return a list of cities whose coordinates lay witin a circle, 
        circle is defined by a center point and a radius'''
        
        querypart = 'city?lat=%f&lon=%f&radius=%d' % (latitude, longitude, radius)
        queryurl = self.OPENWEATHERMAP_FIND_URL + querypart
        
        cities = self.openurldecodesimplejson(queryurl)
        
        return self.getcitylistfromdictionary(cities)
    
    
    def getcitybycitycountrycode(self, city, like, countrycode):
        ''' return a list of cities that match search substring'''
        
        queryurl = None
        
        if countrycode != None:
            querypart = 'name?q=%s,%s' % (city, countrycode)
            queryurl = self.OPENWEATHERMAP_FIND_URL + querypart
            
        if like != None:
            querypart = 'name?q=%s&type=like' % (city)
            queryurl = self.OPENWEATHERMAP_FIND_URL + querypart
            
        if city != None and like == None and countrycode == None:
            querypart = 'name?q=%s' % city
            queryurl = self.OPENWEATHERMAP_FIND_URL + querypart
            
        cities = self.openurldecodesimplejson(queryurl)
        
        return self.getcitylistfromdictionary(cities)
    
    def getcityweaterbyid(self, identifier):
        ''' return the current weather in a concrete chosen city where you know 
        the city id.'''
        
        querypart = '%d' % (identifier)
        queryurl = self.OPENWEATHERMAP_CITY_URL + querypart
        
        city = self.openurldecodesimplejson(queryurl)
        
        return City(getlistitem(city, 'id'), getlistitem(city, 'name'), 
                    getlistitem(city, 'coord'), getlistitem(city, 'distance'), 
                    getlistitem(city, 'main'), getlistitem(city, 'dt'), 
                    getlistitem(city, 'wind'), getlistitem(city, 'clouds'), 
                    getlistitem(city, 'weather'), getlistitem(city, 'sys'))
    
    def getforecastbyid(self, identifier):
        ''' return the forecast of the city for the next 7 days by given id'''
        
        querypart = '%d' % (identifier)
        queryurl = self.OPENWEATHERMAP_FORECAST_URL + querypart
        
        forecast = self.openurldecodesimplejson(queryurl)
        
        self.getforecastlistfrom_dictionary(forecast)
        
    
    def getforecastbyname(self, city):
        ''' return the forecast of the city for the next 7 days by given city''' 
        
        querypart = '?q=%s' % (city)
        queryurl = self.OPENWEATHERMAP_FORECAST_URL + querypart
        
        forecast = self.openurldecodesimplejson(queryurl)
        
        self.getforecastlistfromdictionary(forecast)
    
    def getdailyforecast(self, identifier):
        ''' return the forecast of the city for the next 7 days in a compact 
        format by given id'''
        
        querypart = '%d?mode=daily_compact' % (identifier)
        queryurl = self.OPENWEATHERMAP_FORECAST_URL + querypart
        
        compactforecast = self.openurldecodesimplejson(queryurl)
        
        self.getcompactforecastfromdictionary(compactforecast)
    
    def getweatherstationinformation(self, identifier):
        ''' not implemented yet '''
        pass
    
    def getstation_historybyid(self, identifier, stationtype):
        ''' not implemented yet '''
        pass
    
    def getstationhistorybyidstartend(self, identifier, stationtype, start, end):
        ''' not implemented yet '''
        pass
    
    def getstationlistfromdictionary(self, dictionary):
        ''' returns a list of Station obejcts'''
        stationlist = []
        
        for sstation in dictionary['list']:
            station = Station(getlistitem(sstation, 'id'), getlistitem(sstation, 'dt'), 
                              getlistitem(sstation, 'name'), getlistitem(sstation, 'type'), 
                              getlistitem(sstation, 'coord'), getlistitem(sstation, 'distance'), 
                              getlistitem(sstation, 'main'), getlistitem(sstation, 'wind'), 
                              getlistitem(sstation, 'clouds'), getlistitem(sstation, 'rain'))
            stationlist.append(station)
            
        return stationlist
    
    def getcitylistfromdictionary(self, dictionary):
        ''' returns a list of City objects'''
        citylist = []
        
        for scity in dictionary['list']:
            city = City(getlistitem(scity, 'id'), getlistitem(scity, 'name'),
                        getlistitem(scity, 'coord'), getlistitem(scity, 'distance'), 
                        getlistitem(scity, 'main'), getlistitem(scity, 'dt'), 
                        getlistitem(scity, 'wind'), getlistitem(scity, 'clouds'), 
                        getlistitem(scity, 'weather'), getlistitem(scity, 'sys'))
            
            citylist.append(city)
            
        return citylist
    
    def getforecastlistfromdictionary(self, dictionary):
        ''' returns a Forecast object containing a list of forecast items'''
        
        forecastitems = []
         
        for item in getlistitem(dictionary, 'list'):
            forecastitem = ForecastItem(getlistitem(item, 'clouds'), getlistitem(item, 'snow'), 
                                         getlistitem(item, 'dt_txt'), getlistitem(item, 'weather'), 
                                         getlistitem(item, 'main'), getlistitem(item, 'wind'))
            forecastitems.append(forecastitem)

        return Forecast(getlistitem(dict, 'id'), getlistitem(dict, 'city'), 
                        getlistitem(dict, 'url'), forecastitems)
        
    def getcompactforecastfromdictionary(self, dictionary):
        ''' returns a Forecast_compact object containing ForecastItem_compact objects'''
        
        forecastcompactitems = []
        
        for item in getlistitem(dictionary, 'list'):
            compactforecastitem = ForecastItemcompact(getlistitem(item, 'dt'), getlistitem(item, 'temp'), 
                                                         getlistitem(item, 'night'), getlistitem(item, 'eve'), 
                                                         getlistitem(item, 'morn'), getlistitem(item, 'pressure'), 
                                                         getlistitem(item, 'humidity'), getlistitem(item, 'weather'), 
                                                         getlistitem(item, 'speed'), getlistitem(item, 'deg'))
            forecastcompactitems.append(compactforecastitem)
            
        return Forecastcompact(forecastcompactitems)
    
    def openurldecodejson(self, url):
        ''' open a given url and returns the python object representation of a json string'''
        query_data = urlopen(url)
        return load(query_data)
    
    def openurldecodesimplejson(self, url):
        ''' open a given url and returns the python object representation of a json string'''
        query_data = urlopen(url).read()
        return simplejson.loads(query_data)
        

    
if __name__ == '__main__':
    pass