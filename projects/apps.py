from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "projects"

    def ready(self):
        from django.contrib.auth.models import Group
        from django.db.models.signals import post_migrate

        def create_role_groups(sender, **kwargs):
            Group.objects.get_or_create(name="Student")
            Group.objects.get_or_create(name="Guide")

        post_migrate.connect(create_role_groups, sender=self)
