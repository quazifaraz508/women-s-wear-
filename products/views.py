from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, Favorite
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Create your views here.

def product_list(request):
    products = Products.objects.all().order_by('-product_bestseller', 'id')
    favorite_products = []
    
    if request.user.is_authenticated:
        favorite_products = Products.objects.filter(favorite__user=request.user)
    else:
        favorite_products = []
        
    return render(request, 'main.html', 
                  {'products':products,
                   'favorite_products': favorite_products,
                   })

def product_detail(request, pk):
    product = get_object_or_404(Products, pk=pk)
    is_favorited = False
    if request.user.is_authenticated:
        is_favorited = Favorite.objects.filter(user=request.user, product=product).exists()

    return render(request, 'product_detail.html', {'product': product, 'is_favorited':is_favorited})


@login_required
def toggle_fav(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Products, id=product_id)
        
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        
        if not created:
            favorite.delete()
            is_favorited = False
        else:
            is_favorited = True
        
        return JsonResponse({'favorited': is_favorited})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def contact(request):
    return render(request, 'contact.html')

def collections(request):
    return render(request, 'collections.html')

@login_required
def product_delete(request, prod_id):
    prod = get_object_or_404(Products, pk = prod_id, )
    if request.method == "POST":
        prod.delete()
        return redirect('product_list')
    return render(request,'confirm_product_delete.html', {'pord': prod})


def favorite_products_view(request):
    if request.user.is_authenticated:
        favorite_products = Products.objects.filter(favorite__user = request.user).order_by('-id')
    else:
        favorite_products = None  # not logged in
    return render(request, 'favorite.html',{'favorite_products':favorite_products})

