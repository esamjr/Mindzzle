from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear'),
)

LABEL_CHOICES = (
    ('S', 'primary'),
    ('SW', 'secondary'),
    ('OW', 'danger'),
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    description_item = models.TextField(default="a new product")
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return reverse("core:product", kwargs={"slug": self.slug})


class OrderItem(models.Model):
    username_order_item = models.ForeignKey(settings.AUTH_USER_MODEL,
                                            on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    def get_total_item_price(self):
        """
        get the total item price
        """
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        """
        get the total discount item price
        """
        return self.quantity * self.item.discount_price

    def get_final_price(self):
        """
        get the final price
        """
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    username_order = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    order_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username_order.username} Order'

    def get_total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total