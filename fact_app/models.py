from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Customer(models.Model):
    """
    name : customer model definition
    description : attribute's list of the class customer
    author : francklinngandeu@gmail.com
    """

    SEX_TYPES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )

    name = models.CharField(max_length=132)

    email = models.EmailField()

    phone = models.CharField(max_length=132)

    address = models.CharField(max_length=64)

    sex = models.CharField(max_length=1, choices=SEX_TYPES)

    city = models.CharField(max_length=32)

    zip_code = models.CharField(max_length=16)

    created_date = models.DateTimeField(auto_now_add=True)

    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name


class Invoice(models.Model):
    """
    name: invoice model definition
    description:
    author: francklinngandeu@gmail.com
    """
    INVOICE_TYPE = (
        ('R', _('RECEIPT')),
        ('P', _('PROFORMA INVOICE')),
        ('I', _('INVOICE'))
    )
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    save_by = models.ForeignKey(User, on_delete=models.PROTECT)

    invoice_date_time = models.DateTimeField(auto_now_add=True)

    total = models.DecimalField(max_digits=1000000, decimal_places=2)

    last_update_date = models.DateTimeField(null=True, blank=True)

    paid = models.BooleanField(default=False)

    invoice_type = models.CharField(max_length=1, choices=INVOICE_TYPE)

    comments = models.TextField(null=True, max_length=1000, blank=True)

    class Meta:
        verbose_name = 'Invoice'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        return f"{self.customer.name}_{self.invoice_date_time}"

    @property
    def get_total(self):
        articles = self.article_set.all()
        total = sum(article.get_total for article in articles)
        return total


class Article(models.Model):
    """
    name : article model definition
    description :
    author : francklinngandeu@gmail.com
    """
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)

    name = models.CharField(max_length=32)

    quantity = models.IntegerField()

    unit_price = models.DecimalField(max_digits=1000000, decimal_places=2)

    total = models.DecimalField(max_digits=1000000, decimal_places=2)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    @property
    def get_total(self):
        total = self.quantity * self.unit_price
        return total
