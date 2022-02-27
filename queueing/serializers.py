# from music.queueing.models import Listener
from rest_framework import serializers
from queueing.models import Listener


class ListenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listener
        fields = ["id", "name", "code", "number"]
