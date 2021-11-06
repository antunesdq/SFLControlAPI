from django.db import models
from django.db.models.base import Model
from django.db.models.fields import CharField
import uuid

# Create your models here.
class User(models.Model):
    fields = ('usr_id', 'usr_nickname', 'usr_email', 'usr_doc','usr_pwd', 'usr_credate',)
    usr_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usr_nickname = models.CharField(max_length= 50)
    usr_email = models.CharField(max_length=50)
    usr_doc = models.IntegerField(unique=True)
    usr_pwd = models.CharField(max_length=15)
    usr_credate = models.DateField()

class Account(models.Model):
    acc_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usr_id = models.ForeignKey(User, on_delete=models.CASCADE)
    acc_credate = models.DateField()
    acc_alias = models.CharField(max_length=25)

class Transaction(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    TRANSACTION_MODEL = [
        (IN, 'Receiving'),
        (OUT, 'Sending'),
    ]
    tra_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    tra_date = models.DateTimeField()
    tra_value = models.DecimalField(max_digits=9, decimal_places=2)
    tra_model = models.CharField(max_length=9, choices=TRANSACTION_MODEL, default=IN)
    mod_name = CharField(max_length=50) # ot sure if this should be something different

class Image(models.Model):
    img_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img_image = models.ImageField()
    img_name = models.CharField(max_length=25)

class Tag(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag_name = models.CharField(max_length=25)
    img_id = models.ForeignKey(Image, on_delete=models.CASCADE)

class Vault(models.Model):
    vau_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete= models.CASCADE)
    vau_value = models.DecimalField(max_digits=9, decimal_places=2)

class Budget(models.Model):
    bud_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete= models.CASCADE)
    bud_value = models.DecimalField(max_digits=9, decimal_places=2)


class Active(models.Model):
    act_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag_id = models.ForeignKey(Tag, on_delete= models.CASCADE)
    act_name = models.CharField(max_length=10)
    img_id = models.ForeignKey(Image, on_delete=models.CASCADE)

class Investment(models.Model):
    inv_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    acc_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    inv_date = models.DateTimeField()
    act_id = models.ForeignKey(Active, on_delete=models.CASCADE)
    inv_qty = models.DecimalField(max_digits=9, decimal_places=2)
    inv_price = models.DecimalField(max_digits=9, decimal_places=2)

class Modal(models.Model):
    mod_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mod_name = models.CharField(max_length=25)
    tag_id = models.ForeignKey(Tag, on_delete= models.CASCADE)