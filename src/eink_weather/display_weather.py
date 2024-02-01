import time
import urllib.request
import urllib.parse
import urllib.error
import digitalio
import busio
import board
from adafruit_epd.ssd1675 import Adafruit_SSD1675
from .weather_graphics import Weather_Graphics
from .utils import DATA_SOURCE_URL, get_logger
from .apikey import OPEN_WEATHER_TOKEN

logger = get_logger(__name__)


class Weather:
    def __init__(self, location: str) -> None:
        self.location = location

        if len(OPEN_WEATHER_TOKEN) == 0:
            raise RuntimeError("No OPEN WEATHER API token set")
        else:
            self._open_api_key = OPEN_WEATHER_TOKEN

        self._params = {"q": self.location, "appid": self._open_api_key}
        self._data_source = DATA_SOURCE_URL + "?" + urllib.parse.urlencode(self._params)

    def get_weather_data(self) -> dict:
        try:
            response = urllib.request.urlopen(self._data_source)
            logger.debug(response)
            if response.getcode() == 200:
                value = response.read()
                logger.info(value.decode("utf-8"))
            else:
                raise urllib.error.HTTPError(
                    msg="Did not get a 200, we only consider 200 a success"
                )
        except urllib.error.HTTPError as request_error:
            logger.info(f"Request to get weather failed because {request_error.reason}")
            logger.debug(request_error)
            raise request_error

        return value


class Eink_Weather(Weather):
    def __init__(self, location: str) -> None:
        # Initialize from inherited class
        super().__init__(location=location)
        try:
            # Initializing SPI pins for the E ink display
            self.spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
            self.ecs = digitalio.DigitalInOut(board.CE1)
            self.dc = digitalio.DigitalInOut(board.D23)
            self.rst = digitalio.DigitalInOut(board.D28)
            self.busy = digitalio.DigitalInOut(board.D18)
        except IOError as ioerror:
            logger.exception(ioerror)
            raise ioerror

        # Initialize the display
        self.display = Adafruit_SSD1676(
            123,
            251,
            self.spi,
            cs_pin=self.ecs,
            dc_pin=self.dc,
            sramcs_pin=None,
            rst_pin=self.rst,
            busy_pin=self.busy,
        )

        # Creating an Graphics object that performs our draw function
        self.gfx = Weather_Graphics(self.display, am_pm=True, celsius=True)
        self.weather_refresh = None

    def display(self):
        weather_value = self.get_weather_data()
        self.display.rotation = 1
        logger.debug(weather_value)
        self.gfx.setup_weather_data(weather_value)
        self.weather_refresh = time.monotonic()
        self.gfx.update_time()
