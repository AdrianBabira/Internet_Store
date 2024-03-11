from django.db import models
from django.contrib.auth.models import User


class Image(models.Model):
    def image_directory_path(self, filename: str) -> str:
        if not self.pk:
            try:
                document_next_id = Image.objects.order_by('-id').first().id + 1
            except:
                document_next_id = 1
            self.pk = document_next_id
        return "images/image_{id}/{filename}".format(
            id=self.pk,
            filename=filename,
        )
    alt = models.CharField(
        max_length=200,
        null=False,
        blank=True
    )
    src = models.ImageField(
        upload_to=image_directory_path
    )

    def __str__(self):
        return self.alt

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ('alt', 'pk', )


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    phone = models.TextField(
        max_length=500,
        blank=True
    )
    avatar = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиля'


class CatalogItem(models.Model):
    title = models.CharField(
        max_length=200,
        null=False,
        blank=True
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.PROTECT
    )
    parent = models.ForeignKey(
        'CatalogItem',
        null=True,
        blank=True,
        related_name='subcategories',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('title',)


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)


class Review(models.Model):
    author = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        verbose_name="Автор"
    )
    email = models.CharField(
        max_length=320,
        null=False,
        blank=True,
        verbose_name="Электронная почта"
    )
    text = models.TextField(
        null=False,
        blank=True,
        verbose_name="Содержание"
    )
    rate = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Оценка"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата"
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('author',)


class Specification(models.Model):
    name = models.CharField(max_length=150, null=False, blank=True, verbose_name="Имя")
    value = models.TextField(null=False, blank=True, verbose_name="Значение")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Спецификация'
        verbose_name_plural = 'Спецификации'
        ordering = ('name',)


class Product(models.Model):
    category = models.ForeignKey(
        CatalogItem,
        on_delete=models.PROTECT,
        verbose_name="Категория"
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Цена"
    )
    count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата"
    )
    title = models.CharField(
        max_length=100,
        null=False,
        blank=True,
        verbose_name="Наименование"
    )
    description = models.CharField(
        max_length=250,
        null=False,
        blank=True,
        verbose_name="Краткое описание"
    )
    freeDelivery = models.BooleanField(
        default=False,
        verbose_name="Бесплатная доставка"
    )
    images = models.ManyToManyField(
        Image,
        blank=True,
        related_name="products",
        verbose_name="Изображения"
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="products",
        verbose_name="Теги"
    )
    limited_edition = models.BooleanField(
        default=False,
        verbose_name="Ограниченный тираж"
    )
    fullDescription = models.TextField(
        null=False,
        blank=True,
        verbose_name="Полное описание"
    )
    reviews = models.ManyToManyField(
        Review,
        blank=True,
        related_name="products",
        verbose_name="Отзывы"
    )
    specifications = models.ManyToManyField(
        Specification,
        blank=True,
        related_name="products",
        verbose_name="Спецификации"
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class UserSession(models.Model):
    sessionID = models.CharField(
        max_length=250,
        null=False,
        blank=True,
        verbose_name="Идентификатор сессии"
    )

    class Meta:
        verbose_name = 'Пользовательская сессия'
        verbose_name_plural = 'Пользовательские сессии'


class Basket(models.Model):
    session = models.ForeignKey(
        UserSession,
        on_delete=models.PROTECT,
        verbose_name="Сессия"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Товар"
    )
    count = models.IntegerField(
        default=0,
        verbose_name="Количество"
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Delivery(models.Model):
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Тип доставки"
    )
    price = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Цена"
    )
    is_free_from = models.DecimalField(
        decimal_places=2,
        max_digits=15,
        verbose_name="Бесплатно с:"
    )

    class Meta:
        verbose_name = 'Тип доставки'
        verbose_name_plural = 'Типы доставки'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Пользователь"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата"
    )
    delivery_type = models.ForeignKey(
        Delivery,
        on_delete=models.PROTECT,
        verbose_name="Тип доставки"
    )
    payment_type = models.CharField(
        max_length=150,
        null=False,
        blank=True,
        default="online",
        verbose_name="Тип оплаты"
    )
    status = models.CharField(
        max_length=150,
        null=False,
        blank=True,
        default="created",
        verbose_name="Состояние заказа"
    )
    city = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Город"
    )
    address = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Адрес доставки"
    )

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.PROTECT,
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Товар"
    )
    count = models.IntegerField(
        default=0,
        verbose_name="Количество"
    )

    class Meta:
        verbose_name = 'Строка заказа'
        verbose_name_plural = 'Строки заказа'
