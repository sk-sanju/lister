from django.db import models

class ShoppingItem(models.Model):
    sl_no = models.IntegerField(unique=True)  # Serial number for the item
    category = models.CharField(max_length=100)  # Category of the grocery item
    product_name = models.CharField(max_length=200)  # Name of the product
    quantity = models.IntegerField(default=1)  # Quantity selected by the user
    
    def __str__(self):
        return f"{self.product_name} ({self.quantity})"