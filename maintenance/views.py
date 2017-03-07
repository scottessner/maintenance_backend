from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from maintenance.models import Car, FillUp
from maintenance.serializers import CarSerializer, FillupSerializer
from django_filters.rest_framework import DjangoFilterBackend


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = (DjangoFilterBackend,)

class FillUpViewSet(viewsets.ModelViewSet):
    queryset = FillUp.objects.all()
    serializer_class = FillupSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('car',)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cars': reverse('car-list', request=request, format=format),
        'fill-ups': reverse('fill-up-list', request=request, format=format)
    })