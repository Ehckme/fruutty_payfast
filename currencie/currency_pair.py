import requests
from bs4 import BeautifulSoup

"""
##################### SADC AFRCAN COUNTRIES PAIR ###################
"""

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
URL = 'https://www.tradingview.com/markets/currencies/rates-africa/'
r = requests.get(url=URL, headers=headers)
soup = BeautifulSoup(r.content, 'html5lib')

"""
#########################  MAJOR TRADES PAIRS #####################
"""
URL_MAJOR = 'https://www.tradingview.com/markets/currencies/rates-major/'
req = requests.get(url=URL_MAJOR, headers=headers)
major_soup = BeautifulSoup(req.content, 'html5lib')

"""
#############################  ExOTIC TRADES PAIRS ######################
"""

URL_EXOTIC = 'https://www.tradingview.com/markets/currencies/rates-exotic/'
reqs = requests.get(url=URL_EXOTIC, headers=headers)
exotic_soup = BeautifulSoup(reqs.content, 'html5lib')

"""
###########################  SPECIAL KUWAITI DINAR TRADES ################
"""

URL_EXOTIC = 'https://www.tradingview.com/markets/currencies/rates-middle-east/'
request = requests.get(url=URL_EXOTIC, headers=headers)
kuwaiti_soup = BeautifulSoup(request.content, 'html5lib')

"""
###########################  SPECIAL KUWAITI DINAR TRADES ################
"""

URL_ASIA = 'https://www.tradingview.com/markets/currencies/rates-asia/'
request = requests.get(url=URL_ASIA, headers=headers)
asia_soup = BeautifulSoup(request.content, 'html5lib')

