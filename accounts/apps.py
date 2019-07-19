from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        #print('*'*10, 'at ready', '*'*10)
        import accounts.signals


