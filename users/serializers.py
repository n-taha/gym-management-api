from djoser.serializers import UserCreateSerializer as BaseUserSerializer
from djoser.serializers import UserSerializer
class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'email', 'role', 'first_name', 'last_name', 'password', 'address', 'phone_number']
        read_only_fields = ['role']

class ViewUserSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'first_name', 'last_name', 'address', 'phone_number', 'role']