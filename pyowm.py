#!/usr/bin/env python

from json import load
from urllib2 import urlopen
from pyowmdata import Station
from pyowmdata import City
from pyowmdata import Forecast
from pyowmdata import ForecastItem
from pyowmdata import ForecastItem_compact
from pyowmdata import Forecast_compact
from utilities import *
import simplejson

class OpenWeatherMapApi(object):
    
    openweathermap_find_url = 'http://openweathermap.org/data/2.1/find/'
    openweathermap_city_url = 'http://openweathermap.org/data/2.1/weather/city/'
    openweathermap_forecast_url = 'http://openweathermap.org/data/2.1/forecast/city/'
    
    def get_station_by_coordinates(self, latitude, longitude, count):
        ''' return a list of stations next to the latitude and longitude given'''
        
        query_part = 'station?lat=%f&lon=%f&cnt=%d' % (latitude, longitude, count)
        query_url = self.openweathermap_find_url + query_part
        
        #stations = self.open_url_decode_json(query_url)
        stations = self.open_url_decode_simplejson(query_url)
        
        return self.get_station_list_from_dictionary(stations)
        
    
    def get_city_weather_by_coordinates(self, latitude, longitude, count):
        ''' return a list of cities next to the latitude and longitude given'''
        
        query_part = 'city?lat=%f&lon=%f&cnt=%d' % (latitude, longitude, count)
        query_url = self.openweathermap_find_url + query_part
        
        #cities = self.open_url_decode_json(query_url)
        cities = self.open_url_decode_simplejson(query_url)
        
        return self.get_city_list_from_dictionary(cities)
        
    
    def get_station_by_bounding_box(self, bbox):
        ''' return a list of stations whose geographic coordinates lay within the rectangle bbox'''
        
        query_part = 'station?bbox=%s&cluster=yes' % bbox
        query_url = self.openweathermap_find_url + query_part
        
        #stations = self.open_url_decode_json(query_url)
        stations = self.open_url_decode_simplejson(query_url)
        
        return self.get_station_list_from_dictionary(stations)
    
    def get_city_weather_by_bounding_box(self, bbox):
        ''' return a list of cities whose geographic coordinates lay 
        within the rectangle bbox'''
        
        query_part = 'city?bbox=%s&cluster=yes' % bbox
        query_url = self.openweathermap_find_url + query_part
        
        cities = self.open_url_decode_simplejson(query_url)
        
        return self.get_city_list_from_dictionary(cities)
    
    def get_station_by_coordinates_radius(self, latitude, longitude, radius):
        ''' return a list of stations whose coordinates lay within a circle, 
        circle is defined by a center point and a radius'''
        
        query_part = 'station?lat=%f&lon=%f&radius=%d' % (latitude, longitude, radius)
        query_url = self.openweathermap_find_url + query_part
        
        stations = self.open_url_decode_simplejson(query_url)
        
        return self.get_station_list_from_dictionary(stations)
    
    def get_city_weather_by_coordinates_radius(self, latitude, longitude, radius):
        ''' return a list of cities whose coordinates lay witin a circle, 
        circle is defined by a center point and a radius'''
        
        query_part = 'city?lat=%f&lon=%f&radius=%d' % (latitude, longitude, radius)
        query_url = self.openweathermap_find_url + query_part
        
        cities = self.open_url_decode_simplejson(query_url)
        
        return self.get_city_list_from_dictionary(cities)
    
    
    def get_city_by_city_countrycode(self, city, like, countrycode):
        ''' return a list of cities that match search substring'''
        
        query_url = None
        
        if countrycode != None:
            query_part = 'name?q=%s,%s' % (city, countrycode)
            query_url = self.openweathermap_find_url + query_part
            
        if like != None:
            query_part = 'name?q=%s&type=like' % (city)
            query_url = self.openweathermap_find_url + query_part
            
        if city != None and like == None and countrycode == None:
            query_part = 'name?q=%s' % city
            query_url = self.openweathermap_find_url + query_part
            
        cities = self.open_url_decode_simplejson(query_url)
        
        return self.get_city_list_from_dictionary(cities)
    
    def get_city_weater_by_id(self, identifier):
        ''' return the current weather in a concrete chosen city where you know 
        the city id.'''
        
        query_part = '%d' % (identifier)
        query_url = self.openweathermap_city_url + query_part
        
        city = self.open_url_decode_simplejson(query_url)
        
        return City(get_list_item(city, 'id'), get_list_item(city, 'name'), 
                    get_list_item(city, 'coord'), get_list_item(city, 'distance'), 
                    get_list_item(city, 'main'), get_list_item(city, 'dt'), 
                    get_list_item(city, 'wind'), get_list_item(city, 'clouds'), 
                    get_list_item(city, 'weather'), get_list_item(city, 'sys'))
    
    def get_forecast_by_id(self, identifier):
        ''' return the forecast of the city for the next 7 days by given id'''
        
        query_part = '%d' % (identifier)
        query_url = self.openweathermap_forecast_url + query_part
        
        forecast = self.open_url_decode_simplejson(query_url)
        
        self.get_forecast_list_from_dictionary(forecast)
        
    
    def get_forecast_by_name(self, city):
        ''' return the forecast of the city for the next 7 days by given city''' 
        
        query_part = '?q=%s' % (city)
        query_url = self.openweathermap_forecast_url + query_part
        
        forecast = self.open_url_decode_simplejson(query_url)
        
        self.get_forecast_list_from_dictionary(forecast)
    
    def get_daily_forecast(self, identifier):
        ''' return the forecast of the city for the next 7 days in a compact 
        format by given id'''
        
        query_part = '%d?mode=daily_compact' % (identifier)
        query_url = self.openweathermap_forecast_url + query_part
        
        compact_forecast = self.open_url_decode_simplejson(query_url)
        
        self.get_compact_forecast_from_dictionary(compact_forecast)
    
    def get_weather_station_information(self, identifier):
        ''' not implemented yet '''
        pass
    
    def get_station_history_by_id(self, identifier, stationtype):
        ''' not implemented yet '''
        pass
    
    def get_station_history_by_id_start_end(self, identifier, stationtype, start, end):
        ''' not implemented yet '''
        pass
    
    def get_station_list_from_dictionary(self, dictionary):
        ''' returns a list of Station obejcts'''
        station_list = []
        
        for s_station in dictionary['list']:
            station = Station(get_list_item(s_station, 'id'), get_list_item(s_station, 'dt'), 
                              get_list_item(s_station, 'name'), get_list_item(s_station, 'type'), 
                              get_list_item(s_station, 'coord'), get_list_item(s_station, 'distance'), 
                              get_list_item(s_station, 'main'), get_list_item(s_station, 'wind'), 
                              get_list_item(s_station, 'clouds'), get_list_item(s_station, 'rain'))
            station_list.append(station)
            
        return station_list
    
    def get_city_list_from_dictionary(self, dictionary):
        ''' returns a list of City objects'''
        city_list = []
        
        for s_city in dictionary['list']:
            city = City(get_list_item(s_city, 'id'), get_list_item(s_city, 'name'),
                        get_list_item(s_city, 'coord'), get_list_item(s_city, 'distance'), 
                        get_list_item(s_city, 'main'), get_list_item(s_city, 'dt'), 
                        get_list_item(s_city, 'wind'), get_list_item(s_city, 'clouds'), 
                        get_list_item(s_city, 'weather'), get_list_item(s_city, 'sys'))
            
            city_list.append(city)
            
        return city_list
    
    def get_forecast_list_from_dictionary(self, dictionary):
        ''' returns a Forecast object containing a list of forecast items'''
        
        forecast_items = []
         
        for item in get_list_item(dictionary, 'list'):
            forecast_item = ForecastItem(get_list_item(item, 'clouds'), get_list_item(item, 'snow'), 
                                         get_list_item(item, 'dt_txt'), get_list_item(item, 'weather'), 
                                         get_list_item(item, 'main'), get_list_item(item, 'wind'))
            forecast_items.append(forecast_item)

        return Forecast(get_list_item(dict, 'id'), get_list_item(dict, 'city'), 
                        get_list_item(dict, 'url'), forecast_items)
        
    def get_compact_forecast_from_dictionary(self, dictionary):
        ''' returns a Forecast_compact object containing ForecastItem_compact objects'''
        
        forecast_compact_items = []
        
        for item in get_list_item(dictionary, 'list'):
            compact_forecast_item = ForecastItem_compact(get_list_item(item, 'dt'), get_list_item(item, 'temp'), 
                                                         get_list_item(item, 'night'), get_list_item(item, 'eve'), 
                                                         get_list_item(item, 'morn'), get_list_item(item, 'pressure'), 
                                                         get_list_item(item, 'humidity'), get_list_item(item, 'weather'), 
                                                         get_list_item(item, 'speed'),                                                      get_list_item(item, 'deg'))
            forecast_compact_items.append(compact_forecast_item)
            
        return Forecast_compact(forecast_compact_items)
    
    def open_url_decode_json(self, url):
        ''' open a given url and returns the python object representation of a json string'''
        query_data = urlopen(url)
        return load(query_data)
    
    def open_url_decode_simplejson(self, url):
        ''' open a given url and returns the python object representation of a json string'''
        query_data = urlopen(url).read()
        return simplejson.loads(query_data)
        

    
if __name__ == '__main__':
    pass