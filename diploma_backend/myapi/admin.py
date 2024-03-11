from django.contrib import admin
from .models import Image, CatalogItem, Product, Tag, Specification, Review, Delivery, Order
from .models import Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = 'Профиль'
    verbose_name_plural = 'Профили'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class ImageAdmin(admin.ModelAdmin):
    verbose_name = 'Изображение'
    verbose_name_plural = 'Изображения'
    pass


admin.site.register(Image, ImageAdmin)


class CatalogItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(CatalogItem, CatalogItemAdmin)


class TagsAdmin(admin.ModelAdmin):
    verbose_name = 'Тег'
    verbose_name_plural = 'Теги'
    pass


admin.site.register(Tag, TagsAdmin)


class DeliveryAdmin(admin.ModelAdmin):
    verbose_name = 'Тип доставки'
    verbose_name_plural = 'Типы доставки'
    pass


admin.site.register(Delivery, DeliveryAdmin)


class SpecificationsAdmin(admin.ModelAdmin):
    verbose_name = 'Спецификация'
    verbose_name_plural = 'Спецификации'
    pass


admin.site.register(Specification, SpecificationsAdmin)


class ReviewsAdmin(admin.ModelAdmin):
    verbose_name = 'Отзыв'
    verbose_name_plural = 'Отзывы'
    pass


admin.site.register(Review, SpecificationsAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'
    list_display = ("pk", "category", "price", "count", "title",
                    "description", "freeDelivery", "date",
                    "limited_edition")
    list_display_links = ("pk", "title")
    ordering = ("category", "title")
    search_fields = ("title", "description")
    fieldsets = [
        (None, {
            "fields": ("category", "title", "description", "fullDescription", "freeDelivery", "images",
                       "tags", "reviews", "specifications"),
        }),
        ("Price options", {
            "fields": ("price", "count"),
            "classes": ("wide", "collapse"),
        }),
        ("Extra options", {
            "fields": ("limited_edition", ),
            "classes": ("collapse", ),
            "description": "Extra options, Field 'limited_edition' is to set product as of a limited edition.",
        }),
    ]

    def description_short(self, obj: Product) -> str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    verbose_name = 'Заказ'
    verbose_name_plural = 'Заказы'
    list_display = ("pk", "user", "created_at", "delivery_type", "payment_type",
                    "status", "city", "address")
    list_display_links = ("pk", "user")
    ordering = ("user", "created_at")
    search_fields = ("city", "address")
    fieldsets = [
        (None, {
            "fields": ("user", "delivery_type", "payment_type",
                    "status", "city", "address"),
        }),
    ]
