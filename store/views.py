from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q

from Category.models import Category
from carts.models import CartItem
from carts.views import _cart_id
from store.models import Product, ReviewRating

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from .forms import ReviewForm
from django.contrib import messages


# Create your views here.
def store(request, category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(products, 1)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    context = {'products': paged_products,
               'product_count': product_count
               }
    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):
     try:
         single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
         in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
         
     except Exception as e:
            raise e    
     
     context = {
         'single_product': single_product,
         'in_cart'       : in_cart,
     }
        
     return render(request, 'store/product_detail.html', context)   

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
     }
    return render(request, 'store/store.html', context)

def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            # ✅ If review already exists — update it
            review = ReviewRating.objects.get(user=request.user, product=product)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.')
            else:
                print("❌ FORM ERRORS (update):", form.errors)
                messages.error(request, 'There was a problem submitting your review.')
        except ReviewRating.DoesNotExist:
            # ✅ Otherwise create new review
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                # ✅ match HTML name="rating" (lowercase)
                data.rating = request.POST.get('rating')
                data.ip = request.META.get('REMOTE_ADDR')
                data.product = product
                data.user = request.user
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
            else:
                print("❌ FORM ERRORS (create):", form.errors)
                messages.error(request, 'There was a problem submitting your review.')

        # ✅ Always return a valid response
        return redirect(url)

    # If GET or something else, redirect safely
    return redirect(url)
    url = request.META.get('HTTP_REFERER', '/')  # fallback to home if referer is missing
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            # if review exists — update it
            review = ReviewRating.objects.get(user=request.user, product=product)
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.')
            else:
                messages.error(request, 'There was a problem updating your review.')
        except ReviewRating.DoesNotExist:
            # otherwise create new review
            form = ReviewForm(request.POST)
            if form.is_valid():
                print("✅ FORM VALID")
                data = ReviewRating()
                data.subject = form.cleaned_data.get('subject')
                data.review = form.cleaned_data.get('review')
                # fix field name difference
                data.rating = request.POST.get('Rating')  # ✅ matches HTML input name
                data.ip = request.META.get('REMOTE_ADDR')
                data.product = product
                data.user = request.user
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
            else:
                print("❌ FORM ERRORS:", form.errors)
                messages.error(request, 'There was a problem submitting your review.')

        # ✅ always return a redirect
        return redirect(url)

    # ✅ handle GET request safely
    return redirect(url)

            