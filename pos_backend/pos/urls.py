from django.urls import path
from . import views

urlpatterns = [
    path('receipt/<int:sale_id>/', views.generate_receipt, name='generate_receipt'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('add_stock/<int:product_id>/', views.add_stock, name='add_stock'),
    path('api/products/', views.product_list, name='product-list'),  # Corrected here
    path('api/sales/', views.SaleView.as_view(), name='create-sale'),  # ✅ Access SaleView like this
    path('api/sales/list/', views.SaleListView.as_view(), name='sales-list'),  # Get for fetching sales
]
