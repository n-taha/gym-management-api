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
from rest_framework.decorators import api_view
from sslcommerz_lib import SSLCOMMERZ
from django.conf import settings as main_setting
from django.shortcuts import redirect
from datetime import date,timedelta
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from django.contrib.auth import get_user_model


User = get_user_model()


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


@api_view(["POST"])
def initiate_payment(request):
    user = request.user
    plan_id = request.data.get("memId")
    amount = request.data.get("amount")

    try:
        membership_obj = MembershipPlan.objects.get(id=plan_id)
    except MembershipPlan.DoesNotExist:
        return Response({"error": "Membership not found"}, status=404)

    settings = {
        "store_id": "phima69ac8589a1fca",
        "store_pass": "phima69ac8589a1fca@ssl",
        "issandbox": True,
    }
    sslcz = SSLCOMMERZ(settings)

    post_body = {
        "total_amount": amount,
        "currency": "BDT",
        "tran_id": f"tranxr_{membership_obj.id}_{user.id}",  # user-id ignore korbo backend-e
        "success_url": f"{main_setting.BACKEND_URL}/api/v1/payment/success/",
        "fail_url": f"{main_setting.BACKEND_URL}/api/v1/payment/fail/",
        "cancel_url": f"{main_setting.BACKEND_URL}/payment-cancel",
        "emi_option": 0,
        "cus_name": user.first_name,
        "cus_email": user.email,
        "cus_phone": user.phone_number,
        "cus_add1": user.address,
        "cus_city": "Dhaka",
        "cus_country": "Bangladesh",
        "shipping_method": "NO",
        "num_of_item": 1,
        "product_name": membership_obj.name,
        "product_category": "Membership",
        "product_profile": "general",
    }

    response = sslcz.createSession(post_body)
    return Response(response)


@api_view(["POST"])
def payment_success(request):
    """
    Frontend will POST here with Authorization token
    """
    tran_id = request.data.get("tran_id")
    if not tran_id:
        return Response({"error": "tran_id required"}, status=400)

    try:
        membership_id = tran_id.split("_")[1]
        user_id = tran_id.split('_')[2]
        membership_obj = MembershipPlan.objects.get(id=membership_id)
        user = User.objects.get(id=user_id)
    except:
        return Response(
            {"error": "Invalid tran_id or membership not found"}, status=400
        )

    # Calculate end date
    if membership_obj.duration == "yearly":
        end_date = date.today() + timedelta(days=365)
    elif membership_obj.duration == "monthly":
        end_date = date.today() + timedelta(days=30)
    elif membership_obj.duration == "weekly":
        end_date = date.today() + timedelta(days=7)
    else:
        end_date = date.today() + timedelta(days=1)

    Subscription.objects.create(
        user=user, plan=membership_obj, start_date=date.today(), end_date=end_date
    )

    return redirect(f'{main_setting.FRONTEND_URL}')


@api_view(['POST'])
def payment_fail(request):
    return redirect(f"{main_setting.FRONTEND_URL}")
