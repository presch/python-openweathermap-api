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
    stationtypes = {'1' : 'Airport station', '2' : 'SWOP station', '3' : 'SYNOP station', '4' : '', 
                     '5' : 'DIY station'}
    
    def getstation(self, nr):
        return self.stationtypes[str(nr)]
    
    

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
        
    def gettypestring(self):
        ''' return the type as string'''
        data = Data()
        return data.getstation(self.stationtype)
        
    def getdatetimestring(self):
        ''' return the date and time from the station in the following format year-month-day hour:minute (24hours)'''
        return datetime.datetime.fromtimestamp(self.dt).strftime('%Y-%m-%d %H:%M')
        
    def getcoordtuple(self):
        ''' return the coordinates as tuple (latitude, longitude'''
        return self.coord['lat'], self.coord['lon']
    
    def getmaintemp(self):
        ''' return the temperature of the station '''
        return getlistitem(self.main, 'temp')
        
    def getmaintempc(self):
        ''' return the temperature of the station in degree celsius'''
        return self.getmaintemp() - Data.KELVIN_NULL
    
    def getmaintempf(self):
        ''' return the temperature of the station in degree fahrenheit'''
        return (self.getmaintempc() * 9) / 5 + 32
        
    def getmainpressure(self):
        ''' return the atmospheric pressure in kPa'''
        return getlistitem(self.main, 'pressure')
        
    def getmainhumidity(self):
        ''' return the humidity in %'''
        return getlistitem(self.main, 'humidity')
        
    def getwindspeed(self):
        ''' return the wind speed in mps'''
        getlistitem(self.wind, 'speed')
        
    def getwindspeedkm(self):
        ''' return the windspeed in kms'''
        if self.getwindspeed() != None:
            return self.getwindspeed() * Data.KM_MILES
        
    def getwinddeg(self):
        ''' return the direction of the wind in degrees(meterological)'''
        return getlistitem(self.wind, 'deg')
        
    def getwindgust(self):
        ''' return the speed of wind gust'''
        return getlistitem(self.wind, 'gust')
        
    #def getwindvarbeg(self):
    #    ''' return the wind direction'''
    #    return getlistitem(self.wind, 'var_beg')
        
    #def getwindvarend(self):
    #    ''' return the wind direction'''
    #    return getlistitem(self.wind, 'var_end')
        
    def getcloudsdistance(self):
        ''' return the cloud distance'''
        return getlistitem(self.clouds, 'distance')
        
    def getcloudsconditions(self):
        ''' return the clouds condition '''
        #return getlistitem(self.clouds, 'condition')
        conditions = {}
        if self.clouds != None:
            for element in self.clouds:
                key = element['condition']
                if 'distance' in element:
                    value = element['distance']
                    conditions[key] = value
        return conditions
        
    def getrain1h(self):
        ''' return rain in recent hour'''
        return getlistitem(self.rain, '1h')
        
    def getrain3h(self):
        ''' return rain in recent 3 hours'''
        return getlistitem(self.rain, '3h')
        
    def getrain6h(self):
        ''' return rain in recent 6 hours'''
        return getlistitem(self.rain, '6h')
      
    def getrain12h(self):
        ''' return rain in recent 12 hours'''
        return getlistitem(self.rain, '12h')
        
    def getrain24h(self):
        ''' return rain in recent 24 hours'''
        return getlistitem(self.rain, '24h')
        
    def getrainday(self):
        ''' return rain in recent day'''
        return getlistitem(self.rain, 'day')
        
    def __repr__(self):
        return 'Station class: [id=%s, dt=%s, name=%s, type=%s]' % (self.identifier, self.dt, self.name, self.stationtype) 
    
    
