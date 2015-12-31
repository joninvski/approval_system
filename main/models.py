from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class VendorInformation(models.Model):
    name = models.CharField(max_length=200)
    address_first = models.CharField(max_length=200)
    address_second = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    st = models.CharField(max_length=200)
    zip = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    fax = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    quantity = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return "%d - %s %s" % (self.quantity, self.description, self.unit_price)

    def total_price(self):
        return self.quantity * self.unit_price

class PaymentMethod(models.Model):
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.description


class Approver(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Requester(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Approval(models.Model):
    time = models.DateTimeField()
    user = models.ForeignKey(Approver)
    TYPE_CHOICES = (
        ('n', 'no'),
        ('-', 'pending'),
        ('y', 'yes'),
    )
    approved = models.CharField(max_length=1, choices=TYPE_CHOICES, default='-')

    def __str__(self):
        return str(self.user) + " " + str(self.approved)

    def is_approved(self):
        if self.approved == u'n':
            return 'rejected'
        if self.approved == u'-':
            return 'pending'
        if self.approved == u'y':
            return 'approved'

class ApprovalPriority(models.Model):
    user = models.ForeignKey(Approver)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user) + " " + str(self.priority)

class WorkflowTemplate(models.Model):
    name = models.CharField(max_length=200)
    approval_list = models.ManyToManyField(ApprovalPriority)

    def __str__(self):
        return str(self.name)

class Order(models.Model):
    number = models.CharField(max_length=200)
    vendor = models.ForeignKey(VendorInformation)
    payment_method = models.ForeignKey(PaymentMethod)
    workflow_template = models.ForeignKey(WorkflowTemplate)
    time = models.DateTimeField()
    requester = models.ForeignKey(Requester)
    items = models.ManyToManyField(Item)
    business_purpose = models.CharField(max_length=200)
    closed = models.BooleanField(default=False)
    approvals = models.ManyToManyField(Approval)

    def __str__(self):
        return str(self.number) + " " + str(self.vendor)

    def my_approval(self, user):
        for approval in self.approvals.all():
            if approval.user.user == user:
                return approval

    def total_price(self):
        price = 0

        for item in self.items.all():
            price += item.total_price()
        return price
