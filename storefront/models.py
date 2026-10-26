from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class SiteSettings(models.Model):
    brand_name = models.CharField(max_length=100, default='PriNikki')
    tagline = models.CharField(max_length=180, default='Make every moment sweeter.')
    hero_title = models.CharField(max_length=180, default='A little sweetness. A lot of love.')
    hero_subtitle = models.TextField(default='Thoughtfully crafted chocolates and beautiful gifts for life’s sweetest moments.')
    hero_image = models.ImageField(upload_to='site/', blank=True, null=True)
    hero_button_text = models.CharField(max_length=60, default='Explore the collection')
    phone_number = models.CharField(max_length=40, blank=True, help_text='Include country code for WhatsApp, e.g. 919876543210')
    whatsapp_number = models.CharField(max_length=40, blank=True, help_text='Digits only, including country code, e.g. 919876543210')
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    business_hours = models.CharField(max_length=180, blank=True)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    announcement_bar = models.CharField(max_length=220, blank=True, default='Thoughtful gifts for your sweetest moments')
    about_title = models.CharField(max_length=160, default='Made for moments worth remembering')
    about_text = models.TextField(default='From little celebrations to once-in-a-lifetime milestones, PriNikki helps you share love with thoughtful treats and beautifully presented gifts.')
    seo_title = models.CharField(max_length=180, default='PriNikki | Chocolates & Thoughtful Gifts')
    seo_description = models.CharField(max_length=300, default='Discover premium chocolates, birthday gifts and beautiful gift hampers from PriNikki.')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self): return 'PriNikki website settings'
    class Meta: verbose_name = 'Website settings'; verbose_name_plural = 'Website settings'

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.CharField(max_length=240, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)
    class Meta: ordering = ['sort_order', 'name']; verbose_name_plural = 'Categories'
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name

class Product(models.Model):
    BADGE_CHOICES = [('none','No badge'),('new','New arrival'),('bestseller','Bestseller'),('featured','Featured')]
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    short_description = models.CharField(max_length=260, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    extra_image_1 = models.ImageField(upload_to='products/gallery/', blank=True, null=True)
    extra_image_2 = models.ImageField(upload_to='products/gallery/', blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    sale_price = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, default='none')
    available = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ['sort_order', '-created_at']
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    def __str__(self): return self.name
    @property
    def display_price(self): return self.sale_price if self.sale_price is not None else self.price

class Announcement(models.Model):
    TYPES = [('new','New product'),('hamper','Gift hamper'),('birthday','Birthday gift'),('festival','Festival collection'),('offer','Special offer'),('coming','Coming soon'),('general','General announcement')]
    LOCATIONS = [('bar','Top announcement bar'),('home','Homepage feature'),('both','Bar and homepage')]
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    announcement_type = models.CharField(max_length=20, choices=TYPES, default='general')
    short_description = models.CharField(max_length=260, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)
    label = models.CharField(max_length=40, blank=True, help_text='For example: Coming Soon')
    button_text = models.CharField(max_length=60, blank=True)
    button_url = models.CharField(max_length=400, blank=True)
    display_location = models.CharField(max_length=10, choices=LOCATIONS, default='home')
    start_at = models.DateTimeField(default=timezone.now)
    end_at = models.DateTimeField(blank=True, null=True)
    priority = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-priority', '-start_at']
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    def is_live(self):
        now = timezone.now()
        return self.published and self.start_at <= now and (self.end_at is None or self.end_at >= now)
    def __str__(self): return self.title

class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    text = models.TextField()
    occasion = models.CharField(max_length=100, blank=True)
    approved = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-featured', '-created_at']
    def __str__(self): return f'{self.customer_name} testimonial'

class Enquiry(models.Model):
    STATUS = [('new','New'),('contacted','Contacted'),('closed','Closed')]
    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    subject = models.CharField(max_length=180, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ['-created_at']
    def __str__(self): return f'{self.name} — {self.subject or "Enquiry"}'
