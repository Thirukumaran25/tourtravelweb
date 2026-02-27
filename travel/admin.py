from django.contrib import admin
from .models import *

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name','category', 'price_tag', 'seat_count', 'has_ac', 'has_tv')
    list_filter = ('price_tag', 'has_ac', 'has_tv')
    search_fields = ('name',)
    fieldsets = (
        ('General Information', {
            'fields': ('name','category', 'price_tag', 'seat_count', 'luggage_capacity')
        }),
        ('Media (Images)', {
            'fields': ('main_image','front_image','side_image', 'interior_image'),
            'description': 'Upload high-quality images for the detail page slider.'
        }),
        ('Vehicle Features', {
            'fields': ('has_ac', 'has_tv', 'has_speaker'),
            'classes': ('collapse',),
        }),
        ('Main Description', {
            'fields': ('main_description',)
        }),
        ('Sub Descriptions (Expandable Sections)', {
            'fields': (
                 'sub_desc_1_content', 
                 'sub_desc_2_content'
            )
        }),
    )


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'duration_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)
    
    # Automatically creates the URL slug as you type the title
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Tour Basics', {
            'fields': ('title', 'slug', 'image', 'is_active')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration_days', 'duration_nights')
        }),
        ('Content & Itinerary', {
            'fields': ('overview', 'itinerary', 'inclusions', 'exclusions')
        }),
    )



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'email', 'phone', 'created_at')
    list_filter = ('created_at', 'city')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'phone', 'email', 'city', 'message', 'created_at')



@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'booking_type', 'phone', 'pickup_date', 'created_at')
    list_filter = ('booking_type', 'pickup_date', 'created_at')
    search_fields = ('guest_name', 'phone', 'email', 'city')