from rest_framework import serializers
from .models import (UserProfile, Category, SubCategory, Product,
                      ProductImage, Review, Cart, CartItem)

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'Category_name', 'Category_image']


class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name']


class SubCategoryProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name']


class CategoryDetailSerializer(serializers.ModelSerializer):
    category_sub = SubCategoryListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['Category_name', 'category_sub']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product_image']


class ProductListSerializer(serializers.ModelSerializer):
    photo_product = ProductImageSerializer(read_only=True, many=True)
    subcategory = SubCategoryProductListSerializer()
    average_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'price', 'subcategory', 'product_type',
                  'photo_product', 'average_rating', 'count_people']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    subcategory_product = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = SubCategory
        fields = ['subcategory_name', 'subcategory_product']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserProfileNameSerializer()
    created_data = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Review
        fields = ['id', 'user', 'star', 'text', 'created_data']


class ProductDetailSerializer(serializers.ModelSerializer):
    photo_product = ProductImageSerializer(read_only=True, many=True)
    subcategory = SubCategoryProductListSerializer()
    average_rating = serializers.SerializerMethodField()
    count_people = serializers.SerializerMethodField()
    product_review = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['product_name', 'price', 'subcategory', 'description',
                  'created_data', 'product_type', 'article', 'video',
                  'photo_product', 'count_people', 'average_rating', 'product_review']

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_count_people(self, obj):
        return obj.get_count_people()


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'star', 'text', 'created_data']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        write_only=True,
        source='product'
    )
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']

    def get_total_price(self, obj):
            return obj.get_total_price()

