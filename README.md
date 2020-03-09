# bitstamp.net sensor for Home-Assistant

Home-Assistant sensor for fetching crypto currency data from [bitstamp.net](https://bitstamp.net).

## Get it installed 🍕

1. Install Python dependency `BitstampClient` (if not already installed). 
You can do this by running `pip install BitstampClient==2.2.8` or `docker exec homeassistant pip install BitstampClient==2.2.8` depending wether you are running home-assistant in docker or not.

### Method 1: Using HACS

If you are using the [HACS (Home Assistant Community Store)](https://hacs.xyz/):

1. Add the link to this github repo as a new custom repository in the settings menu 
2. Install bitstamp.net integration via the store UI

### Method 2: Manually

1. checkout this repository
2. copy the content of the  `custom_components/bitstampnet` folder into `config/custom_components/bitstampnet` folder in your home-assistant instance (you may have to create that folder)
3. configure the desired sensors in your `configuration.yaml` file

## Get it running inside home-assistant

### Example configuration entries:

```yaml
sensor:
  - platform: bitstampnet
    name: "EUR/BTC"
    currency: "btc"
    display_currency: "EUR"
    icon: "mdi:currency-btc"

  - platform: bitstampnet
    name: "EUR/ETH"
    currency: "eth"
    icon: "mdi:currency-eth"

  - platform: bitstampnet
    name: "EUR/LTC"
    currency: "ltc"

  - platform: bitstampnet
    name: "EUR/XRP"
    currency: "xrp"
```

### Configuration options

* `name`: Some custom name
* `currency`: The crypto currency you want to see the exchange rate from
* `display_currency`: The currency you want to see the exchange in
* `display_currency_decimals`: The number of decimals the rate should be rounded to. Default: 2
* `icon`: Pick an icon from [materialdesignicons.com](https://materialdesignicons.com/). Default: `mdi:currency-btc`

### Supported crypto currencies:

* btc (Bitcoin)
* eth (Ether)
* xrp (Ripple)
* ltc (Litecoin)
* bch (Bitcoin Cash)

## Supported display currencies:

* eur
* usd

# Screenshot

![Sensor](https://raw.githubusercontent.com/myxor/ha-bitstampnet/master/screenshots/sensor.png)
