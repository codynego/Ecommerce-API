from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=50)

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=100)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	description = models.TextField()
	image = models.URLField(max_length=100, null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

	def __str__(self):
		return self.name


class Order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	products = models.ManyToManyField(Product)
	ordered = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username
	
	def get_total(self):
		total = 0
		for product in self.products.all():
			total += product.price
		return total
	
	def get_total_items(self):
		total = 0
		for product in self.products.all():
			total += 1
		return total
	
class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return f"{self.quantity} of {self.product.name}"

	def get_total_item_price(self):
		return self.quantity * self.product.price

	def get_total_discount_item_price(self):
		return self.quantity * self.product.discount_price

	def get_amount_saved(self):
		return self.get_total_item_price() - self.get_total_discount_item_price()

	def get_final_price(self):
		if self.product.discount_price:
			return self.get_total_discount_item_price()
		return self.get_total_item_price()
	