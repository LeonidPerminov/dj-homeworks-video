from rest_framework import serializers
from logistic.models import Product, Stock, StockProduct


# Сериализатор для продукта
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


# Сериализатор для позиции продукта на складе
class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


# Сериализатор для склада
class StockSerializer(serializers.ModelSerializer):
    # Вложенные позиции продуктов
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        # Достаем связанные данные (позиции)
        positions = validated_data.pop('positions')

        # Создаем склад
        stock = super().create(validated_data)

        # Добавляем продукты на склад
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)

        return stock

    def update(self, instance, validated_data):
        # Достаем связанные данные (позиции)
        positions = validated_data.pop('positions')

        # Обновляем склад
        stock = super().update(instance, validated_data)

        # Обновляем или создаем позиции
        for position in positions:
            StockProduct.objects.update_or_create(
                stock=stock,
                product=position['product'],
                defaults={
                    'quantity': position['quantity'],
                    'price': position['price'],
                }
            )

        return stock
