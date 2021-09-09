from django.contrib import admin
from .models import *
from .forms import CustomerCreationForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CustomerAdmin(UserAdmin):
    model=Customer
    add_form = CustomerCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Customer Information',
            {
            'fields':(
            'phone_number',
                'avatar',
        )
            }
        )
    )

admin.site.register(Customer,CustomerAdmin)
admin.site.register(Purchaser)
admin.site.register(Feedback)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'product', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
