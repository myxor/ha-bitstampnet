"""Details about crypto currencies from bitstamp.net.
This sensor is based on the existing CoinMarketCap sensor inside home-assistant"""
from datetime import timedelta
import logging
from urllib.error import HTTPError

from bitstamp import client
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import ATTR_ATTRIBUTION, CONF_DISPLAY_CURRENCY
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

ATTR_VOLUME_24H = "volume_24h"
ATTR_HIGH = "high_24h"
ATTR_LOW = "low_24h"
ATTR_VWAP = "volume_weighted_avg_price_24h"

ATTRIBUTION = "Data provided by bitstamp.net"

CONF_CURRENCY = "currency"
CONF_DISPLAY_CURRENCY_DECIMALS = "display_currency_decimals"
CONF_NAME = "name"
CONF_ICON = "icon"

DEFAULT_CURRENCY = "btc"
DEFAULT_DISPLAY_CURRENCY = "EUR"
DEFAULT_DISPLAY_CURRENCY_DECIMALS = 2
DEFAULT_NAME = "btc/EUR"
DEFAULT_ICON = "mdi:currency-btc"

SCAN_INTERVAL = timedelta(minutes=15)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_CURRENCY, default=DEFAULT_CURRENCY): cv.string,
        vol.Optional(
            CONF_DISPLAY_CURRENCY, default=DEFAULT_DISPLAY_CURRENCY
        ): cv.string,
        vol.Optional(
            CONF_NAME, default=DEFAULT_NAME
        ): cv.string,
        vol.Optional(
            CONF_ICON, default=DEFAULT_ICON
        ): cv.string,
        vol.Optional(
            CONF_DISPLAY_CURRENCY_DECIMALS, default=DEFAULT_DISPLAY_CURRENCY_DECIMALS
        ): vol.All(vol.Coerce(int), vol.Range(min=1)),
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the BitStampNetData sensor."""
    currency = config.get(CONF_CURRENCY)
    display_currency = config.get(CONF_DISPLAY_CURRENCY).upper()
    display_currency_decimals = config.get(CONF_DISPLAY_CURRENCY_DECIMALS)
    name = config.get(CONF_NAME)
    icon = config.get(CONF_ICON)

    try:
        BitStampNetData(currency, display_currency).update()
    except HTTPError:
        _LOGGER.warning(
            "Currency %s or display currency %s "
            "is not available. Using btc "
            "and EUR.",
            currency,
            display_currency,
        )
        currency = DEFAULT_CURRENCY
        display_currency = DEFAULT_DISPLAY_CURRENCY
        icon = DEFAULT_ICON

    add_entities(
        [
            BitStampNetSensor(
                BitStampNetData(currency, display_currency),
                name,
                currency,
                display_currency,
                display_currency_decimals,
                icon
            )
        ],
        True,
    )


class BitStampNetSensor(Entity):
    """Representation of a BitStampNet sensor."""

    def __init__(self, ticker, name, currency, display_currency, display_currency_decimals, icon):
        """Initialize the sensor."""
        self.ticker = ticker
        self.currency = currency
        self.display_currency = display_currency
        self.display_currency_decimals = display_currency_decimals
        self._name = name
        self._icon = icon
        self._values = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.ticker.values is not None:
            return round(
                float(
                    self.ticker.values.get("last")
                ),
                self.display_currency_decimals,
            )
        else:
            _LOGGER.warning("sensor state was requested but values is not set yet")

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self.display_currency

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._icon

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        if self.ticker is not None:
            return {
                ATTR_VOLUME_24H: self.ticker.values.get("volume"),
                ATTR_ATTRIBUTION: ATTRIBUTION,
                ATTR_HIGH: self.ticker.values.get("high"),
                ATTR_LOW: self.ticker.values.get("low"),
                ATTR_VWAP: self.ticker.values.get("vwap")
            }

    def update(self):
        """Get the latest data and updates the states."""
        self.ticker.update()
        self._values = self.ticker.values

    @name.setter
    def name(self, value):
        self._name = value


class BitStampNetData:
    """Get the latest data and update the states."""

    def __init__(self, currency, display_currency):
        """Initialize the data object."""
        self.currency = currency
        self.display_currency = display_currency
        self.values = None

    def update(self):
        """Get the latest data from bitstamp.net."""
        public_client = client.Public()
        try:
            self.values = public_client.ticker(base=self.currency, quote=self.display_currency)
        except Exception as e:
            _LOGGER.error(e)
