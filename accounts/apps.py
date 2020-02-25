from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        #print('*'*10, 'at read, '*'*10)
        import accounts.signals


