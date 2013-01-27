#!/usr/bin/env python

import datetime
from utilities import *


class Data(object):
    
    ''' absolute zero point'''
    KELVIN_NULL = 273.15
    ''' one mile has 1.609344 km'''
    KM_MILES = 1.609344
    
    conditions = {'NCT' : 'no clouds detected', 'NSC' : 'nil signifant cloud', 'SKC' : 'clear sky',
                  'CLR' : 'clear sky', 'FEW' :'few clouds','OVC' : 'overcast clouds', 'BKN' : 'broken clouds',
                  'CAVOK' : 'ceiling and visibility ok', 'SCT' : 'scattered'}
    station_types = {'1' : 'Airport station', '2' : 'SWOP station', '3' : 'SYNOP station', '4' : '', 
                     '5' : 'DIY station'}
    
    def get_station(self, nr):
        return self.station_types[str(nr)]
    
    

class Station(object):
    ''' This class represents a weather station'''
    
    def __init__(self, identifier, dt, name, stationtype, coord, distance, main, wind, clouds, rain):
        ''' identificator '''
        self.identifier = identifier
        ''' unixtime GMT'''
        self.dt = dt
        ''' station name'''
        self.name = name
        ''' station type '''
        self.stationtype = stationtype
        ''' location lat lng'''
        self.coord = coord
        ''' distance from coordinates '''
        self.distance = distance
        ''' main data of the station'''
        self.main = main
        ''' wind data of the station '''
        self.wind = wind
        ''' cloud data of the station '''
        self.clouds = clouds
        ''' rain data of the station '''
        self.rain = rain
        
    def get_type_string(self):
        ''' return the type as string'''
        data = Data()
        return data.get_station(self.stationtype)
        
    def get_datetime_string(self):
        ''' return the date and time from the station in the following format year-month-day hour:minute (24hours)'''
        return datetime.datetime.fromtimestamp(self.dt).strftime('%Y-%m-%d %H:%M')
        
    def get_coord_tuple(self):
        ''' return the coordinates as tuple (latitude, longitude'''
        return self.coord['lat'], self.coord['lon']
    
    def get_main_temp(self):
        ''' return the temperature of the station '''
        return get_list_item(self.main, 'temp')
        
    def get_main_temp_c(self):
        ''' return the temperature of the station in degree celsius'''
        return self.get_main_temp() - Data.KELVIN_NULL
    
    def get_main_temp_f(self):
        ''' return the temperature of the station in degree fahrenheit'''
        return (self.get_main_temp_c() * 9) / 5 + 32
        
    def get_main_pressure(self):
        ''' return the atmospheric pressure in kPa'''
        return get_list_item(self.main, 'pressure')
        
    def get_main_humidity(self):
        ''' return the humidity in %'''
        return get_list_item(self.main, 'humidity')
        
    def get_wind_speed(self):
        ''' return the wind speed in mps'''
        get_list_item(self.wind, 'speed')
        
    def get_wind_speed_km(self):
        ''' return the windspeed in kms'''
        if self.get_wind_speed() != None:
            return self.get_wind_speed() * Data.KM_MILES
        
    def get_wind_deg(self):
        ''' return the direction of the wind in degrees(meterological)'''
        return get_list_item(self.wind, 'deg')
        
    def get_wind_gust(self):
        ''' return the speed of wind gust'''
        return get_list_item(self.wind, 'gust')
        
    #def get_wind_varbeg(self):
    #    ''' return the wind direction'''
    #    return get_list_item(self.wind, 'var_beg')
        
    #def get_wind_varend(self):
    #    ''' return the wind direction'''
    #    return get_list_item(self.wind, 'var_end')
        
    def get_clouds_distance(self):
        ''' return the cloud distance'''
        return get_list_item(self.clouds, 'distance')
        
    def get_clouds_conditions(self):
        ''' return the clouds condition '''
        #return get_list_item(self.clouds, 'condition')
        conditions = {}
        if self.clouds != None:
            for element in self.clouds:
                key = element['condition']
                if 'distance' in element:
                    value = element['distance']
                    conditions[key] = value
        return conditions
        
    def get_rain_1h(self):
        ''' return rain in recent hour'''
        return get_list_item(self.rain, '1h')
        
    def get_rain_3h(self):
        ''' return rain in recent 3 hours'''
        return get_list_item(self.rain, '3h')
        
    def get_rain_6h(self):
        ''' return rain in recent 6 hours'''
        return get_list_item(self.rain, '6h')
      
    def get_rain_12h(self):
        ''' return rain in recent 12 hours'''
        return get_list_item(self.rain, '12h')
        
    def get_rain_24h(self):
        ''' return rain in recent 24 hours'''
        return get_list_item(self.rain, '24h')
        
    def get_rain_day(self):
        ''' return rain in recent day'''
        return get_list_item(self.rain, 'day')
        
    def __repr__(self):
        return 'Station class: [id=%s, dt=%s, name=%s, type=%s]' % (self.identifier, self.dt, self.name, self.stationtype) 
    
    
