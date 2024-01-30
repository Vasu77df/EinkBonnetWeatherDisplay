from datetime import datetime
import json
from PIL import Image, ImageDraw
from adafruit_epd.epd import Adafruit_EPD
from .utils import (
    small_font,
    medium_font,
    large_font,
    icon_font,
    ICON_MAP,
    WHITE,
    BLACK,
    get_logger,
)

# get logger for this module
logger = get_logger(__name__)


class Weather_Graphics:
    def __init__(self, display, *, am_pm=True, celsius=True, log_level) -> None:
        self.am_pm = am_pm
        self.celsius = celsius

        self.small_font = small_font
        self.medium_font = medium_font
        self.large_font = large_font

        self.display = display

        self._weather_icon = None
        self._city_name = None
        self._main_text = None
        self._temperature = None
        self._description = None
        self._clothes = None
        self._time_text = None
        self._feels_like = None
        self._local_temp = None

    @staticmethod
    def clothes_mapper(temperature: int) -> str:
        if temperature > 20:
            clothes = "Shorts Weather"

        elif temperature > 15 and temperature < 20:
            clothes = "Hoodie day"

        elif temperature > 10 and temperature < 15:
            clothes = "Thick Hoodie"

        elif temperature > 5 and temperature < 10:
            clothes = "Jacket and hoodie"

        elif temperature > -5 and temperature < 5:
            clothes = "Jacket and thick hoodie"
        else:
            clothes = "Heavy Jacket"

        return clothes

    def setup_weather_data(self, weather):
        weather = json.loads(weather.decode("utf-8"))

        # set the icon
        self._weather_icon = ICON_MAP[weather["weather"][0]["icon"]]
        city_name = weather["name"] + ", " + weather["sys"]
        logger.debug(city_name)
        self._city_name = city_name

        main = weather["weather"][0]["main"]
        logger.info(main)
        self._main_text = main

        temperature: int = weather["main"]["temp"] - 273.15  # its in kelvin
        feels_like: int = weather["main"]["feels_like"] - 273.15
        logger.info(temperature)
        logger.info(feels_like)
        if self.celsius:
            self._temperature = "%d °C" % temperature
            self._feels_like = "%d °C" % feels_like
        else:
            self._temperature = "%d °F" % ((temperature * 9 / 5) + 32)
            self._feels_like = "%d °C" % ((feels_like * 9 / 5) + 32)

        description = weather["weather"][0]["description"]
        description = description[0].upper() + description[1:]
        logger.info(description)
        self._description = description
        self._clothes = self.clothes_mapper(feels_like)
        logger.info(self._clothes)
        logger.debug("height: " + str(self.display.height))
        logger.debug("width: " + str(self.display.width))

    def update_time(self) -> None:
        now = datetime.now()
        self._time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")
        self.update_display()

    def update_display(self) -> None:
        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Draw the icon
        (font_width, font_height) = icon_font.getsize(self._weather_icon)
        logger.debug(
            "font width: " + str(font_width) + "font_height: " + str(font_height)
        )
        draw.text(
            self.display.width - font_width // 2 - 40,
            self.display.height - font_height // 2 - 65,
            self._weather_icon,
            font=icon_font,
            fill=BLACK,
        )

        # Draw the city
        draw.text((1, 1), self._city_name, font=self.medium_font, fill=BLACK)

        # Draw the time
        font_width, font_height = medium_font.getsize(self._time_text)
        logger.debug(
            "font width: " + str(font_width) + "font_height: " + str(font_height)
        )
        draw.text(
            (1, font_height * 2 - 16),
            self._time_text,
            font=self.medium_font,
            fill=BLACK,
        )

        # Draw the feels like
        (font_width, font_height) = medium_font.getsize(self._feels_like)
        print(
            "feels like font width: "
            + str(font_width)
            + "font_height: "
            + str(font_height)
        )
        draw.text(
            (1, self.display.height - font_height * 5 + 10),
            "feels like: " + self._feels_like,
            font=self.medium_font,
            fill=BLACK,
        )

        # Draw the description
        (font_width, font_height) = small_font.getsize(self._description)
        print(
            "desc font width: " + str(font_width) + "font_height: " + str(font_height)
        )
        draw.text(
            (5, self.display.height - font_height - 7),
            self._description,
            font=self.medium_font,
            fill=BLACK,
        )
        # Draw the temperature
        (font_width, font_height) = large_font.getsize(self._temperature)
        print(
            "temp font width: " + str(font_width) + "font_height: " + str(font_height)
        )
        draw.text(
            (
                self.display.width - font_width - 5,
                self.display.height - font_height * 3,
            ),
            self._temperature,
            font=self.large_font,
            fill=BLACK,
        )
        # Draw the clothes suggections
        (font_width, font_height) = small_font.getsize(self._clothes)
        print(
            "clothes font width: "
            + str(font_width)
            + "font_height: "
            + str(font_height)
        )
        draw.text(
            (1, self.display.height - font_height - 30),
            self._clothes,
            font=self.medium_font,
            fill=BLACK,
        )
        # render on screen
        self.display.image(image)
        self.display.display()
