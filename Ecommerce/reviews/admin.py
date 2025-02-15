from django.contrib import admin
from . models import Review

# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('product__name', 'user__email')