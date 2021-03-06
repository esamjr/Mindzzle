from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        """
        override to perform initialization for registering signals
        """
        import account.services.automation
