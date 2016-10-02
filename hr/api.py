from rest_framework import viewsets

from hr.models import EmployeeGradeScale
from hr.serializers import EmployeeGradeScaleSerializer


class EmployeeGradeScaleViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGradeScale.objects.all()
    serializer_class = EmployeeGradeScaleSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category', 'in_stock')