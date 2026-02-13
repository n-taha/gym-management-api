from django.urls import path, include
from rest_framework_nested import routers
from classes.views import FitnessClassViewSet, InstructorViewSet, InstructorClassViewSet, ClassBookingViewSet, FeedbackViewSet
from memberships.views import MemberShipPlanViewSet, SubscriptionViewSet

router = routers.DefaultRouter()
router.register('classes', FitnessClassViewSet, basename='classes')
router.register('instructors', InstructorViewSet, basename='instructors')
instructor_router = routers.NestedDefaultRouter(router, 'instructors', lookup='instructor')
instructor_router.register('classes', InstructorClassViewSet, basename='instructor')
router.register('classbookings', ClassBookingViewSet, basename='classbooking')
router.register('memberships', MemberShipPlanViewSet, basename='memberships')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')
classes_router =routers.NestedDefaultRouter(router, 'classes', lookup='fitness_class')
classes_router.register('feedbacks', FeedbackViewSet, basename='feedback')
urlpatterns = [
    path('', include(router.urls)),
    path('', include(instructor_router.urls)),
    path("", include(classes_router.urls))
]
