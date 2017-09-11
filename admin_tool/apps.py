from django.apps import AppConfig


class AdminToolConfig(AppConfig):
    name = 'admin_tool'

    def ready(self):
        import admin_tool.signals  # noqa
