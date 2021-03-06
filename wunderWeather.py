#!/usr/bin/env python

import urllib2
import json
import os

# The Wunderground API key, city, and state should be store in the home directory
config_path = os.path.join(os.path.expanduser('~'), '.weather_config.json')
f = open(config_path, 'r')
config_raw = f.read()
f.close()

config_json = json.loads(config_raw)
api_key = config_json['api_key']
state = config_json['state']
city = config_json['city']

url_raw = "http://api.wunderground.com/api/{0}/conditions/astronomy/forecast/q/{1}/{2}.json".format(
        api_key, state, city)

wurl = urllib2.urlopen(url_raw)
json_string = wurl.read()
parsed_json = json.loads(json_string)

temp_f = parsed_json['current_observation']['temp_f']
conditions = parsed_json['current_observation']['weather']
relative_humidity = parsed_json['current_observation']['relative_humidity']
visi = parsed_json['current_observation']['visibility_mi']
wind_string = parsed_json['current_observation']['wind_string'].replace("F", "f")
wind = wind_string.replace("Gusting", "\nGusting")
UV = parsed_json['current_observation']['UV']
sunrise_hour = parsed_json['moon_phase']['sunrise']['hour']
sunrise_minute = parsed_json['moon_phase']['sunrise']['minute']
sunset_hour = parsed_json['moon_phase']['sunset']['hour']
sunset_minute = parsed_json['moon_phase']['sunset']['minute']

print "Weather for {0}, {1}".format(city, state)
print temp_f, "F"
print conditions
print "Humidity:", relative_humidity
print "Wind", wind
print "Visibility:", visi, "miles"
print "Sunrise @ " + sunrise_hour + ":" + sunrise_minute
print "Sunset @ " + sunset_hour + ":" + sunset_minute
print "UV Index:", UV, "\n"

for data in parsed_json['forecast']['simpleforecast']['forecastday']:
    print data['date']['weekday'] + ':'
    print data['conditions']
    print "Highs:", data['high']['fahrenheit'], "Lows:", data['low']['fahrenheit'], "\n", data['pop'], "% Chance of rain \n"

wurl.close()
