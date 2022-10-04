from django.contrib import admin
from queueing.models import *
from django.contrib.sessions.models import Session

# register listener model

admin.site.register(Listener)
admin.site.register(Follower)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]


admin.site.register(Session, SessionAdmin)
