from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
# from backend.product.views import Resource as ProductsResource

# from backend.customer.models import Customer
# from backend.product.models import *
from backend.cmspage.models import CMS_Page

admin.site.site_header = "Django Testing Administration"


# class CustomersResource(resources.ModelResource):
#     class Meta:
#         model = Customer
#         skip_unchanged = True
#         report_skipped = False
#         exclude = ('created_at', 'updated_at')


# class CustomersAdmin(ImportExportModelAdmin):
#     resource_class = CustomersResource


# admin.site.register(Customer, CustomersAdmin)

# class ProductsAdmin(ImportExportModelAdmin): 
#     resource_class = ProductsResource

# admin.site.register(Products, ProductsAdmin)
admin.site.register(CMS_Page)
# admin.site.register(Variants)
# admin.site.register(Attribute)
# admin.site.register(AttributeValue)
