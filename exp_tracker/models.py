from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.user_id


class Wallet(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_id = models.CharField(max_length=10, primary_key=True)
    balance = models.FloatField()

    def __str__(self):
        return self.wallet_id


class Transcation(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    wallet_id = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_type = models.CharField(max_length=10)
    transaction_details = models.TextField()
    transaction_time = models.DateTimeField()

    def __str__(self):
        return str(self.id)
