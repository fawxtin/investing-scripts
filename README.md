
# TODO

1) Create a deploy script - Makefile?

2) Fetch current pair price - better for automatization

3) Fetch current alerts, to improve management


# Dependencies & Installation

1) Install gridsite-clients (from your package manager - apt?) - urlencode

2) Copy the investing.com pair indexes ids into your home as ~/.investing_com.indexes

3) Copy the script into whatever path you want, I use it at ~/bin

# Alert Usage

There is basically two modes usage, you can setup a fixed alert or ranged alerts. But first, you
must setup your session token ID from the site. 

## Setup INVESTING_COM_SID env-var

Check your cookies from your browser and search for the `ses_id` from .investing.com. Copy the value
and set to the environment variable INVESTING_COM_SID.

## Fixed alert

Considering the price of gold is ~1950 (which currently is ~1940).

```
investing-alert gold over 2000
investing-alert gold under 1900
```

## Ranged alerts

Setup ranged alerts informing the current price point, the step size and how much alerts do you need between the informed price.

```
# By default it will setup 6 step prices (3 over + 3 under) between the informed price with a given step size in points.
# In this case, for example, I want alert on 1930/1910/1890 and 1970/1990/2010:
investing-alert gold around 1950 20

# If I want alerts only above given price 1950, for example, with a step of 30 points as: 1980/2010/2040/2070/2100. The command would be:
investing-alert gold around 1950 30 5 0

# If I want alerts only under given price 1950, for example, with a step of 10 points as: 1940/1930/1920/1910/1900. The command would be:
investing-alert gold around 1950 10 0 5
```
