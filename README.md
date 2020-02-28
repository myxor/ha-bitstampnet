# bitstamp.net sensor for Home-Assistant

Home-Assistant sensor for fetching crypto currency data from [bitstamp.net](https://bitstamp.net).

## Get it running 🍕

### Method 1: Using HACS

If you are using the [HACS (Home Assistant Community Store)](https://hacs.xyz/) you can just add the link to this github repo as a new custom repository in the settings menu and install bitstamp.net via the store UI.

### Method 2: Manually

1. checkout this repository
2. copy the content of the  `custom_components/bitstampnet` folder into `config/custom_components/bitstampnet` folder in your home-assistant instance (you may have to create that folder)
3. configure the desired sensors in your `configuration.yaml` file

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

## configuration

* `name`: Some custom name
* `currency`: The crypto currency you want to see the exchange rate from
* `display_currency`: The currency you want to see the exchange in
* `display_currency_decimals`: The number of decimals the rate should be rounded to. Default: 2
* `icon`: Pick an icon from [materialdesignicons.com](https://materialdesignicons.com/). Default: `mdi:currency-btc`

## Supported crypto currencies:

* btc (Bitcoin)
* eth (Ether)
* xrp (Ripple)
* ltc (Litecoin)
* bch (Bitcoin Cash)

## Supported display currencies:

* eur
* usd
