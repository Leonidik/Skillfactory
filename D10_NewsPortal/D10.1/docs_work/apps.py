from django.apps import AppConfig

class DocsWorkConfig(AppConfig):
    name = 'docs_work'
    
    # нам надо переопределить метод ready, чтобы при готовности нашего приложения импортировался модуль со всеми функциями обработчиками
    def ready(self):
        import docs_work.signals      
        import docs_work.tasks  
    
    
