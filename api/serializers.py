from rest_framework import serializers
from api.models import Category, Product, CustomUser, BlacklistedToken


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'itemsAvailable', 'on_sale']
        read_only_fields = ['itemsAvailable']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'title', 'category']

    def create(self, validated_data):
        category_data = validated_data.pop('category', None)

        # get category if exist and if not create one
        # category_instance, _ = Category.objects.get_or_create(**category_data)

    # Check if the category already exists
        try:
            category_instance = Category.objects.get(**category_data)
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category does not exist.")

        product_instance = Product.objects.create(
            category=category_instance, **validated_data)

        return product_instance


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class BlacklistedTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlacklistedToken
        fields = '__all__'
