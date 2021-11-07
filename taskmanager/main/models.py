from django.db import models
from PIL import ImageFile
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Manga(models.Model):
    manga=models.CharField(max_length=100)
    cover = models.ImageField(upload_to='templates/photo',default=True,blank=True)
    price=models.IntegerField(verbose_name='Цена')
    description=models.CharField(max_length=1000)

    def __str__(self):
        return self.manga


    class Meta:
        verbose_name='Book'
        verbose_name_plural = 'Books'


class Order(models.Model):
    STATUS_NEW='new'
    STATUS_IN_PROGRESS='in_progress'
    STATUS_READY='is_ready'
    STATUS_COMPLETED='completed'

    BUYING_TYPE_SELF='self'
    BUYING_TYPE_DELIVERY='delivery'


    STATUS_CHOICES=(
        (STATUS_NEW,'Новый заказ'),
        (STATUS_IN_PROGRESS,"Заказ в обработке"),
        (STATUS_READY,'Заказ готов'),
        (STATUS_COMPLETED,'Заказ получен покупателем')
    )

    BUYING_TYPE_CHOICES=(
        (BUYING_TYPE_SELF,'Самовывоз'),
        (BUYING_TYPE_DELIVERY,'Доставка')
    )

    customer = models.ForeignKey('Customer',verbose_name='Покупатель',related_name='orders',on_delete=models.CASCADE)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=1024,null=True,blank=True)
    status=models.CharField(max_length=100,choices=STATUS_CHOICES,default=STATUS_NEW)
    buying_type=models.CharField(max_length=100,choices=BUYING_TYPE_CHOICES)
    created_at=models.DateField(auto_now=True)
    order_date=models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name='Order'
        verbose_name_plural='Orders'

class Customer(models.Model):

    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    is_active=models.BooleanField(default=True)
    customer_orders=models.ManyToManyField(
        Order,blank=True,related_name='related_customer')
    wishlist=models.ManyToManyField(Manga,blank=True)
    phone=models.CharField(max_length=20)


    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name='Buyer'
        verbose_name_plural='Buyers'


class CartProduct(models.Model):
    user=models.ForeignKey('Customer',on_delete=models.CASCADE)
    cart=models.ForeignKey('Cart',on_delete=models.CASCADE)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id=models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type','object_id')
    qty=models.PositiveIntegerField(default=1)
    final_price=models.DecimalField(max_digits=9,decimal_places=2)

    def __str__(self):
        return f"Manga:{self.content_object.name} (for a cart)"


    def save(self,*args,**kwargs):
        self.final_price=self.qty*self.content_object.price
        super().save(*args,**kwargs)

    class Meta:
        verbose_name='Продукт корзины'
        verbose_name_plural='Продукты корзины'

class Cart(models.Model):
    owner=models.ForeignKey('Customer',on_delete=models.CASCADE,null=True)
    products=models.ManyToManyField(CartProduct,blank=True,related_name='related_cart')
    total_products=models.IntegerField(default=0)
    final_price=models.DecimalField(max_digits=9,decimal_places=2,null=True,blank=True)
    in_order=models.BooleanField(default=False)
    for_anonymous_user=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name='Cart'
        verbose_name_plural='Carts'