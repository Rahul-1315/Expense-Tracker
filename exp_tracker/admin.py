from django.contrib import admin
from exp_tracker.models import User, Transcation, Wallet
# Register your models here.
admin.site.register(User)
admin.site.register(Wallet)
admin.site.register(Transcation)
