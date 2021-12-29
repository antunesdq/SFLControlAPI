from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.fields import CharField, UUIDField
import uuid

# Create your models here.
class User(models.Model):
    fields = ('usr_id', 'usr_nickname', 'usr_email', 'usr_doc','usr_pwd', 'usr_credate',)
    usr_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usr_nickname = models.CharField(max_length= 50)
    usr_email = models.CharField(max_length=50)
    usr_doc = models.IntegerField(unique=True)
    usr_pwd = models.CharField(max_length=15)
    usr_credate = models.DateField(auto_now_add=True)

class Image(models.Model):
    fields = ('img_name', 'img_image')
    img_name = models.CharField(max_length=50, primary_key=True, default="TestImageName")
    img_image = models.ImageField(blank=True)
    
class Tag(models.Model):
    fields = ('tag_name', 'tag_type', 'img_name', 'tag_colour')
    tag_name = models.CharField(max_length=25, primary_key=True)
    tag_type = models.CharField(max_length=25, blank=True)
    img_name = models.ForeignKey(Image, on_delete=models.CASCADE)
    tag_colour = models.CharField(max_length=7, default='#8CBF26')

class Account(models.Model):
    fields = ('acc_id', 'usr_id', 'acc_credate', 'acc_refday', 'acc_alias', 'tag_name')
    acc_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usr_id = models.ForeignKey(User, on_delete=models.CASCADE)
    acc_credate = models.DateField(auto_now_add=True)
    acc_refday = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(28)])
    acc_alias = models.CharField(max_length=25)
    tag_name = models.ForeignKey(Tag, on_delete=models.CASCADE)

class Transaction(models.Model):
    fields = ('tra_id', 'acc_id', 'tra_date', 'tra_value', 'tra_name', 'tag_name', 'tra_type')
    tra_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    tra_date = models.DateTimeField()
    tra_value = models.DecimalField(max_digits=9, decimal_places=2)
    tra_name = models.CharField(max_length=25)
    tag_name = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='_tra_pair')
    tra_type = models.CharField(max_length=25)



class Vault(models.Model):
    fields = ('vau_id', 'acc_id', 'tag_id', 'vau_value')
    vau_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    img_name = models.CharField(max_length=25)
    vau_value = models.DecimalField(max_digits=9, decimal_places=2)

class Budget(models.Model):
    fields = ('bud_id', 'acc_id', 'tag_name', 'bud_value')
    bud_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    bud_value = models.DecimalField(max_digits=9, decimal_places=2)
    tag_name = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='_bud_pair')
class Active(models.Model):
    fields = ('act_id', 'act_name', 'img_name')
    act_id = models.CharField(max_length=10, primary_key=True)
    act_name = models.CharField(max_length=50)
    img_name = models.CharField(max_length=25)

class Investment(models.Model):
    fields = ('inv_id', 'acc_id', 'inv_date', 'act_id', 'inv_qty', 'inv_price')
    inv_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    inv_date = models.DateTimeField()
    act_id = models.ForeignKey(Active, on_delete=models.CASCADE)
    inv_qty = models.IntegerField()
    inv_price = models.DecimalField(max_digits=9, decimal_places=2)
