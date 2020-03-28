from django.db import models

class ProductSize(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    # TODO
    # Price on sale
    # Regular price
    price = models.DecimalField(max_digits=10, decimal_places=2)
    on_sale = models.BooleanField(default=False)
    size = models.ManyToManyField(ProductSize, blank=True)
    color = models.ManyToManyField(ProductColor, blank=True)

    active = models.BooleanField(default=True)
    delivery_days = models.PositiveIntegerField(blank=True, null=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    end_datetime = models.DateTimeField(blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