class Currency_Pairs:
    """
    FTVS (Fruutty Token Value System) Currency Pairs.

    Basic Usage:

    from currencu_pairs import Currency_Pairs

    currency_pairs = Currency_Pairs()
    xyz_currency = currency_pairs.xyz_currency()
    """
    # USD to ZAR


    def __init__(self):

        pass

    def usd_zar(self):
        """ ######### USD - ZAR CURRENCY PAIR CONVERSION SECTION ###############"""
        self.us_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDZAR'})
        self.us_zar_td = self.us_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.us_zar_linktag = self.us_zar_tr.find('a', attrs={'title': 'USDZAR − U.S. DOLLAR / SOUTH AFRICAN RAND'})
        self.us_zar_linktagText = self.us_zar_linktag.get_text()
        self.us_zar_text = self.us_zar_td.get_text()
        self.USD_ZAR = float(self.us_zar_text)

        return self.USD_ZAR

    def aoa_zar(self):
        """ ######### ANGOLA ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 angolan value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                aoa_zar = currency_pair.bwp_zar()
                trade_value = 1 / aoa_zar
        """
        self.angola_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDAOA'})
        self.angola_zar_td = self.angola_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.angola_zar_linktag = self.angola_zar_tr.find('a', attrs={'title': 'USDAOA − U.S. DOLLAR / ANGOLAN KWANZA'})
        self.angola_zar_linktagText = self.angola_zar_linktag.get_text()
        self.angola_zar_text = self.angola_zar_td.get_text()
        self.angola_zar_tradeValue = float(self.angola_zar_text) / float(self.us_zar_text)

        OAOZAR = 'OAOZAR'

        return self.angola_zar_tradeValue

    def bwp_zar(self):
        """ ######### BOTSWANA - ZAR CURRENCY PAIR CONVERSION SECTION ###############
            Here we divide 1 botswana value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                bwp_zar = currency_pair.bwp_zar()
                trade_value = 1 / bwp_zar
        """
        self.botswana_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDBWP'})
        self.botswana_zar_td = self.botswana_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.botswana_zar_linktag = self.botswana_zar_tr.find('a', attrs={'title': 'USDBWP − U.S. DOLLAR / BOTSWANAN PULA'})
        self.botswana_zar_linktagText = self.botswana_zar_linktag.get_text()
        self.botswana_zar_text = self.botswana_zar_td.get_text()
        self.botswana_zar_tradeValue = float(self.botswana_zar_text) / float(self.us_zar_text)

        BWPZAR = 'BWPZAR'

        return self.botswana_zar_tradeValue

    def cdf_zar(self):
        """ ######### CONGO ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                cdf_zar = currency_pair.bwp_zar()
                trade_value = 1 / cdf_zar
        """
        self.congo_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDCDF'})
        self.congo_zar_td = self.congo_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.congo_zar_linktag = self.congo_zar_tr.find('a', attrs={'title': 'USDCDF − U.S. DOLLAR / CONGOLESE FRANC'})
        self.congo_zar_linktagText = self.congo_zar_linktag.get_text()
        self.congo_zar_text = self.congo_zar_td.get_text()
        self.value = self.congo_zar_text.replace(',', '')

        self.congo_zar_tradeValue = float(self.value) / float(self.us_zar_text)

        CDFZAR = 'CDFZAR'

        return self.congo_zar_tradeValue

    def etb_zar(self):
        """ ######### ETHOPIAN - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                etb_zar = currency_pair.etb_zar()
                trade_value = 1 / etb_zar
        """
        self.ethopia_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDETB'})
        self.ethopia_zar_td = self.ethopia_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.ethopia_zar_linktag = self.ethopia_zar_tr.find('a', attrs={'title': 'USDETB − U.S. DOLLAR / ETHIOPIAN BIRR'})
        self.ethopia_zar_linktagText = self.ethopia_zar_linktag.get_text()
        self.ethopia_zar_text = self.ethopia_zar_td.get_text()
        self.ethopia_zar_tradeValue = float(self.ethopia_zar_text) / float(self.us_zar_text)

        ETBZAR = 'ETBZAR'

        return self.ethopia_zar_tradeValue

    def ghs_zar(self):
        """ ######### Namibia ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                ghs_zar = currency_pair.ghs_zar()
                trade_value = 1 / ghs_zar
        """
        self.ghana_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDGHS'})
        self.ghana_zar_td = self.ghana_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.ghana_zar_linktag = self.ghana_zar_tr.find('a', attrs={'title': 'USDGHS − U.S. DOLLAR / GHANAIAN CEDI'})
        self.ghana_zar_linktagText = self.ghana_zar_linktag.get_text()
        self.ghana_zar_text = self.ghana_zar_td.get_text()
        self.ghana_zar_tradeValue = float(self.ghana_zar_text) / float(self.us_zar_text)

        GHSZAR = 'GHSZAR'

        return self.ghana_zar_tradeValue

    def lsl_zar(self):
        """ ######### LESOTHO ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                lsl_zar = currency_pair.lsl_zar()
                trade_value = 1 / lsl_zar

        """
        self.lesotho_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDLSL'})
        self.lesotho_zar_td = self.lesotho_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.lesotho_zar_linktag = self.lesotho_zar_tr.find('a', attrs={'title': 'USDLSL − U.S. DOLLAR / BASOTHO LOTI'})
        self.lesotho_zar_linktagText = self.lesotho_zar_linktag.get_text()
        self.lesotho_zar_text = self.lesotho_zar_td.get_text()
        self.lesotho_zar_tradeValue = float(self.lesotho_zar_text) / float(self.us_zar_text)

        LSLZAR = 'LSLZAR'

        return self.lesotho_zar_tradeValue

    def mwk_zar(self):
        """ ######### MALAWIAN - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                mwk_zar = currency_pair.mwk_zar()
                trade_value = 1 / mwk_zar
        """
        self.malawi_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:ZARMWK'})
        self.malawi_zar_td = self.malawi_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})

        self.malawi_zar_linktag = self.malawi_zar_tr.find('a', attrs={'title': 'ZARMWK − SOUTH AFRICAN RAND / MALAWIAN KWACHA'})
        self.malawi_zar_linktagText = self.malawi_zar_linktag.get_text()
        self.malawi_zar_text = self.malawi_zar_td.get_text()
        self.value = self.malawi_zar_text.replace(',', '')


        self.malawi_zar_tradeValue = float(self.value)

        MWKZAR = 'MWKZAR'

        return self.malawi_zar_tradeValue

    def mzn_zar(self):
        """ ######### MOZAMBIQUE - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                mzn_zar = currency_pair.mzn_zar()
                trade_value = 1 / mzn_zar
        """
        self.mozambic_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDMZN'})
        self.mozambic_zar_td = self.mozambic_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.mozambic_zar_linktag = self.mozambic_zar_tr.find('a', attrs={'title': 'USDMZN − U.S. DOLLAR / MOZAMBICAN METICAL'})
        self.mozambic_zar_linktagText = self.mozambic_zar_linktag.get_text()
        self.mozambic_zar_text = self.mozambic_zar_td.get_text()
        self.mozambic_zar_tradeValue = float(self.mozambic_zar_text) / float(self.us_zar_text)

        MZNZAR = 'MZNZAR'

        return self.mozambic_zar_tradeValue

    def nad_zar(self):
        """ ######### Namibia ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                nad_zar = currency_pair.nad_zar()
                trade_value = 1 / nad_zar
        """
        self.namibia_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDNAD'})
        self.namibia_zar_td = self.namibia_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.namibia_zar_linktag = self.namibia_zar_tr.find('a', attrs={'title': 'USDNAD − U.S. DOLLAR / NAMIBIAN DOLLAR'})
        self.namibia_zar_linktagText = self.namibia_zar_linktag.get_text()
        self.namibia_zar_text = self.namibia_zar_td.get_text()
        self.namibia_zar_tradeValue = float(self.namibia_zar_text) / float(self.us_zar_text)

        NADZAR = 'NADZAR'

        return self.namibia_zar_tradeValue

    def ngn_zar(self):
        """ ######### NGN Nigeria ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                ngn_zar = currency_pair.ngn_zar()
                trade_value = 1 / ngn_zar

        """
        self.nigeria_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDNGN'})
        self.nigeria_zar_td = self.nigeria_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.nigeria_zar_linktag = self.nigeria_zar_tr.find('a', attrs={'title': 'USDNGN − U.S. DOLLAR / NIGERIA NAIRA'})
        self.nigeria_zar_linktagText = self.nigeria_zar_linktag.get_text()
        self.nigeria_zar_text = self.nigeria_zar_td.get_text()
        self.value = self.nigeria_zar_text.replace(',', '')

        self.nigeria_zar_tradeValue = float(self.value) / float(self.us_zar_text)

        NGNZAR = 'NGNZAR'

        return self.nigeria_zar_tradeValue

    def kes_zar(self):
        """ ######### KENYA ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                kes_zar = currency_pair.kes_zar()
                trade_value = 1 / kes_zar
        """
        self.kenya_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDKES'})
        self.kenya_zar_td = self.kenya_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.kenya_zar_linktag = self.kenya_zar_tr.find('a', attrs={'title': 'USDKES − U.S. DOLLAR / KENYAN SHILLING'})
        self.kenya_zar_linktagText = self.kenya_zar_linktag.get_text()
        self.kenya_zar_text = self.kenya_zar_td.get_text()
        self.kenya_zar_tradeValue = float(self.kenya_zar_text) / float(self.us_zar_text)

        KESZAR = 'KESZAR'

        return self.kenya_zar_tradeValue

    def sos_zar(self):
        """ ######### SOMALIA ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                sos_zar = currency_pair.sos_zar()
                trade_value = 1 / sos_zar
        """
        self.somalia_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDSOS'})
        self.somalia_zar_td = self.somalia_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.somalia_zar_linktag = self.somalia_zar_tr.find('a', attrs={'title': 'USDSOS − U.S. DOLLAR / SOMALI SHILLING'})
        self.somalia_zar_linktagText = self.somalia_zar_linktag.get_text()
        self.somalia_zar_text = self.somalia_zar_td.get_text()
        self.somalia_zar_tradeValue = float(self.somalia_zar_text) / float(self.us_zar_text)

        SOSZAR = 'SOSZAR'

        return self.somalia_zar_tradeValue

    def szl_zar(self):
        """ ######### SWAZILAND ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                szl_zar = currency_pair.szl_zar()
                trade_value = 1 / szl_zar
        """
        self.swaziland_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDSZL'})
        self.swaziland_zar_td = self.swaziland_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.swaziland_zar_linktag = self.swaziland_zar_tr.find('a', attrs={'title': 'USDSZL − U.S. DOLLAR / SWAZI LILANGENI'})
        self.swaziland_zar_linktagText = self.swaziland_zar_linktag.get_text()
        self.swaziland_zar_text = self.swaziland_zar_td.get_text()
        self.swaziland_zar_tradeValue = float(self.swaziland_zar_text) / float(self.us_zar_text)

        SZLZAR = 'SZLZAR'

        return self.swaziland_zar_tradeValue

    def tzs_zar(self):
        """ ######### TANZANIA ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                tzs_zar = currency_pair.tzs_zar()
                trade_value = 1 / tzs_zar
        """
        self.tanzania_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDTZS'})
        self.tanzania_zar_td = self.tanzania_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.tanzania_zar_linktag = self.tanzania_zar_tr.find('a', attrs={'title': 'USDTZS − U.S. DOLLAR / TANZANIAN SHILLING'})
        self.tanzania_zar_linktagText = self.tanzania_zar_linktag.get_text()
        self.tanzania_zar_text = self.tanzania_zar_td.get_text()
        self.value = self.tanzania_zar_text.replace(',', '')

        self.tanzania_zar_tradeValue = float(self.value) / float(self.us_zar_text)

        TZSZAR = 'TZSZAR'

        return self.tanzania_zar_tradeValue

    def ugx_zar(self):
        """ ######### UGANDA ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
            Usage:
            e.g currency_pair = Currency_Pairs()
                ugx_zar = currency_pair.ugx_zar()
                trade_value = 1 / ugx_zar
        """
        self.uganda_zar_tr = soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDUGX'})
        self.uganda_zar_td = self.uganda_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.uganda_zar_linktag = self.uganda_zar_tr.find('a', attrs={'title': 'USDUGX − U.S. DOLLAR / UGANDAN SHILLING'})
        self.uganda_zar_linktagText = self.uganda_zar_linktag.get_text()
        self.uganda_zar_text = self.uganda_zar_td.get_text()
        self.value = self.uganda_zar_text.replace(',', '')

        self.uganda_zar_tradeValue = float(self.value) / float(self.us_zar_text)

        UGXZAR = 'UGXZAR'

        return self.uganda_zar_tradeValue
        """
        ####################################  MAJOR TRADES #################################################
        """

    def eur_zar(self):
        """ ######### Euro - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            eur_zar = currency_pair.eur_zar()
            trade_value = 1 / eur_zar
        """
        self.euro_zar_tr = major_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:EURUSD'})
        self.euro_zar_td = self.euro_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.euro_zar_linktag = self.euro_zar_tr.find('a', attrs={'title': 'EURUSD − EURO / U.S. DOLLAR'})
        self.euro_zar_linktagText = self.euro_zar_linktag.get_text()
        self.euro_zar_text = self.euro_zar_td.get_text()
        self.euro_zar_tradeValue = float(self.euro_zar_text) * float(self.us_zar_text)

        EURZAR = 'EURZAR'

        return self.euro_zar_tradeValue

    def jpy_zar(self):
        """ ######### JAPANESE - ZAR CURRENCY PAIR SECTION ###############
         Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            jpy_zar = currency_pair.jpy_zar()
            trade_value = 1 / jpy_zar
        """
        self.japan_zar_tr = major_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDJPY'})
        self.japan_zar_td = self.japan_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.japan_zar_linktag = self.japan_zar_tr.find('a', attrs={'title': 'USDJPY − U.S. DOLLAR / JAPANESE YEN'})
        self.japan_zar_linktagText = self.japan_zar_linktag.get_text()
        self.japan_zar_text = self.japan_zar_td.get_text()
        self.japan_zar_tradeValue = float(self.japan_zar_text) / float(self.us_zar_text)

        JPYZAR = 'JPYZAR'

        return self.japan_zar_tradeValue

    def gbp_zar(self):
        """ ######### BRITISH - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            gbp_zar = currency_pair.gbp_zar()
            trade_value = 1 / gbp_zar
        """
        self.british_pound_zar_tr = major_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:GBPUSD'})
        self.british_pound_zar_td = self.british_pound_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.british_pound_zar_linktag = self.british_pound_zar_tr.find('a', attrs={'title': 'GBPUSD − BRITISH POUND / U.S. DOLLAR'})
        self.british_pound_zar_linktagText = self.british_pound_zar_linktag.get_text()
        self.british_pound_zar_text = self.british_pound_zar_td.get_text()
        self.british_pound_zar_tradeValue = 1 / (float(self.british_pound_zar_text) * float(self.us_zar_text))

        GBPZAR = 'GBPZAR'

        return self.british_pound_zar_tradeValue

    def aud_zar(self):
        """ ######### AUSTRALIAN - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            aud_zar = currency_pair.aud_zar()
            trade_value = 1 / aud_zar
        """
        self.australia_zar_tr = major_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:AUDUSD'})
        self.australia_zar_td = self.australia_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.australia_zar_linktag = self.australia_zar_tr.find('a', attrs={'title': 'AUDUSD − AUSTRALIAN DOLLAR / U.S. DOLLAR'})
        self.australia_zar_linktagText = self.australia_zar_linktag.get_text()
        self.australia_zar_text = self.australia_zar_td.get_text()
        self.australia_zar_tradeValue = 1 / (float(self.australia_zar_text) * float(self.us_zar_text))
        AUDZAR = 'AUDZAR'

        return self.australia_zar_tradeValue

    def cad_zar(self):
        """ ######### CANADIAN - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            cad_zar = currency_pair.cad_zar()
            trade_value = 1 / cad_zar
        """
        self.canada_zar_tr = major_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDCAD'})
        self.canada_zar_td = self.canada_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.canada_zar_linktag = self.canada_zar_tr.find('a', attrs={'href': '/symbols/USDCAD/?exchange=FX_IDC'})
        self.canada_zar_linktagText = self.canada_zar_linktag.get_text()
        self.canada_zar_text = self.canada_zar_td.get_text()
        self.canada_zar_tradeValue = float(self.canada_zar_text) / float(self.us_zar_text)

        CADZAR = 'CADZAR'

        return self.canada_zar_tradeValue

    def chf_zar(self):
        """ ######### SWISS - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            chf_zar = currency_pair.chf_zar()
            trade_value = 1 / chf_zar
        """
        self.swiss_zar_tr = major_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDCHF'})
        self.swiss_zar_td = self.swiss_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.swiss_zar_linktag = self.swiss_zar_tr.find('a', attrs={'href': '/symbols/USDCHF/?exchange=FX_IDC'})
        self.swiss_zar_linktagText = self.swiss_zar_linktag.get_text()
        self.swiss_zar_text = self.swiss_zar_td.get_text()
        self.swiss_zar_tradeValue = float(self.swiss_zar_text) / float(self.us_zar_text)

        CHFZAR = 'CHFZAR'

        return self.swiss_zar_tradeValue

    """
    ####################################  ExOTIC TRADES #################################################
    """

    def rub_zar(self):
        """ ######### Russia - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            rub_zar = currency_pair.rub_zar()
            trade_value = 1 / rub_zar
        """
        self.russia_zar_tr = exotic_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDRUB'})
        self.russia_zar_td = self.russia_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.russia_zar_linktag = self.russia_zar_tr.find('a', attrs={'title': 'USDRUB − U.S. DOLLAR / RUSSIAN RUBLE'})
        self.russia_zar_linktagText = self.russia_zar_linktag.get_text()
        self.russia_zar_text = self.russia_zar_td.get_text()
        self.russia_zar_tradeValue = float(self.russia_zar_text) / float(self.us_zar_text)

        RUBZAR = 'RUBZAR'

        return self.russia_zar_tradeValue

    def inr_zar(self):
        """ ######### SWISS - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            inr_zar = currency_pair.inr_zar()
            trade_value = 1 / inr_zar
        """
        self.india_zar_tr = exotic_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDINR'})
        self.india_zar_td = self.india_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.india_zar_linktag = self.india_zar_tr.find('a', attrs={'title': 'USDINR − U.S. DOLLAR / INDIAN RUPEE'})
        self.india_zar_linktagText = self.india_zar_linktag.get_text()
        self.india_zar_text = self.india_zar_td.get_text()
        self.india_zar_tradeValue = float(self.india_zar_text) / float(self.us_zar_text)

        INRZAR = 'INRZAR'

        return self.india_zar_tradeValue

    def brl_zar(self):
        """ ######### SWISS - ZAR CURRENCY PAIR SECTION ###############
        Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            brl_zar = currency_pair.brl_zar()
            trade_value = 1 / brl_zar
        """
        self.brazil_zar_tr = exotic_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDBRL'})
        self.brazil_zar_td = self.brazil_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.brazil_zar_linktag = self.brazil_zar_tr.find('a', attrs={'title': 'USDBRL − U.S. DOLLAR / BRAZILIAN REAL'})
        self.brazil_zar_linktagText = self.brazil_zar_linktag.get_text()
        self.brazil_zar_text = self.brazil_zar_td.get_text()
        self.brazil_zar_tradeValue = float(self.brazil_zar_text) / float(self.us_zar_text)

        BRLZAR = 'BRLZAR'

        return self.brazil_zar_tradeValue

    """
    ####################################  SPECIAL KUWAITI DINAR TRADES #################################################
    """
    def kwd_zar(self):

        """ ######### USD - KUWAITI DINAR - ZAR CURRENCY PAIR SECTION ###############
         Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            kwd_zar = currency_pair.kwd_zar()
            trade_value = 1 / kwd_zar
        """
        self.kuwaiti_zar_tr = kuwaiti_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDKWD'})
        self.kuwaiti_zar_td = self.kuwaiti_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.kuwaiti_zar_linktag = self.kuwaiti_zar_tr.find('a', attrs={'title': 'USDKWD − U.S. DOLLAR / KUWAITI DINAR'})
        self.kuwaiti_zar_linktagText = self.kuwaiti_zar_linktag.get_text()
        self.kuwaiti_zar_text = self.kuwaiti_zar_td.get_text()
        self.kuwaiti_zar_tradeValue = float(self.kuwaiti_zar_text) / float(self.us_zar_text)

        KWDZAR = 'KWDZAR'

        return self.kuwaiti_zar_tradeValue

    def cny_zar(self):

        """ ######### USD - CHINESE YUAN - ZAR CURRENCY PAIR SECTION ###############
         Here we divide 1 congo value to get actual equivalent rand trade value.
        Usage:
        e.g currency_pair = Currency_Pairs()
            kwd_zar = currency_pair.kwd_zar()
            trade_value = 1 / kwd_zar
        """
        self.cny_zar_tr = asia_soup.find('tr', attrs={'data-rowkey': 'FX_IDC:USDCNY'})
        self.cny_zar_td = self.cny_zar_tr.find('td', attrs={'class': 'cell-RLhfr_y4 right-RLhfr_y4'})
        self.cny_zar_linktag = self.cny_zar_tr.find('a', attrs={'title': 'USDCNY − U.S. DOLLAR / CHINESE YUAN'})
        self.cny_zar_linktagText = self.cny_zar_linktag.get_text()
        self.cny_zar_text = self.cny_zar_td.get_text()
        self.cny_zar_tradeValue = (float(self.cny_zar_text) / float(self.us_zar_text))

        CNYZAR = 'CNYZAR'

        return self.cny_zar_tradeValue

