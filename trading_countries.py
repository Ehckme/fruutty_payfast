# import pandas
import datetime
from sqlalchemy import DateTime
from sqlalchemy.sql import func
# importing geopy library & requests
from geopy.geocoders import Nominatim
from requests import get
import json

import pandas
from currencie.currency_pair import Currency_Pairs
from flask import request





# trading_countries.py
import pandas as pd


currency_pair = Currency_Pairs()

# Predefined exchange rates
countries = {
    'South Africa': currency_pair.usd_zar(),
    'Angola': currency_pair.aoa_zar(),
    'Botswana': currency_pair.bwp_zar(),
    'République démocratique du Congo': currency_pair.cdf_zar(),
    'Ghana': currency_pair.ghs_zar(),
    'Lesotho': currency_pair.lsl_zar(),
    'Malawi': currency_pair.mwk_zar(),
    'Moçambique': currency_pair.mzn_zar(),
    'Namibia': currency_pair.nad_zar(),
    'Nigeria': currency_pair.ngn_zar(),
    'Kenya': currency_pair.kes_zar(),
    'Soomaaliya الصومال': currency_pair.sos_zar(),
    'eSwatini': currency_pair.szl_zar(),
    'Uganda': currency_pair.ugx_zar(),
    '日本': currency_pair.jpy_zar(),
    'United Kingdom': currency_pair.gbp_zar(),
    'Australia': currency_pair.aud_zar(),
    'Canada': currency_pair.cad_zar(),
    'Schweiz/Suisse/Svizzera/Svizra': currency_pair.chf_zar(),
    'Россия': currency_pair.rub_zar(),
    'India': currency_pair.inr_zar(),
    'Brasil': currency_pair.brl_zar(),
    'الكويت': currency_pair.kwd_zar(),
}

def get_user_country():
    """Fetch user country code safely from ipinfo.io"""
    try:
        url = "http://ipinfo.io/json"
        response = get(url, timeout=5)
        data = response.json()
        return data.get("country")  # safe get()
    except Exception as e:
        return None

def resolve_location(country_code: str | None):
    """Use Nominatim to resolve a human-readable location"""
    if not country_code:
        return None
    try:
        loc = Nominatim(user_agent="GetLoc")
        return loc.geocode(country_code)
    except Exception:
        return None

def term1():
    """Build a pandas DataFrame with location + exchange rate"""
    country_code = get_user_country()
    loc = resolve_location(country_code)
    return pd.DataFrame(
        {
            "Country": loc.address if loc else "Unknown",
            "Symbol": country_code if country_code else "N/A",
            "Value": countries.get("République démocratique du Congo"),  # example value
        },
        index=[1],
    )

if __name__ == "__main__":
    df = term1()
    print(df)
    df.to_excel("currency_pair.xlsx", sheet_name="Sheet", index=False)


"""
currency_pair = Currency_Pairs()
usd_zar = currency_pair.usd_zar()
bwp_zar = currency_pair.bwp_zar()
aoa_zar = currency_pair.aoa_zar()
cdf_zar = currency_pair.cdf_zar()
# etb_zar = currency_pair.etb_zar()
lsl_zar = currency_pair.lsl_zar()
mwk_zar = currency_pair.mwk_zar()
mzn_zar = currency_pair.mzn_zar()
nad_zar = currency_pair.nad_zar()
ngn_zar = currency_pair.ngn_zar()
ghs_zar = currency_pair.ghs_zar()
kes_zar = currency_pair.kes_zar()
sos_zar = currency_pair.sos_zar()
szl_zar = currency_pair.szl_zar()
tzs_zar = currency_pair.tzs_zar()
ugx_zar = currency_pair.ugx_zar()

# ############## majors ############
eur_zar = currency_pair.eur_zar()
jpy_zar = currency_pair.jpy_zar()
gbp_zar = currency_pair.gbp_zar()
aud_zar = currency_pair.aud_zar()
cad_zar = currency_pair.cad_zar()
chf_zar = currency_pair.chf_zar()

# ############## exotic ############
rub_zar = currency_pair.rub_zar()
inr_zar = currency_pair.inr_zar()
brl_zar = currency_pair.brl_zar()

# ######### KUWAITI DINAR #############
kwd_zar = currency_pair.kwd_zar()

countries = {
    'South Africa': usd_zar, 'Angola': aoa_zar,
    'Botswana': bwp_zar, 'République démocratique du Congo': cdf_zar,
     'Ghana': ghs_zar,
    'Lesotho': lsl_zar, 'Malawi': mwk_zar,
    'Moçambique': mzn_zar, 'Namibia': nad_zar,

    'Nigeria': ngn_zar, 'Kenya': kes_zar,
    'Soomaaliya الصومال': sos_zar, 'eSwatini': szl_zar,
    'Uganda': ugx_zar, '日本': jpy_zar,
    'United Kingdom': gbp_zar, 'Australia': aud_zar,
    'Canada': cad_zar, 'Schweiz/Suisse/Svizzera/Svizra': chf_zar,

    'Россия': rub_zar, 'India': inr_zar,
    'Brasil': brl_zar, 'الكويت': kwd_zar,

}


# get user location from url requests library
url = 'http://ipinfo.io/json'
response = get(url)
data = json.loads(response.text)
country = data['country']

# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")

# get the location name
getLoc = loc.geocode(f"{country}")


# create pandas data set function term1() using pandas
def term1():
    term1_dataset = {
        'Country': getLoc.address,
        'Symbol': country,
        'Value': cdf_zar,
    }
    # create dataframe variable
    term1_dataframe = pandas.DataFrame(term1_dataset, index=[1])
    return term1_dataframe


if __name__ == "__main__":
    # Call request name function

    # Call and ssend term1 function to excell
    # term1()

    # send term1() function data to Excel spreadsheet
    term1().to_excel("currency_pair.xlsx", sheet_name="Sheet", index=False)

    # print term1() data
    print(term1())
"""
