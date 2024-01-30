from .display_weather import Eink_Weather

# from .display_weather import Weather

if __name__ == "__main__":
    weather = Eink_Weather("AUSTIN, US")
    # weather = Weather("AUSTIN, US")
    output = weather.get_weather_data()
    weather.display()
