from django.apps import AppConfig


class ArticlesConfig(AppConfig):
    name = 'articles'

    def ready(self):
        #print('*' * 10, 'at read')
        import articles.signals