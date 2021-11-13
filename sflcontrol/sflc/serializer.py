from rest_framework import serializers
from django.forms import ModelForm

from sflc.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = User.fields

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = Account.fields

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = Transaction.fields

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = Image.fields

class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = Image.fields
        
class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = Tag.fields

class VaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vault
        fields = Vault.fields

class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = Budget.fields

class ActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Active
        fields = Active.fields

class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = Investment.fields