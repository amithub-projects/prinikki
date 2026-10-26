from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .models import Product, Category, Announcement, Testimonial, Enquiry, SiteSettings


def live_announcements():
    now = timezone.now()
    return Announcement.objects.filter(published=True, start_at__lte=now).filter(Q(end_at__isnull=True) | Q(end_at__gte=now))

def home(request):
    products = Product.objects.filter(published=True, available=True)
    featured = products.filter(Q(featured=True) | Q(badge='featured'))[:8]
    if not featured: featured = products[:8]
    categories = Category.objects.filter(active=True)[:8]
    announcements = live_announcements().filter(display_location__in=['home','both'])[:3]
    testimonials = Testimonial.objects.filter(approved=True, featured=True)[:3]
    return render(request, 'storefront/home.html', {'featured_products': featured, 'categories': categories, 'announcements': announcements, 'testimonials': testimonials})

def product_list(request):
    qs = Product.objects.filter(published=True, available=True).select_related('category')
    query = request.GET.get('q','').strip()
    category = request.GET.get('category','').strip()
    if query: qs = qs.filter(Q(name__icontains=query) | Q(short_description__icontains=query) | Q(description__icontains=query))
    if category: qs = qs.filter(category__slug=category)
    sort = request.GET.get('sort','newest')
    if sort == 'price_low': qs = qs.order_by('sale_price','price')
    elif sort == 'price_high': qs = qs.order_by('-sale_price','-price')
    elif sort == 'name': qs = qs.order_by('name')
    else: qs = qs.order_by('-created_at')
    page_obj = Paginator(qs, 12).get_page(request.GET.get('page'))
    return render(request, 'storefront/products.html', {'page_obj': page_obj, 'categories': Category.objects.filter(active=True), 'query': query, 'selected_category': category, 'sort': sort})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, published=True, available=True)
    related = Product.objects.filter(published=True, available=True).exclude(pk=product.pk)
    if product.category_id: related = related.filter(category=product.category)
    return render(request, 'storefront/product_detail.html', {'product': product, 'related_products': related[:4]})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, active=True)
    page_obj = Paginator(Product.objects.filter(category=category, published=True, available=True), 12).get_page(request.GET.get('page'))
    return render(request, 'storefront/category.html', {'category': category, 'page_obj': page_obj})

def announcement_list(request):
    return render(request, 'storefront/announcements.html', {'announcements': live_announcements().filter(display_location__in=['home','both'])})

def announcement_detail(request, slug):
    announcement = get_object_or_404(live_announcements(), slug=slug)
    return render(request, 'storefront/announcement_detail.html', {'announcement': announcement})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name','').strip()
        phone = request.POST.get('phone','').strip()
        email = request.POST.get('email','').strip()
        subject = request.POST.get('subject','').strip()
        message_text = request.POST.get('message','').strip()
        if not name or not message_text:
            messages.error(request, 'Please enter your name and message.')
        else:
            Enquiry.objects.create(name=name, phone=phone, email=email, subject=subject, message=message_text)
            messages.success(request, 'Thank you! Your message has been received. We will get back to you soon.')
            return redirect('contact')
    return render(request, 'storefront/contact.html')

def about(request): return render(request, 'storefront/about.html')
