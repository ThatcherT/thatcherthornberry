from django.contrib import admin
from queueing.models import *

# register listener model

admin.site.register(Listener)
admin.site.register(Follower)
