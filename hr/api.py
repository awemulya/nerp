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

    def get_queryset(self):
        if self.request.GET.get('validity_id'):
            return self.queryset.filter(validity_id=self.request.GET.get('validity_id'))
        return self.queryset

    def create(self, request, *args, **kwargs):
        rows = request.data
        for row in rows:
            for roow in row['employee_grades']:
                import ipdb
                ipdb.set_trace()
                # obj, created = EmployeeGradeScale.objects.update_or_create(**roow['scale'])
                # print obj, created



class EmployeeGradeGroupViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGradeGroup.objects.all()
    serializer_class = EmployeeGradeGroupSerializer

    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category', 'in_stock')

    # def get_queryset(self):
    #     if self.request.GET.get('validity_id'):
    #         return self.queryset.filter(employee_grades__grade_scales__validity_id=self.request.GET.get('validity_id'))
    #     return self.queryset

    # def list(self, request, *args, **kwargs):
    #     super(EmployeeGradeGroupViewSet, self).list(request, *args, **kwargs)


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
