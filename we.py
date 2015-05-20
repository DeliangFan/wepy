#!/usr/bin/python
# -*- coding: utf-8 -*-

import httplib 
import json

import copy
import sys
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

TEMP_COLOR = {
    0: '27',
    1: '39',
    2: '51',
    3: '49',
    4: '47',
    5: '82',
    6: '190',
    7: '154',
    8: '214',
    9: '220',
}

WIND_COLOR = {
    0: '82',
    1: '118',
    2: '154',
    3: '190',
    4: '226',
    5: '220',
    6: '214',
    7: '208',
    9: '202',
}


class WeatherFormat(object):
    def __init__(self, data):
        weather = data['weather'][0]
        self.id = weather['id']
        self.main = weather['main']

        if len(weather['description']) >= 16:
            self.description = weather['description'][0:16]
        else:
            self.description = weather['description']

        if self.id in WEATHER_MAPE:
            self.weather_icon = copy.deepcopy(WEATHER_ICON[WEATHER_MAPE[self.id]])
        else:
            self.weather_icon = copy.deepcopy(WEATHER_ICON['unknown'])

        self.dt = data['dt']
        self.date = time.asctime(time.localtime(self.dt))[0:10]
        self.data = data

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

    def color_wind(self, wind_speed):
        if int(wind_speed * 1.2) >= 9:
            color = WIND_COLOR[9]
        else:
            color = WIND_COLOR[int(wind_speed * 1.2)]

        return "\033[38;5;" + color + "m" + str(wind_speed) + "\033[0m"

    def color_temp(self, temp):
        temp += 15
        if temp < 0:
            color = TEMP_COLOR[0]
        elif temp > 56:
            color = TEMP_COLOR[9]
        else:
            color = TEMP_COLOR[int(temp / 7)]

        return "\033[38;5;" + color + "m" + str(temp - 15) + "\033[0m" 

    def color_date(self, date):
        return "\033[38;5;202m" + date + "\033[0m"

    def color_main(self, main):
        return "\033[1;5;32m" + main + "\033[0m"

    def format_daily(self):

        temp = self.data['temp']
        self.temp_min = temp['min']
        self.temp_max = temp['max']
        self.pressure = self.data['pressure']
        self.humidity = self.data['humidity']
        self.wind_deg = self.data['deg']
        self.wind_speed = self.data['speed']
        self.wind_icon = self.get_wind_icon()

        wind_ret = self.wind_icon +  "  " + self.color_wind(self.wind_speed)  + " m/s"
        temp_ret = self.color_temp(self.temp_min) + " - " + self.color_temp(self.temp_max) + ' °C' 

        ret = list(self.weather_icon)
        ret[0] += self.color_main(self.main)
        ret[1] += self.description
        ret[2] += wind_ret
        ret[3] += temp_ret
        ret[4] += 'Humidity: ' + str(self.humidity)
        ret.append(self.color_date(self.date))

        length = [len(self.main) + 17,
                  len(self.description) + 17,
                  len('  ' + str(self.wind_speed) + ' m/s') + 18,
                  len(str(self.temp_min) + " - " + str(self.temp_max) + ' °C') + 16,
                  len('Humidity: ' + str(self.humidity)) + 17]

        ret.append(length)

        return ret


class OpenWeatherMap(object):
    def __init__(self, q=None):
        # City name.
        self.q = q or 'beijing'
        self.city = None
        self.country = None
        self.APPID = None
        self.host = 'api.openweathermap.org'
        self.today_path = '/data/2.5/forecast/daily?units=metric&cnt=15&q=' + self.q

    def http_request(self, path):
        # try:...  We need handle exception here.

        conn = httplib.HTTPConnection(self.host)
        conn.request('GET', path)

        res = conn.getresponse()
        if res.status in (200, 201, 202, 204):
            body = res.read()
        else:
            body = None

        conn.close()

        return body

    def get_weather_data(self):
        resp = self.http_request(self.today_path)
        # TypeError: expected string or buffer

        if not resp:
            exit(0)

        data = json.loads(resp)


        self.city = data['city']['name']
        self.country = data['city']['country']
        data = data['list']

        return data 


class PrintWeather(object):
    def __init__(self, data):
        self.data = data
        self.lines = [ 
            "┌──────────────────────────────┬──────────────────────────────┬──────────────────────────────┬──────────────────────────────┐",
            "│                              │                              |                              │                              │",
            "├──────────────────────────────┼──────────────────────────────┼──────────────────────────────┼──────────────────────────────┤",
            "|                              |                              |                              |                              |",
            "|                              |                              |                              |                              |",
            "|                              |                              |                              |                              |",
            "|                              |                              |                              |                              |",
            "|                              |                              |                              |                              |",
            "└──────────────────────────────┴──────────────────────────────┴──────────────────────────────┴──────────────────────────────┘"]

    def prepare_date(self):
        d_line = ""
        for i in range(4):
            d_line += "│          " + self.data[i][5]  + "          "
        d_line += "|"
        self.lines[1] = d_line

    def prepare_weather(self):
        for i in range(5):
            w_line = ""
            for j in range(4):
                if self.data[j][6][i] <= 34:
                    w_line += "|" + self.data[j][i] + " " * (34 -self.data[j][6][i])
                else:
                    w_line += "|" + self.data[j][i][0:34]
            w_line += "|"
            self.lines[i + 3] = w_line


def print_city_info(city, country):
    city_info = "\n\033[38;5;202mWeather for City: \033[0m"
    city_info += "\033[1;5;32m" + city + " " + country + "\033[0m\n"
    print(city_info)


if '__main__' == __name__:
    if len(sys.argv) == 1:
        weather = OpenWeatherMap()
    else:
        weather = OpenWeatherMap(sys.argv[1])

    data = weather.get_weather_data()

    format_data = []
    for d in data[0:12]:
        daily_data = WeatherFormat(d)
        format_data.append(daily_data.format_daily())

    print_city_info(weather.city, weather.country)

    for i in range(3):
        p = PrintWeather(format_data[4*i: 4*i + 4])
        p.prepare_date()
        p.prepare_weather()
        for j in range(9):
            print(p.lines[j])
        print('\n')
    
