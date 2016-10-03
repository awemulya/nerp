from rest_framework import viewsets

from hr.models import EmployeeGradeScale, EmployeeGradeGroup, GradeScaleValidity, EmployeeGrade
from hr.serializers import EmployeeGradeScaleSerializer, EmployeeGradeGroupSerializer, GradeScaleValiditySerializer, \
    EmployeeGradeSerializer


class EmployeeGradeScaleViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGradeScale.objects.all()
    serializer_class = EmployeeGradeScaleSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category', 'in_stock')


class EmployeeGradeGroupViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGradeGroup.objects.all()
    serializer_class = EmployeeGradeGroupSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category', 'in_stock')


class GradeScaleValidityViewSet(viewsets.ModelViewSet):
    queryset = GradeScaleValidity.objects.all()
    serializer_class = GradeScaleValiditySerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category', 'in_stock')


class EmployeeGradeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGrade.objects.all()
    serializer_class = EmployeeGradeSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category', 'in_stock')