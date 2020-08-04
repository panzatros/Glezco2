from django.db import models
from django.shortcuts import reverse
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.template.defaultfilters import slugify
#pythfrom django_countries.fields import CountryField

class DireccionEntrega(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    calle = models.CharField(max_length=250)
    numeroExterior = models.IntegerField(blank=False)
    numeroInterior = models.IntegerField(default=None)
    colonia = models.CharField(max_length=250)
    codigoPostal = models.IntegerField()
    rfc = models.CharField(max_length=250, blank=True)
    telefono = models.CharField(max_length=250, blank=True)
    slug = models.SlugField(null=False, unique=True)

    def select_direccion(self):
        return reverse("select-Direccion", kwargs={'slug': self.slug})    

    def delete_direccion(self):
        return reverse("delete-addres", kwargs={'slug': self.slug})

    def check_direccion(self):
        return reverse("detalle-addres", kwargs={'slug': self.slug})

    def __str__(self):
        return self.calle + str(self.numeroExterior)

    def Identifier(self):
        identificador = self.calle + ' ' + str(self.numeroExterior)
        if(self.numeroInterior):
            direccion = identificador + ' ' + 'numero interior' + str(self.numeroInterior) + ' ' + self.colonia + ' ' + 'codigo postal: ' + self.codigoPostal
        else:    
            direccion =  identificador + ' ' + self.colonia + ' ' + 'codigo postal: ' + self.codigoPostal
        informacion = {
            'identificador':identificador,
            'direccion':direccion
        }
        return informacion


class productos(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    price = models.FloatField(default=1) #quitar
    image = models.ImageField(upload_to='media/core/images/')
    slug = models.SlugField(null=False, unique=True)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("producto", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("my_form_view_url", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("remove-from-cart", kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        return super().save(*args, **kwargs)

class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(productos, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.titulo}"

    def get_total_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(null=True, blank=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ManyToManyField(DireccionEntrega)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    ordered_date_pedido = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_related_shiping_addres(self):
        return
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        return total


class Perfil(models.Model):
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


