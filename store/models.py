from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from .managers import CustomUserManager


# Custom User Model
class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name="Username")
    first_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Фамилия")
    phone_number = models.CharField(max_length=13, null=True, blank=True, verbose_name="Телефон номер")
    last_login = models.DateTimeField(auto_now=True, null=True)
    password = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    def __str__(self):
        return self.first_name + " " + self.last_name


# Stores model
class Store(models.Model):
    image = models.ImageField(verbose_name="Логотип", upload_to='logo', null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name="Название магазина")
    shortInfo = models.CharField(max_length=455, verbose_name="Краткое описание")
    location = models.CharField(max_length=255, verbose_name="Адресс")
    owner = models.CharField(max_length=255, verbose_name="ФИО владельца")
    phone = models.CharField(max_length=255, verbose_name="Телефон номер")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

    def __str__(self):
        return self.name

    def image_tag(self):
        return format_html('<img src="{}" style="width:70px; height:70px"/>'.format(self.image.url))


# Color model for Category
class Color(models.Model):
    name = models.CharField(null=True, max_length=50, verbose_name="Цвет")
    code = models.CharField(null=True, max_length=50, blank=True)

    class Meta:
        verbose_name = "Цвет"
        verbose_name_plural = "Цвета"

    def __str__(self):
        return self.name

    def color_tag(self):
        if self.code is not None:
            return mark_safe('<p style="background-color:{}"> Color</p>'.format(self.code))
        else:
            return ""


# Category model
class Category(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="Название")
    image = models.ImageField(null=True, verbose_name="Фото", upload_to='icons')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, verbose_name="Цвет", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def image_tag(self):
        return format_html('<img src="{}" style="object-fit:contain; padding:4px; width: 64px; height: 64px;'
                           ' border-radius: 50%; background-color: white;"/>'.format(self.image.url))


# Brand model
class Brand(models.Model):
    name = models.CharField(max_length=50, verbose_name="Бренд")

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=150, verbose_name="Валютная единица")

    class Meta:
        verbose_name = "Валютная единица"
        verbose_name_plural = "Валютная единицы"

    def __str__(self):
        return self.name


# Product model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категории")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Бренд")
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name="Валютная единица")
    name = models.CharField(max_length=255, verbose_name="Название")
    description = RichTextUploadingField(verbose_name="Описание")
    price = models.FloatField(default=None, verbose_name="Цена")
    discount = models.FloatField(null=True, verbose_name="Скидка(%)")
    discounted_price = models.FloatField(null=True, verbose_name="Цена со скидкой")
    sell_price = models.FloatField(null=True, verbose_name="Цена продажи")
    image = models.ImageField(upload_to="products", null=True, verbose_name="Главная фото")
    is_available = models.BooleanField(default=True, verbose_name="Доступен")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return self.name

    def image_tag(self):
        return format_html('<img src="{}" style="width:120px; height:120px"/>'.format(self.image.url))


# Image Model For Products
class ProductsImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="Фото")
    image = models.ImageField(upload_to="products", null=True, blank=True, verbose_name="Фото")

    class Meta:
        verbose_name = "Фото продукта"
        verbose_name_plural = "Фото продукты"

    def __str__(self):
        return "%s" % self.product.name


# Option Model
class Option(models.Model):
    name = models.CharField(max_length=255, null=True, verbose_name="Название")

    class Meta:
        verbose_name = "Варианты название"
        verbose_name_plural = "Варианты название"

    def __str__(self):
        return self.name


class OptionValue(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, null=True, verbose_name="Вариант")
    name = models.CharField(max_length=255, null=True, verbose_name="Название")

    class Meta:
        verbose_name = "Значение варианты"
        verbose_name_plural = "Значение варианты"

    def __str__(self):
        return self.name


# Product Option Model
class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, verbose_name="Продукт")
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Цвет")
    option = models.ForeignKey(OptionValue, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Варианты")
    price = models.FloatField(default=None, verbose_name="Цена", null=True, blank=True)

    class Meta:
        verbose_name = "Вариант продукта"
        verbose_name_plural = "Варианты продукты"

    def __str__(self):
        return self.product.name
