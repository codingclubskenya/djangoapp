from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from tenant.serializers import TenantSerializer


class UserSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(read_only=True)
    tenant_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'phone', 'role',
            'is_synced', 'created_at', 'updated_at', 'tenant',
            'tenant_id', 'password', 'password_reset_token',
            'password_reset_expires', 'reset_token', 'reset_token_expiry',
        ]
        read_only_fields = [
            'id', 'created_at', 'updated_at',
            'password_reset_token', 'password_reset_expires',
            'reset_token', 'reset_token_expiry',
        ]

    def create(self, validated_data):
        tenant_id = validated_data.pop('tenant_id', None)
        password = validated_data.pop('password', None)
        if tenant_id:
            from tenant.models import Tenant
            validated_data['tenant'] = Tenant.objects.get(id=tenant_id)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        tenant_id = validated_data.pop('tenant_id', None)
        if tenant_id:
            from tenant.models import Tenant
            instance.tenant = Tenant.objects.get(id=tenant_id)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email'], tenant__is_active=True).first()
        if user is None:
            raise serializers.ValidationError('Invalid credentials')

        password_valid = user.check_password(data['password'])

        if not password_valid:
            raise serializers.ValidationError('Invalid credentials')

        refresh = _UserToken.for_user(user)
        return {
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class _UserToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        if user.tenant_id:
            token['tenant_id'] = str(user.tenant_id)
        token['role'] = user.role
        token['email'] = user.email
        token['full_name'] = user.full_name or ''
        return token
