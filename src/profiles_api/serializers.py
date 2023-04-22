from rest_framework import serializers


class HelloSerializer(serializers.Serializer):
    """ Serializers a name field for test api_view  """
    name = serializers.CharField(max_length=10)