class City(object):
    ''' This class represents the weather information of a city'''
    
    ICON_URL = 'http://openweathermap.org/img/w/%s.png'
    
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
        
    def getcoordtuple(self):
        ''' return the coordinates as tuple (latitude, longitude'''
        return self.coord['lat'], self.coord['lon']
        
    def getmaintemp(self):
        ''' return the current temperature in kelvin'''
        return getlistitem(self.main, 'temp')
    
    def getmaintempc(self):
        ''' return the current temperature in degree celsius'''
        return self.getmaintemp() - Data.KELVIN_NULL
    
    def getmaintempf(self):
        ''' return the current temperature in degree fahrenheit'''
        return (self.getmaintempc() * 9) / 5 + 32
    
    def getmainmintemp(self):
        ''' return min temperature'''
        return getlistitem(self.main, 'temp_min')
    
    def getmainmintempc(self):
        ''' return min temperature in degree celsius'''
        return self.getmainmintemp() - Data.KELVIN_NULL
    
    def getmainmintempf(self):
        ''' return min temperature in degree fahrenheit '''
        return (self.getmainmintempc() * 9) / 5 + 32
    
    def getmainmaxtemp(self):
        ''' return max temperature'''
        return getlistitem(self.main, 'temp_max')
    
    def getmainmaxtempc(self):
        ''' return max temperature in degree celsius'''
        return self.getmainmaxtemp() - Data.KELVIN_NULL
    
    def getmainmaxtempf(self):
        ''' return max temperature in degree fahrenheit '''
        return (self.getmainmaxtempc() * 9) / 5 + 32
    
    def getmainpressure(self):
        ''' return the pressure in hPa '''
        return getlistitem(self.main, 'pressure')
    
    def getmainhumidity(self):
        ''' return the humitiy in percent'''
        return getlistitem(self.main, 'humidity')
    
    def getclouds(self):
        ''' return the cloudiness in percent'''
        return getlistitem(self.clouds, 'all')
    
    def getwindspeed(self):
        ''' return the windspeed in mps'''
        return getlistitem(self.wind, 'speed')
    
    def getwindspeedkm(self):
        ''' return the windspeed in kms'''
        return self.getwindspeed() * Data.KM_MILES
    
    def getwinddeg(self):
        ''' return the wind direction in degrees(meteorological)'''
        return getlistitem(self.wind, 'deg')
    
    def getwindgust(self):
        ''' return the wind gust??'''
        return getlistitem(self.wind, 'gust')
    
    def getweatherid(self):
        ''' return the weather id'''
        return getlistitem(self.weather, 'id')
    
    def getweathermain(self):
        ''' return the weather main'''
        return getlistitem(self.weather, 'main')
    
    def getweatherdescription(self):
        ''' return the weather description'''
        return getlistitem(self.weather, 'description')
            
    def getweathericonurl(self):
        ''' return the url to the current weather icon'''
        icon = getlistitem(self.weather, 'icon')
        return self.ICON_URL % (icon)
    
    def __repr__(self):
        return 'City class: [id=%s, dt=%s, name=%s]' % (self.identifier, self.dt, self.name) 


class Forecast(object):
    ''' This class represents the forecast in the city for the next 7 days'''
    
    def __init__(self, identifier, city, url, forecastlist):
        self.identifier = identifier
        self.city = city
        self.url = url
        self.forecastlist = forecastlist
        
    def getcityname(self):
        ''' return the name of the city'''
        return getlistitem(self.city, 'name')
    
    def getcitycountry(self):
        ''' return the country of the city'''
        return getlistitem(self.city, 'country')
    
    def getcitycoordastuple(self):
        ''' return the coordinates of the city as tuple'''
        coord = self.city['coord']
        return coord['lat'], coord['long']
    
    def getcitystationscount(self):
        ''' return the stations count of a city'''
        return getlistitem(self.city, 'stations_count')
    
    def __repr__(self):
        return 'Forecast class: [id=%d, name=%s, country=%s]' % (self.id, self.city['name'], self.city['country']) 

