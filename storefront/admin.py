from django.contrib import admin
from .models import SiteSettings, Category, Product, Announcement, Testimonial, Enquiry

admin.site.site_header = 'PriNikki Website Manager'
admin.site.site_title = 'PriNikki Admin'
admin.site.index_title = 'Manage your chocolate and gifting website'

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Brand and homepage', {'fields': ('brand_name','tagline','hero_title','hero_subtitle','hero_image','hero_button_text','announcement_bar')}),
        ('Contact details', {'fields': ('phone_number','whatsapp_number','email','address','business_hours','instagram_url','facebook_url')}),
        ('About section', {'fields': ('about_title','about_text')}),
        ('Search engine settings', {'fields': ('seo_title','seo_description')}),
    )
    def has_add_permission(self, request): return not SiteSettings.objects.exists()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','active','sort_order')
    list_editable = ('active','sort_order')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','category','display_price','published','available','featured','badge')
    list_filter = ('published','available','featured','badge','category')
    list_editable = ('published','available','featured')
    search_fields = ('name','short_description','description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at','updated_at')
    fieldsets = (
        ('Product information', {'fields': ('name','slug','category','short_description','description')}),
        ('Images', {'fields': ('image','extra_image_1','extra_image_2')}),
        ('Pricing and merchandising', {'fields': ('price','sale_price','badge','featured','sort_order')}),
        ('Availability and publishing', {'fields': ('available','published','created_at','updated_at')}),
    )

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title','announcement_type','display_location','start_at','end_at','published','priority')
    list_filter = ('published','announcement_type','display_location')
    list_editable = ('published','priority')
    search_fields = ('title','short_description','description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('Announcement content', {'fields': ('title','slug','announcement_type','label','short_description','description','image')}),
        ('Call to action', {'fields': ('button_text','button_url')}),
        ('Publishing and scheduling', {'fields': ('display_location','start_at','end_at','priority','published')}),
    )

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name','occasion','approved','featured','created_at')
    list_filter = ('approved','featured')
    list_editable = ('approved','featured')

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name','phone','email','subject','status','created_at')
    list_filter = ('status','created_at')
    list_editable = ('status',)
    search_fields = ('name','phone','email','subject','message')
    readonly_fields = ('created_at',)
