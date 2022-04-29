from django.shortcuts import render, get_object_or_404
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator

from shop.models import Product, Category


def home(request):
    return render(request, 'shop/home.html')


def product_list(request, page, category_slug=None):
    category = None
    message = None
    categories = Category.objects.all()
    object_list = Product.objects.filter(available=True).all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        object_list = object_list.filter(category=category)

    query = None
    if 'search_field' in request.GET:
        query = request.GET.get('search_field')
        object_list = Product.objects.annotate(
            similarity=TrigramSimilarity('name', query),
        ).filter(similarity__gt=0.1).order_by('-similarity')

    if object_list.count() == 0:
        message = 'Products not available'

    paginator = Paginator(object_list, per_page=10)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page)

    return render(request, 'shop/product_list.html',
                  {'products': page_object, 'categories': categories, 'category': category,
                   'message': message, 'query': query})


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'shop/detail.html', {'product': product})
