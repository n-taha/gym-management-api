from django.shortcuts import render
from memberships.models import Subscription, MembershipPlan
from rest_framework.viewsets import ModelViewSet
from memberships.serializers import MembershipSerializer, SubscriptionSerializer, SubscriptionCreateSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from classes.permissions import IsAdminOrReadOnly, IsAdminOrStaffOrReadonly

class MemberShipPlanViewSet(ModelViewSet):
    """
    - Anyone can retrive the membership plan list
    - Admin or staff can create new membership
    """
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = [IsAdminOrStaffOrReadonly]


class SubscriptionViewSet(ModelViewSet):
    """
    - Only Authenticated User can buy Subscription
    - Admin and staff can see subscription list
    - normal user can see his/her own subscription
    """
    # serializer_class = SubscriptionSerializer
    http_method_names = ['get', 'post', 'head', 'options']
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Subscription.objects.all()
        return Subscription.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return SubscriptionCreateSerializer
        return SubscriptionSerializer

    def get_serializer_context(self):
        return {'user':self.request.user}

    @action(detail=False, methods=['get'])
    def active(self, request):
        subscription = Subscription.objects.filter(user=self.request.user, is_active=True, end_date__gte = date.today()).order_by('-start_date').first()

        if not subscription:
            return Response('No Active Subscription')

        serializer = self.get_serializer(subscription)
        return Response(serializer.data)