class City(object):
    ''' This class represents the weather information of a city'''
    
    icon_url = 'http://openweathermap.org/img/w/%s.png'
    
    def __init__(self, identifier, name, coord, distance, main, dt, wind, clouds, weather, sys):
        ''' identificator '''
        self.identifier = identifier
        ''' city name'''
        self.name = name
        ''' location lat lng'''
        self.coord = coord
        ''' distance from coordinates'''
        self.distance = distance
        ''' main data of the city'''
        self.main = main
        ''' datetime of the city'''
        self.dt = dt
        ''' wind data of the city'''
        self.wind = wind
        ''' cloud data of the city'''
        self.clouds = clouds
        ''' weather data of the city'''
        self.weather = weather
        ''' ?? '''
        self.sys = sys
        
    def get_temp(self):
        ''' return the current temperature in kelvin'''
        return get_list_item(self.main, 'temp')
    
    def get_temp_c(self):
        ''' return the current temperature in degree celsius'''
        self.get_temp() - Data.KELVIN_NULL
    
    def get_temp_f(self):
        ''' return the current temperature in degree fahrenheit'''
        return (self.get_temp_c() * 9) / 5 + 32
    
    def get_min_temp(self):
        ''' return min temperature'''
        return get_list_item(self.main, 'temp_min')
    
    def get_min_temp_c(self):
        ''' return min temperature in degree celsius'''
        return self.get_min_temp() - Data.KELVIN_NULL
    
    def get_min_temp_f(self):
        ''' return min temperature in degree fahrenheit '''
        return (self.get_min_temp_c() * 9) / 5 + 32
    
    def get_max_temp(self):
        ''' return max temperature'''
        return get_list_item(self.main, 'temp_max')
    
    def get_max_temp_c(self):
        ''' return max temperature in degree celsius'''
        return self.get_max_temp() - Data.KELVIN_NULL
    
    def get_max_temp_f(self):
        ''' return max temperature in degree fahrenheit '''
        return (self.get_max_temp_c() * 9) / 5 + 32
    
    def get_pressure(self):
        ''' return the pressure in hPa '''
        return get_list_item(self.main, 'pressure')
    
    def get_humidity(self):
        ''' return the humitiy in percent'''
        return get_list_item(self.main, 'humidity')
    
    def get_clouds(self):
        ''' return the cloudiness in percent'''
        return get_list_item(self.clouds, 'all')
    
    def get_wind_speed(self):
        ''' return the windspeed in mps'''
        return get_list_item(self.wind, 'speed')
    
    def get_wind_speed_km(self):
        ''' return the windspeed in kms'''
        return self.get_wind_speed() * Data.KM_MILES
    
    def get_wind_deg(self):
        ''' return the wind direction in degrees(meteorological)'''
        return get_list_item(self.wind, 'deg')
    
    def get_wind_gust(self):
        ''' return the wind gust??'''
        return get_list_item(self.wind, 'gust')
    
    def get_weather_id(self):
        ''' return the weather id'''
        return get_list_item(self.weather, 'id')
    
    def get_weather_main(self):
        ''' return the weather main'''
        return get_list_item(self.weather, 'main')
    
    def get_weather_description(self):
        ''' return the weather description'''
        return get_list_item(self.weather, 'description')
            
    def get_weather_icon_url(self):
        ''' return the url to the current weather icon'''
        icon = get_list_item(self.weather, 'icon')
        return self.icon_url % (icon)