"""
currency_pair = Currency_Pairs()
usd_zar = currency_pair.usd_zar()
bwp_zar = currency_pair.bwp_zar()
aoa_zar = currency_pair.aoa_zar()
cdf_zar = currency_pair.cdf_zar()
etb_zar = currency_pair.etb_zar()
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

# ######### ASIA / CHINESE YUAN #############
cny_zar = currency_pair.cny_zar()

print('USD TO ZAR : ', usd_zar)
print('BOTSWANA TO ZAR : ', bwp_zar)
print('ANGOLA TO ZAR : ', aoa_zar)
print('CONGO TO ZAR : ', cdf_zar)
print('ETHOPIA TO ZAR : ', etb_zar)
print('LESOTHO TO ZAR : ', lsl_zar)
print('MALAWI TO ZAR : ', mwk_zar)
print('MOZAMBIQUE TO ZAR : ', mzn_zar)
print('NAMIBIA TO ZAR : ', nad_zar)
print('NIGERIA TO ZAR : ', ngn_zar)
print('GHANA TO ZAR : ', ghs_zar)
print('KENYA TO ZAR : ', kes_zar)
print('SOMALIA TO ZAR : ', sos_zar)
print('SWAZILAND TO ZAR : ', szl_zar)
print('TANZANIA TO ZAR : ', tzs_zar)
print('UGANDA TO ZAR : ', ugx_zar)
# ######### majors #############

print('EURO TO ZAR : ', eur_zar)
print('JAPAN TO ZAR : ', jpy_zar)
print('BRITISH POUND TO ZAR : ', gbp_zar)
print('AUSTRALIA TO ZAR : ', aud_zar)
print('CANADA TO ZAR', cad_zar)
print('SWISS TO ZAR', chf_zar)
# ######### EXOTIC #############

print('RUSSIA TO ZAR', rub_zar)
print('INDIA TO ZAR', inr_zar)
print('BRAZIL TO ZAR', brl_zar)

# ######### KUWAITI DINAR #############
print('KUWAITI DINAR TO ZAR', kwd_zar)

# ######### ASIA / CHINESE YUAN #############
print('CHINESE YUAN TO ZAR', cny_zar)
"""



if __name__ == '__main__':
    # Currency_Pairs()
    pass
