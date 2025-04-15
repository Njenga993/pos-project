from rest_framework import serializers
from .models import Product
from .models import Sale, SaleItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']  # Include the fields you want to expose

class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity',]

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        sale = Sale.objects.create(**validated_data)

        for item in items_data:
            product = item['product']
            quantity = item['quantity']
            subtotal = item['subtotal']

            # Reduce stock
            product.stock -= quantity
            product.save()

            SaleItem.objects.create(sale=sale, product=product, quantity=quantity, subtotal=subtotal)

        return sale