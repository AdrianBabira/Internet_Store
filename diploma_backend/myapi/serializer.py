from django.contrib.auth.models import User
from . import models
from rest_framework import serializers


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = ['src', 'alt']


class SubCategorySerializer(serializers.ModelSerializer):
    image = ImagesSerializer(many=False)

    class Meta:
        model = models.CatalogItem
        fields = ['id', 'title', 'image']


class CatalogItemSerializer(serializers.ModelSerializer):
    image = ImagesSerializer(many=False)
    subcategories = SubCategorySerializer(many=True)

    class Meta:
        model = models.CatalogItem
        fields = ['id', 'title', 'image', 'subcategories']


class TagsFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id', 'name']


class TagsIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tag
        fields = ['id']


class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = ['author', 'email', 'text', 'rate', 'date']


class SpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specification
        fields = ['name', 'value']


class ProductShortSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True)
    tags = TagsFullSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_reviews(self, obj):
        return obj.reviews.all().count()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            sum_rates = 0
            for review in reviews:
                sum_rates += review.rate
            return sum_rates/obj.reviews.all().count()
        return 0

    class Meta:
        model = models.Product
        fields = ['id', 'category', 'price', 'count', 'date', 'title',
                  'description', 'freeDelivery', 'images', 'tags',
                  'reviews', 'rating']


class ProductFullSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True)
    reviews = ReviewsSerializer(many=True)
    # specifications = SpecificationsSerializer(many=True)
    tags = serializers.SerializerMethodField()
    specifications = serializers.SerializerMethodField()
    def get_tags(self, instance):
        names = []
        a = instance.tags.get_queryset()
        for i in a:
            name = dict()
            name["name"] = i.name
            names.append(name)
        return names

    def get_specifications(self, instance):
        names = []
        a = instance.specifications.get_queryset()
        for i in a:
            name = dict()
            name["name"] = i.name
            name["value"] = i.value
            names.append(name)
        return names

    class Meta:
        model = models.Product
        fields = ['id', 'category', 'price', 'count', 'date', 'title',
                  'description', 'fullDescription', 'freeDelivery', 'images', 'tags',
                  'reviews', 'specifications']


class BasketSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    freeDelivery = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_id(self, instance):
        return instance.product.pk

    def get_category(self, instance):
        return instance.product.category.pk

    def get_price(self, instance):
        return instance.product.price

    def get_count(self, instance):
        return instance.count

    def get_date(self, instance):
        return instance.product.date

    def get_title(self, instance):
        return instance.product.title

    def get_description(self, instance):
        return instance.product.description

    def get_freeDelivery(self, instance):
        return instance.product.freeDelivery

    def get_images(self, instance):
        return ImagesSerializer(instance.product.images, many=True).data

    def get_tags(self, instance):
        return TagsFullSerializer(instance.product.tags, many=True).data

    def get_reviews(self, instance):
        return instance.product.reviews.all().count()

    def get_rating(self, instance):
        reviews = instance.product.reviews.all()
        if reviews:
            sum_rates = 0
            for review in reviews:
                sum_rates += review.rate
            return sum_rates/instance.product.reviews.all().count()
        return 0

    class Meta:
        model = models.Basket
        fields = [
            'id', 'category', 'price', 'count', 'date', 'title',
            'description', 'freeDelivery', 'images', 'tags',
            'reviews', 'rating'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    freeDelivery = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_id(self, instance):
        return instance.product.pk

    def get_category(self, instance):
        return instance.product.category.pk

    def get_price(self, instance):
        return instance.product.price

    def get_count(self, instance):
        return instance.count

    def get_date(self, instance):
        return instance.product.date

    def get_title(self, instance):
        return instance.product.title

    def get_description(self, instance):
        return instance.product.description

    def get_freeDelivery(self, instance):
        return instance.product.freeDelivery

    def get_images(self, instance):
        return ImagesSerializer(instance.product.images, many=True).data

    def get_tags(self, instance):
        return TagsFullSerializer(instance.product.tags, many=True).data

    def get_reviews(self, instance):
        return instance.product.reviews.all().count()

    def get_rating(self, instance):
        reviews = instance.product.reviews.all()
        if reviews:
            sum_rates = 0
            for review in reviews:
                sum_rates += review.rate
            return sum_rates/instance.product.reviews.all().count()
        return 0

    class Meta:
        model = models.OrderItem
        fields = [
            'id', 'category', 'price', 'count', 'date', 'title',
            'description', 'freeDelivery', 'images', 'tags',
            'reviews', 'rating'
        ]


class OrderSerializer(serializers.ModelSerializer):
    createdAt = serializers.SerializerMethodField()
    fullName = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    totalCost = serializers.SerializerMethodField()
    deliveryType = serializers.SerializerMethodField()
    paymentType = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    def get_createdAt(self, instance):
        return instance.created_at
    def get_fullName(self, instance):
        return instance.user.first_name + " " + instance.user.last_name

    def get_email(self, instance):
        return instance.user.email

    def get_phone(self, instance):
        profile, created = models.Profile.objects.get_or_create(user=instance.user)
        if not created:
            return profile.phone
        return None

    def get_totalCost(self, instance):
        total = 0
        products = models.OrderItem.objects.filter(order=instance).all()
        # print("Serializer get_totalCost: ", products)
        for order_item in products:
            total += order_item.count * order_item.product.price
        if instance.delivery_type.is_free_from > 0:
            if total < instance.delivery_type.is_free_from:
                total += instance.delivery_type.price
        else:
            total += instance.delivery_type.price
        return total

    def get_deliveryType(self, instance):
        return instance.delivery_type.name

    def get_paymentType(self, instance):
        return instance.payment_type

    def get_products(self, instance):
        products_all = models.OrderItem.objects.filter(order=instance).all()
        return OrderItemSerializer(products_all, many=True).data

    class Meta:
        model = models.Order
        fields = ["id", "createdAt", "fullName", "email", "phone",
                  "deliveryType", "paymentType", "totalCost", "status",
                  "city", "address", "products"]


class UserSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_fullName(self, instance):
        return instance.first_name + " " + instance.last_name

    def get_phone(self, instance):
        return instance.profile.phone

    def get_avatar(self, instance):
        return ImagesSerializer(instance.profile.avatar, many=False).data

    class Meta:
        model = User
        fields = [
            "fullName", "email", "phone", "avatar"
        ]
