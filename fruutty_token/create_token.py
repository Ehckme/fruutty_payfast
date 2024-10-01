import qrcode
import json
import datetime

import random
import string



class Token:
        def __init__(self):
                return

        def fruuty_token(self,
                         amount,
                         name: str = None,
                         token_id: str = None,
                         user_id: str = None,
                         token_type: str = None,
                         product_name: str = None,
                         store_name: str = None,
                         city: str = None,
                         user_country: str = None,
                         trade_country: str = None,
                         ):
                self.name = name
                self.amount = amount
                self.token_id = token_id
                self.user_id = user_id
                self.token_type = token_type
                self.product_name = product_name
                self.store_name = store_name
                self.city = city
                self.user_country = user_country
                self.trade_country = trade_country

                fruuty_qr_token = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=100,
                    border=1,
                )
                self.data = {'token_id': f'{self.token_id}',
                             'user_id': f'{self.user_id}',
                             'token_type': f'{self.token_type}',
                             'product_name': f'{self.product_name}',
                             'store_name': f'{self.store_name}',
                             'city': f'{self.city}',
                             'user_country': f'{self.user_country}',
                             'trade_country': f'{self.trade_country}',
                             'token_amount': f'{self.amount}',
                             'date': f'{datetime.datetime.today()}',
                             'processor': 'fruutty',
                             }

                self.jsonify_data = json.dumps(self.data)
                fruuty_qr_token.add_data(self.jsonify_data)
                fruuty_qr_token.make(fit=True)
                fruuty_token_image = fruuty_qr_token.make_image(fill_color='black', back_color='white')
                # token_image = qrcode.make(f'{self.jsonify_data}')
                # image = token_image.save('new_fruuty_token.jpeg')

                return fruuty_token_image.save(f'{self.name}.png')

        def fruuty_product_token(self):
            return

token = Token()
amount = token.fruuty_token(7777777, name='TJFiles')





# fruutty_token = [0.5, 1, 2, 2.5, 5, 10, 15, 20, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 1000, 1500, 5000]