class ForecastItem(object):
    ''' This class represents a forecast item of the Forecast object'''
    
    def __init__(self, clouds, snow, dttxt, weather, main, wind): 
        self.clouds = clouds
        self.snow = snow
        self.dttxt = dttxt
        self.weather = weather
        self.main = main
        self.wind = wind
        
    def getcloudshigh(self):
        ''' return the percentage of high clouds'''
        return getlistitem(self.clouds, 'high')
    
    def getcloudsmiddle(self):
        ''' return the percentage of middle clouds'''
        return getlistitem(self.clouds, 'middle')
    
    def getcloudslow(self):
        ''' return the percentage of low clouds'''
        return getlistitem(self.clouds, 'low')
        
    def getcloudsall(self):
        ''' return the percentage of all clouds'''
        return getlistitem(self.clouds, 'all')
    
    def getweathermain(self):
        ''' return the weather main'''
        return getlistitem(self.weather, 'main')
    
    def getweatherid(self):
        ''' return the weather id'''
        return getlistitem(self.weather, 'id')
    
    def getweathericonurl(self):
        ''' return the weather icon '''
        icon = getlistitem(self.weather, 'icon')
        return self.ICON_URL % (icon)
    
    def getweatherdescription(self):
        ''' return the weather description'''
        return getlistitem(self.weather, 'description')
    
    def getmaintemp(self):
        ''' return the temperature'''
        return getlistitem(self.main, 'temp')
    
    def getmaintempc(self):
        ''' return the temperature in degree celsius'''
        return self.getmaintemp() - Data.KELVIN_NULL
    
    def getmaintempf(self):
        ''' return the temperature in degree fahrenheit'''
        return (self.gettempc() * 9) / 5 + 32
    
    def getmaintempmin(self):
        ''' return the minimum temperature'''
        return getlistitem(self.main, 'temp_min')
    
    def getmaintempminc(self):
        ''' return the miniumum temperature in degree celsius'''
        return self.getmaintempmin() - Data.KELVIN_NULL
    
    def getmaintempminf(self):
        ''' return the minimum temperature in degree fahrenheit'''
        return (self.getmaintempminc() * 9) / 5 + 32
    
    def getmaintempmax(self):
        ''' return the maximum temperature'''
        return getlistitem(self.main, 'temp_max')
    
    def getmaintempmaxc(self):
        ''' return the maximum temperature in degree celsisus'''
        return self.getmaintempmax() - Data.KELVIN_NULL
    
    def getmaintempmaxf(self):
        ''' return the maximum temperature in degree fahrenheit'''
        return (self.getmaintempmaxc() * 9) / 5 + 32
    
    def getmainhumidity(self):
        ''' return the humidity in percent'''
        return getlistitem(self.main, 'humidity')
    
    def getmainpressure(self):
        ''' return the pressure in hpa'''
        return getlistitem(self.main, 'pressure')
    
    def getwindgust(self):
        ''' return the speed of wind gust'''
        return getlistitem(self.wind, 'gust')
    
    def getwindspeed(self):
        ''' return the windspeed in mps'''
        return getlistitem(self.wind, 'speed')
    
    def getwindspeedkm(self):
        ''' return the windspeed in kms'''
        return self.getwindspeed() * Data.KM_MILES
    
    def getwinddeg(self):
        ''' return the wind degree'''
        return getlistitem(self.wind, 'deg')
    
    def __repr__(self):
        return 'ForecastItem class: [weather=%s, temp=%f, mintemp=%f, maxtemp=%f, windspeed=%f]' % (self.getweathermain(), self.getmaintempc(), self.getmaintempmaxc(), self.getwindspeedkm())
    
    
class Forecastcompact(object):
    ''' This class represents a compact weather infos for the next 7 days'''
    
    def __init__(self, forecastlist):
        self.forecastlist = forecastlist
    

class ForecastItemcompact(object):
    
    ICON_URL = 'http://openweathermap.org/img/w/%s.png'
    
    ''' This class represents compact weather infos for a single day as part of the Compact_Forecast object'''
    def __init__(self, dt, temp, tempnight, tempeve, tempmorn, pressure, humidity, weather, windspeed, winddegree):
        self.datetime = datetime
        self.temp = temp
        self.tempnight = tempnight
        self.tempeve = tempeve
        self.tempmorn = tempmorn
        self.pressure = pressure
        self.humidity = humidity
        self.weather = weather
        self.windspeed = windspeed
        self.winddegree = winddegree
        
    def gettempc(self):
        ''' return the temperature in degree celsius'''
        return self.temp - Data.KELVIN_NULL
    
    def gettempf(self):
        ''' return the temperature in degree fahrenheit'''
        return (self.tempc() * 9) / 5 + 32
    
    def gettempnightc(self):
        ''' return the night temperature in degree celsius'''
        return self.tempnight - Data.KELVIN_NULL
    
    def gettempnightf(self):
        ''' return the night temperature in degree fahrenheit'''
        return (self.tempnightc()  * 9) / 5 + 32
    
    def gettempevec(self):
        ''' return the eve temperature in degree celsius'''
        return self.tempeve - Data.KELVIN_NULL
    
    def gettempevef(self):
        ''' return the eve temperature in degree fahrenheit'''
        return (self.gettempevec() * 9) / 5 + 32
    
    def gettempmornc(self):
        ''' return the morn temperature in degree celsius'''
        return self.tempmorn - Data.KELVIN_NULL
    
    def gettempmornf(self):
        ''' return the morn temperature in degree fahrenheit'''
        return (self.gettempmornc() * 9) / 5 + 32
    
    def getpressure(self):
        ''' return the pressure in hPa '''
        return self.pressure
    
    def gethumidity(self):
        ''' return the humitiy in percent'''
        return self.humidity
    
    def getweathermain(self):
        ''' return the weather main'''
        return getlistitem(self.weather, 'main')
    
    def getweatherdescription(self):
        ''' return the weather description'''
        return getlistitem(self.weather, 'description')
    
    def getweathericonurl(self):
        ''' return the url to the weather icon'''
        icon = getlistitem(self.weather, 'icon')
        return self.ICON_URL % (icon)
    
    def getwindspeed(self):
        ''' return the windspeed in mps'''
        return self.cloudspeed
    
    def getwindspeedkm(self):
        ''' return the windspeed in kms'''
        return self.cloudspeed * Data.KM_MILES
    
    def getwinddeg(self):
        ''' return the wind direction in degrees(meteorological)'''
        return self.clouddegree
 


if __name__ == '__main__':
    pass