class Forecast(object):
    ''' This class represents the forecast in the city for the next 7 days'''
    
    def __init__(self, identifier, city, url, forecast_list):
        self.identifier = identifier
        self.city = city
        self.url = url
        self.forecast_list = forecast_list
        
    def get_city_name(self):
        ''' return the name of the city'''
        return get_list_item(self.city, 'name')
    
    def get_city_country(self):
        ''' return the country of the city'''
        return get_list_item(self.city, 'country')
    
    def get_city_coord_as_tuple(self):
        ''' return the coordinates of the city as tuple'''
        coord = self.city['coord']
        return coord['lat'], coord['long']
    
    def get_city_stations_count(self):
        ''' return the stations count of a city'''
        return get_list_item(self.city, 'stations_count')
    
    def __str__(self):
        return 'Forecast class: [id=%d, name=%s, country=%s]' % (self.id, self.city['name'], self.city['country']) 

class ForecastItem(object):
    ''' This class represents a forecast item of the Forecast object'''
    
    def __init__(self, clouds, snow, dt_txt, weather, main, wind): 
        self.clouds = clouds
        self.snow = snow
        self.dt_txt = dt_txt
        self.weather = weather
        self.main = main
        self.wind = wind
        
    def get_clouds_high(self):
        ''' return the percentage of high clouds'''
        return get_list_item(self.clouds, 'high')
    
    def get_clouds_middle(self):
        ''' return the percentage of middle clouds'''
        return get_list_item(self.clouds, 'middle')
    
    def get_clouds_low(self):
        ''' return the percentage of low clouds'''
        return get_list_item(self.clouds, 'low')
        
    def get_clouds_all(self):
        ''' return the percentage of all clouds'''
        return get_list_item(self.clouds, 'all')
    
    def get_weather_main(self):
        ''' return the weather main'''
        return get_list_item(self.weather, 'main')
    
    def get_weather_id(self):
        ''' return the weather id'''
        return get_list_item(self.weather, 'id')
    
    def get_weather_icon_url(self):
        ''' return the weather icon '''
        icon = get_list_item(self.weather, 'icon')
        return self.icon_url % (icon)
    
    def get_weather_description(self):
        ''' return the weather description'''
        return get_list_item(self.weather, 'description')
    
    def get_main_temp(self):
        ''' return the temperature'''
        return get_list_item(self.main, 'temp')
    
    def get_main_temp_c(self):
        ''' return the temperature in degree celsius'''
        return self.get_main_temp() - Data.KELVIN_NULL
    
    def get_main_temp_f(self):
        ''' return the temperature in degree fahrenheit'''
        return (self.get_temp_c() * 9) / 5 + 32
    
    def get_main_temp_min(self):
        ''' return the minimum temperature'''
        return get_list_item(self.main, 'temp_min')
    
    def get_main_temp_min_c(self):
        ''' return the miniumum temperature in degree celsius'''
        return self.get_main_temp_min() - Data.KELVIN_NULL
    
    def get_main_temp_min_f(self):
        ''' return the minimum temperature in degree fahrenheit'''
        return (self.get_main_temp_min_c() * 9) / 5 + 32
    
    def get_main_temp_max(self):
        ''' return the maximum temperature'''
        return get_list_item(self.main, 'temp_max')
    
    def get_main_temp_max_c(self):
        ''' return the maximum temperature in degree celsisus'''
        return self.get_main_temp_max() - Data.KELVIN_NULL
    
    def get_main_temp_max_f(self):
        ''' return the maximum temperature in degree fahrenheit'''
        return (self.get_main_temp_max_c() * 9) / 5 + 32
    
    def get_main_humidity(self):
        ''' return the humidity in percent'''
        return get_list_item(self.main, 'humidity')
    
    def get_main_pressure(self):
        ''' return the pressure in hpa'''
        return get_list_item(self.main, 'pressure')
    
    def get_wind_gust(self):
        ''' return the speed of wind gust'''
        return get_list_item(self.wind, 'gust')
    
    def get_wind_speed(self):
        ''' return the windspeed in mps'''
        return get_list_item(self.wind, 'speed')
    
    def get_wind_speed_km(self):
        ''' return the windspeed in kms'''
        return self.get_wind_speed() * Data.KM_MILES
    
    def get_wind_deg(self):
        ''' return the wind degree'''
        return get_list_item(self.wind, 'deg')
    
    
