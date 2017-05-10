from django.conf.urls import url
# from rest_framework import renderers
from rest_framework.schemas import get_schema_view
from maintenance.views import CarViewSet, FillUpViewSet, RepairViewSet, api_root

car_list = CarViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

car_detail = CarViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

fillup_list = FillUpViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

fillup_detail = FillUpViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

repair_list = RepairViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

repair_detail = RepairViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    url(r'^$', api_root),
    url(r'^cars/$', car_list, name='car-list'),
    url(r'^cars/(?P<pk>[0-9]+)/$', car_detail, name='car-detail'),
    url(r'^fill-ups/$', fillup_list, name='fill-up-list'),
    url(r'^fill-ups/(?P<pk>[0-9]+)/$', fillup_detail, name='fillup-detail'),
    url(r'^repairs/$', repair_list, name='repair-list'),
    url(r'^repairs/(?P<pk>[0-9]+)/$', repair_detail, name='repair-detail')
]