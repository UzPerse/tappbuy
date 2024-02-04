from rest_framework import serializers
from .models import *


# Store detail serializer
class StoreSerializers(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


# Category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# Product images
class ProductsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsImage
        fields = "__all__"


# Product Variant Serializer
class ProductVariantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="option.option", read_only=True)
    value = serializers.CharField(source="option.name", read_only=True)
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    category_id = serializers.IntegerField(source="product.category.id", read_only=True)

    class Meta:
        model = ProductVariant
        fields = ['id', 'name', 'value', 'price', 'product_id', 'category_id']


# Product serializer
class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source="category.id", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_id = serializers.IntegerField(source="brand.id", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    currency_id = serializers.CharField(source="currency.id", read_only=True)
    currency = serializers.CharField(source="currency.name", read_only=True)
    images = ProductsImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True
    )
    variants = ProductVariantSerializer(source="product", many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Product.objects.create(**validated_data)

        for image in uploaded_images:
            ProductsImage.objects.create(product=product, image=image)

        return product

