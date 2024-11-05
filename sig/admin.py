from django.contrib import admin
from .models import Department, Municipality, User, Category, UserCategory

# Register your models here.
admin.site.register(Department)
admin.site.register(Municipality)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(UserCategory)