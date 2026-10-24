from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=50)


class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    picture = models.URLField(
        max_length=200,
        default='https://www.google.com/imgres?q=restaurant%20images&imgurl=https%3A%2F%2Fassets.architecturaldigest.in%2Fphotos%2F67c55d02484735032005928d%2F4%3A3%2Fw_1440%2Ch_1080%2Cc_limit%2Fcover%2520image%2520template.jpg&imgrefurl=https%3A%2F%2Fwww.architecturaldigest.in%2Fstory%2Fa-new-restaurant-in-jaipurs-city-palace-the-sarvato-dives-into-rajasthans-culinary-traditions%2F&docid=PNSEJFrhpaNGsM&tbnid=OAmoPr6vVHx75M&vet=12ahUKEwjUksX1_u-WAxUSjeEIHTexPFsQnPAOegQIRhAA..i&w=1440&h=1080&hcb=2&ved=2ahUKEwjUksX1_u-WAxUSjeEIHTexPFsQnPAOegQIRhAA'
    )
    cuisine = models.CharField(max_length=200)
    rating = models.FloatField()


class Item(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    vegeterian = models.BooleanField(default=False)
    picture = models.URLField(
        max_length=400,
        default='https://www.indiafilings.com/learn/wp-content/uploads/2024/08/How-to-Start-Food-Business.jpg'
    )


class Cart(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE
    )

    items = models.ManyToManyField(
        Item,
        blank=True
    )

    def total_price(self):
        return sum(item.price for item in self.items.all())


# =========================================================
# ORDER HISTORY
# =========================================================

class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    items = models.ManyToManyField(
        Item,
        blank=True
    )

    total_price = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    payment_status = models.CharField(
        max_length=20,
        default='Paid'
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username}"