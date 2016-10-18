from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.response import Response

from hr.models import EmployeeGradeScale, EmployeeGradeGroup, GradeScaleValidity, EmployeeGrade, AllowanceValidity, \
    AllowanceName, Allowance
from hr.serializers import EmployeeGradeScaleSerializer, EmployeeGradeGroupSerializer, GradeScaleValiditySerializer, \
    EmployeeGradeSerializer, AllowanceValiditySerializer, AllowanceNameSerializer, AllowanceSerializer


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
        if rows:
            validity_id = rows[0]['employee_grades'][0]['scale']['validity_id']
            for row in rows:
                for roow in row['employee_grades']:

                    try:
                        obj, created = EmployeeGradeScale.objects.update_or_create(**roow['scale'])
                    except (ValueError, IntegrityError):
                        pass
            saved_data = EmployeeGradeScaleSerializer(
                EmployeeGradeScale.objects.filter(validity_id=validity_id),
                many=True
            )
            return Response(saved_data.data)
        else:
            return Response([])


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


class EmployeeGradeViewSet(viewsets.ModelViewSet):
    queryset = EmployeeGrade.objects.all()
    serializer_class = EmployeeGradeSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)
    # filter_backends = (filters.DjangoFilterBackend,)
    # filter_fields = ('category', 'in_stock')


# Allowance Viewset

class AllowanceValidityViewSet(viewsets.ModelViewSet):
    queryset = AllowanceValidity.objects.all()
    serializer_class = AllowanceValiditySerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)


class AllowanceNameViewSet(viewsets.ModelViewSet):
    queryset = AllowanceName.objects.all()
    serializer_class = AllowanceNameSerializer


class AllowanceViewSet(viewsets.ModelViewSet):
    queryset = Allowance.objects.all()
    serializer_class = AllowanceSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            validity_id = self.request.GET.get('validity_id')
            name_id = self.request.GET.get('validity_id')
            return self.queryset.filter(validity_id=validity_id, name_id=name_id)
        return self.queryset

    def create(self, request, *args, **kwargs):
        rows = request.data
        if rows:
            validity_id = rows[0]['employee_grades'][0]['allowance']['validity_id']
            name_id = rows[0]['employee_grades'][0]['allowance']['name_id_id']
            for row in rows:
                for roow in row['employee_grades']:

                    try:
                        obj, created = Allowance.objects.update_or_create(**roow['scale'])
                    except (ValueError, IntegrityError):
                        pass
            saved_data = AllowanceSerializer(
                Allowance.objects.filter(validity_id=validity_id, name_id=name_id),
                many=True
            )
            return Response(saved_data.data)
        else:
            return Response([])

# End Allowance Viewset