import hashlib
from .register import Register
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class Login(Register):
    """  # Use case 1

    mail = Login()

    dbPassword = 'flex'
    dbEmail = 'cody@gmail.com'

    if mail.loginEmail('cody@gmail.com') == dbEmail and mail.loginPassword('flex', dbPassword):
        print('Welcome to yout dashboard')
    else:
        print('Please enter corrrect login details')

    # Use case 2

    dashboard = Login()

    if dashboard.dashboard('cody@gmail.com', dbEmail, 'flex', dbPassword):
        print('THis is your dashboard')
    """
    def __init__(self,):
        pass

    # create and check user login-email function
    def loginEmail(self, email):
        """
        :param email:
        :return verified email from super() [Register]:
        """
        self.email = email
        if self.email == ' ' or self.email == None:
            print('Please enter email')
        else:
            return super().userEmail(email=self.email)

    # create and validate user login-password function

    def loginPassword(self, loginPassword, hashedPassword):
        """
        :param loginPassword:
        :param hashedPassword:
        :return:
        """
        self.loginPassword = loginPassword
        self.hashLoginPassword = super().userPassword(self.loginPassword)

        try:
            self.ph = PasswordHasher()
            if self.ph.verify(self.hashLoginPassword, hashedPassword):
                print('okay Argon verified ')
                return self.hashLoginPassword
        except:
            print('Not okay, Argon verified ')


        if self.hashLoginPassword != hashedPassword:
            print('Please enter correct password')
        else:
            print('Password match')
            return self.hashLoginPassword

    # create and validate user login-key function

    def lognKey(self, loginKey, hashedKey):
        self.loginKey = loginKey
        self.hashLoginKey = super().userKey(self.loginKey)
        if self.hashLoginKey != hashedKey:
            print('Please enteer correct user key')
        else:
            print('Key matches')
            return self.hashLoginKey

    def dashboard(self, input_email, db_email, input_password, db_hash_password):
        self.input_email = input_email
        self.db_email = db_email
        self.input_password = input_password
        self.db_hash_password = db_hash_password
        self.display_dashboard = Login()

        if self.display_dashboard.loginEmail(
                self.input_email
        ) == self.db_email and self.display_dashboard.loginPassword(
                self.input_password, self.db_hash_password):

            # print('Welcome to yout dashboard')
            return

        else:
            print('Please enter corrrect login details')

if __name__ == '__main__':
    Login()


