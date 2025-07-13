import graphene
from .models import Product

class ProductType(graphene.ObjectType):
    name = graphene.String()
    stock = graphene.Int()

class UpdateLowStockProducts(graphene.Mutation):
    products = graphene.List(ProductType)
    success = graphene.Boolean()

    def mutate(self, info):
        products = Product.objects.filter(stock__lt=10)
        updated = []
        for p in products:
            p.stock += 10
            p.save()
            updated.append(p)
        return UpdateLowStockProducts(products=updated, success=True)

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
