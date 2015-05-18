#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import httplib 
import json
import time


OK_STATUS = (200, 201, 202, 204)

WIND_ICON = {
    "N":   "\033[1m↓\033[0m",
    "NE":  "\033[1m↙\033[0m",
    "E":   "\033[1m←\033[0m",
    "SE":  "\033[1m↖\033[0m",
    "S":   "\033[1m↑\033[0m",
    "SW":  "\033[1m↗\033[0m",
    "W":   "\033[1m→\033[0m",
    "NW":  "\033[1m↘\033[0m"
}

WEATHER_ICON = {
    "unknown": (
        "    .-.      ",
        "     __)     ",
        "    (        ",
        "     `-’     ",
        "      •      "),
    "sunny": (
        "\033[38;5;226m    \\   /    \033[0m",
        "\033[38;5;226m     .-.     \033[0m",
        "\033[38;5;226m  ― (   ) ―  \033[0m",
        "\033[38;5;226m     `-’     \033[0m",
        "\033[38;5;226m    /   \\    \033[0m"),
    "partlyCloudy": (
        "\033[38;5;226m   \\  /\033[0m      ",
        "\033[38;5;226m _ /\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m   \\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "             "),
    "cloudy": (
        "             ",
        "\033[38;5;250m     .--.    \033[0m",
        "\033[38;5;250m  .-(    ).  \033[0m",
        "\033[38;5;250m (___.__)__) \033[0m",
        "             "),
    "veryCloudy": (
        "             ",
        "\033[38;5;240;1m     .--.    \033[0m",
        "\033[38;5;240;1m  .-(    ).  \033[0m",
        "\033[38;5;240;1m (___.__)__) \033[0m",
        "             "),
    "lightShowers": (
        "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;111m     ‘ ‘ ‘ ‘ \033[0m",
        "\033[38;5;111m    ‘ ‘ ‘ ‘  \033[0m"),
    "heavyShowers": (
        "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
        "\033[38;5;21;1m   ‚‘‚‘‚‘‚‘  \033[0m",
        "\033[38;5;21;1m   ‚’‚’‚’‚’  \033[0m"),
    "lightSnowShowers": (
        "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;255m     *  *  * \033[0m",
        "\033[38;5;255m    *  *  *  \033[0m"),
    "heavySnowShowers": (
        "\033[38;5;226m _`/\"\"\033[38;5;240;1m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;240;1m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;240;1m(___(__) \033[0m",
        "\033[38;5;255;1m    * * * *  \033[0m",
        "\033[38;5;255;1m   * * * *   \033[0m"),
    "lightSleetShowers": (
        "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;111m     ‘ \033[38;5;255m*\033[38;5;111m ‘ \033[38;5;255m* \033[0m",
        "\033[38;5;255m    *\033[38;5;111m ‘ \033[38;5;255m*\033[38;5;111m ‘  \033[0m"),
    "thunderyShowers": (
        "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;228;5m    ⚡\033[38;5;111;25m‘ ‘\033[38;5;228;5m⚡\033[38;5;111;25m‘ ‘ \033[0m",
        "\033[38;5;111m    ‘ ‘ ‘ ‘  \033[0m"),
    "thunderyHeavyRain": (
        "\033[38;5;240;1m     .-.     \033[0m",
        "\033[38;5;240;1m    (   ).   \033[0m",
        "\033[38;5;240;1m   (___(__)  \033[0m",
        "\033[38;5;21;1m  ‚‘\033[38;5;228;5m⚡\033[38;5;21;25m‘‚\033[38;5;228;5m⚡\033[38;5;21;25m‚‘   \033[0m",
        "\033[38;5;21;1m  ‚’‚’\033[38;5;228;5m⚡\033[38;5;21;25m’‚’   \033[0m"),
    "thunderySnowShowers": (
        "\033[38;5;226m _`/\"\"\033[38;5;250m.-.    \033[0m",
        "\033[38;5;226m  ,\\_\033[38;5;250m(   ).  \033[0m",
        "\033[38;5;226m   /\033[38;5;250m(___(__) \033[0m",
        "\033[38;5;255m     *\033[38;5;228;5m⚡\033[38;5;255;25m *\033[38;5;228;5m⚡\033[38;5;255;25m * \033[0m",
        "\033[38;5;255m    *  *  *  \033[0m"),
    "lightRain": (
        "\033[38;5;250m     .-.     \033[0m",
        "\033[38;5;250m    (   ).   \033[0m",
        "\033[38;5;250m   (___(__)  \033[0m",
        "\033[38;5;111m    ‘ ‘ ‘ ‘  \033[0m",
        "\033[38;5;111m   ‘ ‘ ‘ ‘   \033[0m"),
    "heavyRain": (
        "\033[38;5;240;1m     .-.     \033[0m",
        "\033[38;5;240;1m    (   ).   \033[0m",
        "\033[38;5;240;1m   (___(__)  \033[0m",
        "\033[38;5;21;1m  ‚‘‚‘‚‘‚‘   \033[0m",
        "\033[38;5;21;1m  ‚’‚’‚’‚’   \033[0m"),
    "lightSnow": (
        "\033[38;5;250m     .-.     \033[0m",
        "\033[38;5;250m    (   ).   \033[0m",
        "\033[38;5;250m   (___(__)  \033[0m",
        "\033[38;5;255m    *  *  *  \033[0m",
        "\033[38;5;255m   *  *  *   \033[0m"),
    "heavySnow": (
        "\033[38;5;240;1m     .-.     \033[0m",
        "\033[38;5;240;1m    (   ).   \033[0m",
        "\033[38;5;240;1m   (___(__)  \033[0m",
        "\033[38;5;255;1m   * * * *   \033[0m",
        "\033[38;5;255;1m  * * * *    \033[0m"),
    "lightSleet": (
        "\033[38;5;250m     .-.     \033[0m",
        "\033[38;5;250m    (   ).   \033[0m",
        "\033[38;5;250m   (___(__)  \033[0m",
        "\033[38;5;111m    ‘ \033[38;5;255m*\033[38;5;111m ‘ \033[38;5;255m*  \033[0m",
        "\033[38;5;255m   *\033[38;5;111m ‘ \033[38;5;255m*\033[38;5;111m ‘   \033[0m"),
    "fog": (
        "             ",
        "\033[38;5;251m _ - _ - _ - \033[0m",
        "\033[38;5;251m  _ - _ - _  \033[0m",
        "\033[38;5;251m _ - _ - _ - \033[0m",
        "             ")
}

WEATHER_MAPE = {
    800: 'sunny',
    801: 'partlyCloudy',
    802: 'cloudy',
    803: 'veryCloudy',
    804: 'veryCloudy',
    620: 'lightSnowShowers',
    621: 'lightSnowShowers',
    622: 'heavySnowShowers',
    612: 'lightSleetShowers',
    211: 'thunderyShowers',
    201: 'thunderyHeavyRain',
    202: 'thunderyHeavyRain',
    500: 'lightRain',
    501: 'lightRain',
    521: 'lightRain',
    502: 'heavyRain',
    503: 'heavyRain',
    504: 'heavyRain',
    522: 'heavyRain',
    600: 'lightSnow',
    601: 'lightSnow',
    602: 'heavySnow',
    611: 'lightSleet',
    200: 'fog',
}


class WeatherFormat(object):
    def __init__(self, data):
        weather = data['weather'][0]
        self.id = weather['id']
        self.main = weather['main']
        self.description = weather['description']
        #(NOTE) UTC vs Localtime
        self.dt = data['dt']
        self.data = data

        if self.id in WEATHER_MAPE:
            self.weather_icon = copy.deepcopy(WEATHER_ICON[WEATHER_MAPE[self.id]])
        else:
            self.weather_icon = copy.deepcopy(WEATHER_ICON['unknown'])

    def get_wind_icon(self):
        if self.wind_deg >= 337.5 or self.wind_deg < 22.5:
            wind_icon = WIND_ICON['N']
        elif self.wind_deg >= 22.5 and self.wind_deg < 67.5:
            wind_icon = WIND_ICON['NE']
        elif self.wind_deg >= 67.5 and self.wind_deg < 112.5:
            wind_icon = WIND_ICON['E']
        elif self.wind_deg >= 112.5 and self.wind_deg < 157.5:
            wind_icon = WIND_ICON['SE']
        elif self.wind_deg >= 157.5 and self.wind_deg < 202.5:
            wind_icon = WIND_ICON['S']
        elif self.wind_deg >= 202.5 and self.wind_deg < 247.5:
            wind_icon = WIND_ICON['SW']
        elif self.wind_deg >= 247.5 and self.wind_deg < 292.5:
            wind_icon = WIND_ICON['W']
        elif self.wind_deg >= 292.5 and self.wind_deg < 337.5:
            wind_icon = WIND_ICON['NW']

        return wind_icon

    def format_today(self):
        temp = self.data['temp']
        self.temp_min = temp['min']
        self.temp_max = temp['max']
        self.pressure = self.data['pressure']
        self.humidity = self.data['humidity']
        self.wind_deg = self.data['deg']
        self.wind_speed = self.data['speed']
        self.wind_icon = self.get_wind_icon()

        wind_ret = self.wind_icon + '  ' + str(self.wind_speed) + ' m/s'
        temp_ret = str(self.temp_min) + ' - ' + str(self.temp_max) + ' °C' 

        ret = list(self.weather_icon)
        ret[0] += self.main
        ret[1] += self.description
        ret[2] += wind_ret
        ret[3] += temp_ret
        ret[4] += 'Humidity: ' + str(self.humidity)

        return ret

    def format_forecast(self):
        pass


class OpenWeatherMap(object):
    def __init__(self):
        # City name.
        self.q = 'beijing'
        self.city = None
        self.country = None
        self.APPID = None
        self.host = 'api.openweathermap.org'
        self.forecast_path = '/data/2.5/forecast?units=metric&q=' + self.q
        self.today_path = '/data/2.5/forecast/daily?units=metric&cnt=1&q=' + self.q

    def http_request(self, path):
        # try:...  We need handle exception here.

        conn = httplib.HTTPConnection(self.host)
        conn.request('GET', path)

        res = conn.getresponse()
        if res.status in (200, 201, 202, 204):
            return res.read()

    def parse_forecast_weather(self):
        resp = self.http_request(self.forecast_path)
        data = json.loads(resp)

        return data['list'] 

    def parse_today_weather(self):
        resp = self.http_request(self.today_path)
        data = json.loads(resp)

        self.city = data['city']['name']
        self.country = data['city']['country']
        today_data = data['list'][0]

        return today_data 


def print_city_info(city, country):
    print("Weather for City: %s  %s\n" %(city, country))


def print_today_weather(data):
    today = WeatherFormat(data)
    ret = today.format_today()

    for line in ret:
        print(line)

    print('\n')


def print_forecast_weather():
    pass


def print_day_weather():
    pass

if '__main__' == __name__:
    weather = OpenWeatherMap()
    today_data = weather.parse_today_weather()
    forecast_data = weather.parse_forecast_weather()
    print_city_info(weather.city, weather.country)
    print_today_weather(today_data)
