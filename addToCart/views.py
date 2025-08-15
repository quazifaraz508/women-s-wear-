from django.shortcuts import render,redirect, get_object_or_404
from .models import CartItem
from products.models import Products
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, pk=product_id)
    quantity = int(request.POST.get("quantity", 1))

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product
    )

    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity

    cart_item.save()

    # Get updated cart data
    cart_items = CartItem.objects.filter(user=request.user)
    total_items = sum(item.quantity for item in cart_items)
    total_price = sum(item.total_price for item in cart_items)

    items_list = [
        {
            "name": ci.product.product_name,
            "quantity": ci.quantity,
            "price": float(ci.product.product_price),
            "total": float(ci.total_price)
        }
        for ci in cart_items
    ]

    return JsonResponse({
        'message': 'Added to cart',
        'cart_count': total_items,
        'cart_total': float(total_price),
        'cart_items': items_list
    })


@login_required
def cart_summary(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in items)
    return render(request, 'cart_summary.html', {'items': items, 'total': total})


@login_required
def cart_dropdown(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price for item in items)
    return render(request, 'main.html', {'items': items, 'total': total})

from django.views.decorators.http import require_POST

@login_required
def get_cart_data(request):
    items = CartItem.objects.filter(user=request.user)
    total_items = sum(item.quantity for item in items)
    total_price = sum(item.total_price for item in items)

    cart_items = [
        {
            "id": item.id,  # ✅ Include ID
            "name": item.product.product_name,
            "quantity": item.quantity,
            "price": float(item.product.product_price),
            "total": float(item.total_price)
        }
        for item in items
    ]

    return JsonResponse({
        "cart_count": total_items,
        "cart_total": float(total_price),
        "cart_items": cart_items
    })

@require_POST
@login_required
def update_quantity(request, item_id):
    import json
    data = json.loads(request.body)
    action = data.get('action')
    
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if action == 'increase':
        item.quantity += 1
    elif action == 'decrease' and item.quantity > 1:
        item.quantity -= 1
    
    item.save()
    return get_cart_data(request)  # returns JSON


@require_POST
@login_required
def remove_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    return get_cart_data(request)  # ✅ Return updated cart JSON
