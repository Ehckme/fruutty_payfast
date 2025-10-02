class MailError(Exception):
    """ Custon Mail error message
    e.g
        raise MailError('type your custom error message here')

        greetings = 'Hello'
        response = 'Hi'
        def greeting(greet, respond):
            if greet == greetings and respond == response:
                print('Great communication skills')
            else:
                try:
                    raise MailError('Comunication misunderstood')
                except MailError as e:
                    print(e)

        greeting('Hello', 'Hi')
        output: Great communication skills

    """
    def __init__(self, message=None):
        self.message = message
        self.error_code = 'MailError'
        super().__init__(self.message)

class PasswordError(Exception):
    """ Custon Password error message
        e.g
            raise PasswordError('type your custom error message here')

        greetings = 'Hello'
        response = 'Hi'
        def greeting(greet, respond):
            if greet == greetings and respond == response:
                print('Great communication skills')
            else:
                try:
                    raise PasswordError('Comunication misunderstood')
                except PasswordError as e:
                    print(e)

        greeting('Hello', 'Hi')
        output: Great communication skills

    """
    def __init__(self, message=None):
        self.message = message
        self.error_code = 'PasswordError'
        super().__init__(self.message)

if __name__ == '__main__':
   MailError()