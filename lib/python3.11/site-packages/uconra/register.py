import hashlib
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from .error import MailError
import re
from .smtp_mail import SMTP_Mail

import random
import string


class Register:
    """
     # Use case Example

    register = Register()

    print(register.userEmail('cody@gmail.com'))
    print(register.userPassword('flex'))
    print(register.userKey('flex'))
    """
    def __init__(self):
        pass
    # create and check user email function
    def userEmail(self, email):
        """
        :param email:
        :return:
        """
        self.email = email
        if re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', self.email):
            print("Okay")
        else:
            try:
                raise MailError('Invalid email input')
            except MailError as e:
                print(f'Error: {e}')
            finally:
                print('MailError')
        return str(self.email)

    # Create and hash user passerword function
    def userPassword(self, password):
        """
        :param password:
        :return:
        """
        self.password = password
        self.phPassword = PasswordHasher()
        self.hashed_argonPassword = self.phPassword.hash(self.password)
        return self.hashed_argonPassword

    # Create and hash user key function
    def userKey(self, key):
        """
        :param key:
        :return:
        """
        self.key = key
        self.phKey = PasswordHasher()
        self.hashed_argonKey = self.phKey.hash(self.key)
        return self.hashed_argonKey

    def hash_encryption(self, encryption):
        self.encryption = encryption
        self.emcrypt_data = hashlib.sha256(encryption.encode())
        self.encrypted_data = self.emcrypt_data.hexdigest()
        return self.encrypted_data

"""
The following method expresses and defines random
password generator.
It uses standard non Alpha-Numeric password compatable characters.

It is good for generating random Password for users. 
"""
def random_chars(random_chars_length):
    punc = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "14", "15"]
    string_punc = "".join(punc)
    password_chars = "".join(random.choice(string.ascii_lowercase + string_punc + string.hexdigits)
                             for i in range(random_chars_length))
    return password_chars


password_gen = random_chars(8)
# print(password_gen)





if __name__ == '__main__':
   Register()

   hash = Register()
   encryption = hash.hash_encryption('motchello')

   hash1 = Register()
   encryption1 = hash.hash_encryption('motchello')

   print(encryption)
   print(encryption1)









