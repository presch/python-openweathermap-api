python-openweathermap-api
=========================

The module provides a python wrapper for the open weather api

Installation
--------------------------
> python setup.py install


Usage
--------------------------
`> from pyowm import OpenWeatherMapApi`

get the next 10 stations for a given latitude/longitude
`> api = OpenWeatherMapApi()`
`> stationlist = api.getstationbycoordinates(22.5, 16.3, 10)`

`print the stations`
`> for station in stationlist:`
`>	print station`

Station class: [id=4812, dt=1359571800, name=BGQQ, type=1]  
Station class: [id=4685, dt=1359568800, name=SABE, type=1]  
Station class: [id=6196, dt=1359568800, name=DAAP, type=1]  
Station class: [id=6231, dt=1359568800, name=DAUZ, type=1]  
Station class: [id=6198, dt=1359570600, name=DAAT, type=1]  
Station class: [id=6437, dt=1359571500, name=HLLB, type=1]  
Station class: [id=6873, dt=1359570600, name=FTTJ, type=1]  
Station class: [id=6441, dt=1359571800, name=HLLT, type=1]  
Station class: [id=6438, dt=1359571800, name=HLLM, type=1]  
Station class: [id=6320, dt=1359568800, name=DTTD, type=1]  

print the temperature in degree celsius from the first station
`> print stationlist[0].getmaintempc()`
-21.0

