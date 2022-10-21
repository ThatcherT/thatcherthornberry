from django.contrib import admin
from django.contrib.sessions.models import Session

from queueing.models import *

# register listener model

admin.site.register(Listener)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]


admin.site.register(Session, SessionAdmin)