class Forecast_compact(object):
    ''' This class represents a compact weather infos for the next 7 days'''
    
    def __init__(self, forecast_list):
        self.forecast_list = forecast_list
    

class ForecastItem_compact(object):
    ''' This class represents compact weather infos for a single day as part of the Compact_Forecast object'''
    def __init__(self, dt, temp, temp_night, temp_eve, temp_morn, pressure, humidity, weather, wind_speed, wind_degree):
        self.datetime = datetime
        self.temp = temp
        self.temp_night = temp_night
        self.temp_eve = temp_eve
        self.temp_morn = temp_morn
        self.pressure = pressure
        self.humidity = humidity
        self.weather = weather
        self.wind_speed = wind_speed
        self.wind_degree = wind_degree
        
    def get_temp_c(self):
        ''' return the temperature in degree celsius'''
        return self.temp - Data.KELVIN_NULL
    
    def get_temp_f(self):
        ''' return the temperature in degree fahrenheit'''
        return (self.temp_c() * 9) / 5 + 32
    
    def get_temp_night_c(self):
        ''' return the night temperature in degree celsius'''
        return self.temp_night - Data.KELVIN_NULL
    
    def get_temp_night_f(self):
        ''' return the night temperature in degree fahrenheit'''
        return (self.temp_night_c()  * 9) / 5 + 32
    
    def get_temp_eve_c(self):
        ''' return the eve temperature in degree celsius'''
        return self.temp_eve - Data.KELVIN_NULL
    
    def get_temp_eve_f(self):
        ''' return the eve temperature in degree fahrenheit'''
        return (self.get_temp_eve_c() * 9) / 5 + 32
    
    def get_temp_morn_c(self):
        ''' return the morn temperature in degree celsius'''
        return self.temp_morn - Data.KELVIN_NULL
    
    def get_temp_morn_f(self):
        ''' return the morn temperature in degree fahrenheit'''
        return (self.get_temp_morn_c() * 9) / 5 + 32
    
    def get_pressure(self):
        ''' return the pressure in hPa '''
        return self.pressure
    
    def get_humidity(self):
        ''' return the humitiy in percent'''
        return self.humidity
    
    def get_weather_main(self):
        ''' return the weather main'''
        return get_list_item(self.weather, 'main')
    
    def get_weather_description(self):
        ''' return the weather description'''
        return get_list_item(self.weather, 'description')
    
    def get_weather_icon_url(self):
        ''' return the url to the weather icon'''
        icon = get_list_item(self.weather, 'icon')
        return self.icon_url % (icon)
    
    def get_wind_speed(self):
        ''' return the windspeed in mps'''
        return self.cloud_speed
    
    def get_wind_speed_km(self):
        ''' return the windspeed in kms'''
        return self.cloud_speed * Data.KM_MILES
    
    def get_wind_deg(self):
        ''' return the wind direction in degrees(meteorological)'''
        return self.cloud_degree
 


if __name__ == '__main__':
    pass