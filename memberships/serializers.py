from memberships.models import MembershipPlan, Subscription
from rest_framework import serializers
from datetime import date, timedelta
from django.utils.timezone import now

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = ['id', 'name', 'duration', 'price', 'description']


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'is_active']
        read_only_fields = ['user', 'start_date', 'end_date', 'is_active']


    def create(self, validated_data):
        user = self.context['user']
        plan = validated_data['plan']
        start_date = date.today()

        if plan.duration == 'weekly':
            end_date = start_date + timedelta(days=7)
        elif plan.duration == 'monthly':
            end_date = start_date + timedelta(days=30)
        elif plan.duration == 'yearly':
            end_date = start_date + timedelta(days=365)
        else:
            raise serializers.ValidationError('invalid plan duration')

        obj = Subscription.objects.create(
            user = user,
            plan = plan,
            start_date = start_date,
            end_date = end_date,
            is_active = True
        )

        return obj


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = MembershipSerializer()
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'is_active']
        read_only_fields = ['user', 'start_date', 'end_date', 'is_active']

    def to_representation(self, instance):
        if instance.end_date < now().date() and instance.is_active:
            instance.is_active = False
            instance.save(update_fields=["is_active"])
        return super().to_representation(instance)
