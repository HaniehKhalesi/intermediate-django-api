from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import HelloSerializer
from rest_framework import status


class HelloAPIView(APIView):
    """Test API VIEW"""
    serializer_class = HelloSerializer

    def get(self, request, format=None):
        """Return a list af API View fe+atures"""
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over your logic',
            'Is mapped manually to URLs',
        ]
        return Response({'message': 'Hello', 'an_apiview': an_apiview })

    def post(self, request):
        """ create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            message = f'Hello {name}'
            return Response({"name": message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handel update on object"""
        return Response({"methode": "put"})

    def patch(self, request, pk=None):
        """Handel a partial update of an object"""
        return Response({"methode": "patch"})

    def delete(self, request, pk=None):
        """Handel a delete of an object"""
        return Response({"methode": "delete"})



