from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Product, Category

from django.views.generic.base import View

from django.core.paginator import Paginator
from django.db.models import Q

import shop.serializers

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
class ProdList(View):

    # def get(self, request):
    #     return render(request, template_name="sidebar.html")

    def get(self, request):
        # return render(request, template_name="base.html")
        search_query = request.GET.get('search', '')
        
        if search_query:
            product = Product.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
        else:
            product = Product.objects.all()

        paginator = Paginator(product, 20)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        is_paginated = page.has_other_pages()
        
        if page.has_previous():   
            prev_url = '?page={}'.format(page.previous_page_number())
        else:
            prev_url = ''
        
        if page.has_next():
            next_url = '?page={}'.format(page.next_page_number())
        else: 
            next_url = ''

        context = {
            'page_object': page,
            'is_paginated': is_paginated,
            'next_url': next_url,
            'prev_url': prev_url,
        }

        return render(request, template_name="base.html", context=context)


class CategoryProductVue(View):
    """Список товаров из категории для vue"""
    def get(self, request):
        return render(request, "shop/vue/list-product-vue.html")

    def post(self, request):
        slug = request.POST.get("slug")
        node = Category.objects.get(slug=slug)
        if Product.objects.filter(category__slug=slug).exists():
            products = Product.objects.filter(category__slug=slug)
        else:
            products = Product.objects.filter(category__slug__in=[x.slug for x in node.get_family()])

        category_ser = CatSer(Category.objects.filter(parent__isnull=True), many=True)
        serializers = ProductSer(product, many=True)
        return JsonResponse(
            {
                "product": serializers.data,
                "category": category_ser.data
            },
            safe=False)

class SortProducts(View):
    """Фильтр товаров"""
    def get(self, request):
        return render(request, "shop/vue/list-product-vue.html")

    def post(self, request):
        category = request.POST.get("category", None)
        price_1 = request.POST.get("price1", 1)
        price_2 = request.POST.get("price2", 1000000000)
        availability = request.POST.get("availability", None)

        filt = []

        if category:
            cat = Q()
            cat &= Q(category__name__icontains=category)
            filt.append(cat)
        if price_1 or price_2:
            price = Q()
            price &= Q(price__gte=int(price_1)) & Q(price__lte=int(price_2))
            filt.append(price)
        if availability:
            if availability == "False":
                avail = False
            elif availability == "True":
                avail = True
            availability = Q()
            availability &= Q(availability=avail)
            filt.append(availability)
        sort = Product.objects.filter(*filt)

        category_ser = CatSer(Category.objects.filter(parent__isnull=True), many=True)
        serializers = ProductSer(sort, many=True)
        return JsonResponse(
            {
                "products": serializers.data,
                "category": category_ser.data
             },
            safe=False)