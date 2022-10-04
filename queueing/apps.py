from django.apps import AppConfig
from django.utils.autoreload import autoreload_started
from pathlib import Path
import os


def my_watch_dog(sender, *args, **kwargs):
    watch = sender.extra_files.add

    # get all files in queueing directory, add to watchdog for file reload
    for root, dirs, files in os.walk("queueing"):
        for file in files:
            file_path = os.path.join(root, file)
            watch(Path(file_path))


class QueueingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "queueing"

    def ready(self):
        autoreload_started.connect(my_watch_dog)
