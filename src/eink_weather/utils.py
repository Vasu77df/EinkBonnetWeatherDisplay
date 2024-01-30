from PIL import ImageFont
import logging
from logging import Logger
import sys

# OpenWeather constants
OPEN_WEATHER_TOKEN = "dd5792cff21790d86f018738d0df7dbd"
DATA_SOURCE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Map the OpenWeatherMap icon code to the appropriate font character
# See http://www.alessioatzeni.com/meteocons/ for icons
ICON_MAP = {
    "01d": "B",
    "01n": "C",
    "02d": "H",
    "02n": "I",
    "03d": "N",
    "03n": "N",
    "04d": "Y",
    "04n": "Y",
    "09d": "Q",
    "09n": "Q",
    "10d": "R",
    "10n": "R",
    "11d": "Z",
    "11n": "Z",
    "13d": "W",
    "13n": "W",
    "50d": "J",
    "50n": "K",
}

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
small_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
)
medium_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18
)
large_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44
)
icon_font = ImageFont.truetype("/usr/share/fonts/truetype/meteocon/meteocons.ttf", 36)


def get_logger(logger_name: str, log_level: str = "INFO") -> Logger:
    file_formatter = logging.Formatter(
        "%(asctime)s~%(levelname)s~%(message)s~module:%(module)s~function:%(module)s"
    )
    console_formatter = logging.Formatter("%(levelname)s -- %(message)s")

    file_handler = logging.FileHandler("/var/log/eink_weather.log")
    file_handler.setFormatter(file_formatter)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger(logger_name)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    if log_level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return logger
