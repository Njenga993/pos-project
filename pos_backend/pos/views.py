from django.http import JsonResponse
from django.shortcuts import render
from .models import Sale, Product, SaleItem
from django.http import HttpResponse
import datetime
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SaleSerializer

# Corrected function-based view for listing products
@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@require_http_methods(["GET", "POST"])
def add_stock(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity'))
            if quantity > 0:
                product.stock += quantity
                product.save()
                messages.success(request, f'Successfully added {quantity} units to {product.name}.')
            else:
                messages.error(request, 'Please enter a positive quantity.')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid quantity.')

        return redirect('inventory')

    return render(request, 'pos/add_stock.html', {'product': product})

def generate_receipt(request, sale_id):
    sale = Sale.objects.get(id=sale_id)
    items = sale.saleitem_set.all()

    # Calculate total amount, VAT (16%), and change
    total_amount = 0
    for item in items:
        total_amount += item.total_price  # Using the total price from SaleItem

    vat = total_amount * Decimal('0.16')
    total_with_vat = total_amount + vat
    change = Decimal(sale.amount_rendered) - total_with_vat

    # Create the receipt HTML
    receipt_html = f"""
    <html>
    <body>
        <div style="text-align: center;">
            <h1>Store Name</h1>
            <p>1234 Store St.<br>City, Country<br>Tel: 123-456-7890</p>
        </div>
        
        <div>
            <h2>Receipt for Sale #{sale.id}</h2>
            <p>Date: {sale.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <table border="1" style="width: 100%; margin: 20px 0;">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Adding products to the receipt
    for item in items:
        receipt_html += f"""
        <tr>
            <td>{item.product.name}</td>
            <td>{item.quantity}</td>
            <td>${item.product.price}</td>
            <td>${item.total_price}</td>
        </tr>
        """

    receipt_html += f"""
        </tbody>
    </table>

    <div>
        <p><strong>Subtotal:</strong> ${total_amount}</p>
        <p><strong>VAT (16%):</strong> ${vat}</p>
        <p><strong>Total Amount:</strong> ${total_with_vat}</p>
        <p><strong>Amount Rendered:</strong> ${sale.amount_rendered}</p>
        <p><strong>Change:</strong> ${change}</p>
    </div>

    <div style="text-align: center; margin-top: 20px;">
        <p>Served by: {sale.server.get_full_name()}</p> <!-- Updated here -->
        <p>Thank you for shopping with us!</p>
    </div>
    </body>
    </html>
    """

    return HttpResponse(receipt_html)

def sales_report(request):
    # Default filters (last 30 days)
    start_date = timezone.now() - timedelta(days=30)
    end_date = timezone.now()
    product_filter = None

    # Get filter data from the request
    if request.GET.get('start_date'):
        start_date = timezone.datetime.strptime(request.GET['start_date'], '%Y-%m-%d')
    if request.GET.get('end_date'):
        end_date = timezone.datetime.strptime(request.GET['end_date'], '%Y-%m-%d')
    if request.GET.get('product'):
        product_filter = request.GET['product']

    # Get sales in the date range
    sales = Sale.objects.filter(timestamp__gte=start_date, timestamp__lte=end_date)

    if product_filter:
        # Filter by product if a product is selected
        sales = sales.filter(saleitem__product__name=product_filter)

    total_sales = sum([sale.total_amount for sale in sales])

    # Get the list of products for the filter
    products = Product.objects.all()

    context = {
        'sales': sales,
        'total_sales': total_sales,
        'products': products,
        'start_date': start_date,
        'end_date': end_date,
        'product_filter': product_filter,
    }

    return render(request, 'pos/sales_report.html', context)

def inventory_view(request):
    products = Product.objects.all()
    return render(request, 'pos/inventory.html', {'products': products})

# API endpoint to get products
def get_products(request):
    products = Product.objects.all()
    product_data = [
        {"id": product.id, "name": product.name, "price": product.price, "stock": product.stock}
        for product in products
    ]
    return JsonResponse(product_data, safe=False)

# API endpoint to create a sale
@csrf_exempt
def create_sale(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        product = Product.objects.get(id=product_id)
        if product.stock >= quantity:
            # Create the sale
            sale = Sale.objects.create(
                customer_name="Customer",  # You can customize this field
                total_amount=product.price * quantity,
                amount_rendered=product.price * quantity,  # Modify as needed
                change=0,
            )

            # Create SaleItem
            sale_item = SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                total_price=product.price * quantity,
            )

            # Update product stock
            product.stock -= quantity
            product.save()

            return JsonResponse({"message": "Sale created successfully"}, status=201)

        else:
            return JsonResponse({"error": "Not enough stock available"}, status=400)


class SaleView(APIView):
    def post(self, request):
        serializer = SaleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # New SaleListView for GET
class SaleListView(APIView):
    def get(self, request, *args, **kwargs):
        sales = Sale.objects.all()
        serializer = SaleSerializer(sales, many=True)
        return JsonResponse(serializer.data, safe=False)