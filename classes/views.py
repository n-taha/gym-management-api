from django.shortcuts import render
from classes.models import FitnessClass, ClassBooking, Attendance, Feedback
from classes.serializers import FitnessClassSerializer, InstructorSerializer, ClassBookingSerializer, UpdateFitnessClassSerializer, FeedbackSerializer
from rest_framework.viewsets import ModelViewSet
from users.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from classes.permissions import IsAdminOrStaffOrReadonly, IsAdminOrReadOnly, CustomPermission, FeedBackPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

class FitnessClassViewSet(ModelViewSet):

    """
    - Retrive All Class --> Anyone
    - Create , Update , Delete Class ---> Admin User

    """

    queryset = FitnessClass.objects.all()
    serializer_class = FitnessClassSerializer
    # permission_classes = [IsAuthenticated, IsAdminOrStaffOrReadonly]

    @swagger_auto_schema(
        operation_summary='TO List all classess',
        operation_description= 'We Can retrive all by uisng this method'
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['patch'])
    def update_instructor(self, request, pk=None):
        cls = self.get_object()
        serializer = UpdateFitnessClassSerializer(cls, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(f'Instructor updated')

    def get_permissions(self):
        if self.action in ['partial_update', 'create', 'destroy', 'update', 'update_instructor']:
            return [IsAdminUser()]
        return [AllowAny()]


class InstructorViewSet(ModelViewSet):

    """
    - Retrive Only a Authenticated User
    - Admin User can user turn to instructor by changin role
    """
    serializer_class = InstructorSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(role='STAFF')

class InstructorClassViewSet(ModelViewSet):
    serializer_class = FitnessClassSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticated]
    def get_queryset(self):
        return FitnessClass.objects.filter(instructor_id=self.kwargs.get('instructor_pk'))


class ClassBookingViewSet(ModelViewSet):
    """
    - Admin Can Retrive all bookings
    - Authenticated User and Preimum User can book class
    - Authenticated User just see his/her own bookings
    """
    serializer_class = ClassBookingSerializer
    permission_classes = [IsAuthenticated, CustomPermission]

    def get_queryset(self):
        if self.request.user.is_staff:
            return ClassBooking.objects.all()
        return ClassBooking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {'user':self.request.user}


class FeedbackViewSet(ModelViewSet):

    """
    Only specific classes booked user can give review for each class
    """

    serializer_class = FeedbackSerializer
    permission_classes = [FeedBackPermission]

    def get_queryset(self):
        return Feedback.objects.filter(fitness_class_id = self.kwargs.get('fitness_class_pk'))

    def get_serializer_context(self):
        return {'user':self.request.user, 'fitness_class':self.kwargs.get('fitness_class_pk')}




# class ClassBookingViewSet(ModelViewSet):
#     queryset = ClassBooking.objects.all()
#     serializer_class =