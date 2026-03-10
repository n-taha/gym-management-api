from rest_framework import serializers
from classes.models import FitnessClass, Attendance, ClassBooking, Feedback
from users.models import User
from memberships.models import Subscription
from datetime import date

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'role']
        read_only_fields = ['id', 'first_name', 'role']

class UpdateFitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['instructor']

class FitnessClassSerializer(serializers.ModelSerializer):
    # instructor = serializers.PrimaryKeyRelatedField()
    class Meta:
        model = FitnessClass
        fields = ['id','name', 'instructor', 'description', 'schedule_date', 'start_time', 'end_time', 'capacity']


class ClassBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassBooking
        fields = ['id', 'user', 'fitness_class', 'booked_at']
        read_only_fields = ['booked_at', 'user']

    def validate_fitness_class(self, value):
        user = self.context['user']

        subscription = Subscription.objects.filter(user=user, is_active=True, end_date__gte=date.today()).exists()

        if not subscription:
            raise serializers.ValidationError('You must have a subscription to book a class!! ')

        if value.capacity <= value.bookings.count():
            raise serializers.ValidationError('Capacity is full!!!')

        return value

    def create(self, validated_data):
      user = self.context['user']
      validated_data['user'] = user
      fitness_class = validated_data['fitness_class']

      if ClassBooking.objects.filter(
          user=user,
          fitness_class=fitness_class
      ).exists():
          raise serializers.ValidationError(
              "You have already booked this class"
          )

      return super().create(validated_data)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'fitness_class', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'fitness_class', 'created_at']


    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        cls_id = self.context['fitness_class']
        cls = FitnessClass.objects.get(pk=cls_id)
        validated_data['fitness_class'] = cls

        if not ClassBooking.objects.filter(user_id=user.pk):
            raise serializers.ValidationError('You not booked this class')
        return super().create(validated_data)

# class ClassBookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model =