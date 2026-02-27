from django.db import models

# Create your models here.
class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ('car', 'Luxury Car'),
        ('bus', 'Bus / Traveler'),
        ('van', 'Van'),
    ]

    name = models.CharField(max_length=200, help_text="e.g., 24 Seater Bus or Mercedes S Class")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='car')

    price_tag = models.CharField(max_length=100, default="Luxury Car")
    seat_count = models.CharField(max_length=50, default="4+1")
   
    main_image = models.ImageField(upload_to='vehicles/main/')
    front_image= models.ImageField(upload_to='vehicles/front/', null=True, blank=True)
    side_image = models.ImageField(upload_to='vehicles/side/', null=True, blank=True)
    interior_image = models.ImageField(upload_to='vehicles/interior/', null=True, blank=True)

    has_ac = models.BooleanField(default=True, verbose_name="Has AC")
    has_speaker = models.BooleanField(default=True, verbose_name="Has Speaker System")
    has_tv = models.BooleanField(default=False, verbose_name="Has TV")
    luggage_capacity = models.IntegerField(default=5)

    # Descriptions
    main_description = models.TextField()
    sub_desc_1_content = models.TextField(blank=True)
    sub_desc_2_content = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    

class TourPackage(models.Model):
    title = models.CharField(max_length=200, help_text="e.g., Kashmir Holiday Tour")
    slug = models.SlugField(unique=True, help_text="URL-friendly name (e.g., kashmir-holiday-tour)")
    image = models.ImageField(upload_to='tours/')
    duration_days = models.IntegerField(help_text="Number of days")
    duration_nights = models.IntegerField(help_text="Number of nights")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    overview = models.TextField()
    itinerary = models.TextField(help_text="Detailed day-by-day plan")
    inclusions = models.TextField(help_text="What is included (one per line)")
    exclusions = models.TextField(help_text="What is NOT included")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class Feedback(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Feedback Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"Feedback from {self.name} - {self.city}"


class Booking(models.Model):
    BOOKING_TYPE_CHOICES = [
        ('rental', 'Rental Car'),
        ('tour', 'Tour Package'),
    ]

    booking_type = models.CharField(max_length=10, choices=BOOKING_TYPE_CHOICES)
    guest_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)
    pickup_date = models.DateField(null=True, blank=True)
    num_person = models.PositiveIntegerField(default=1)
    vehicle_category = models.CharField(max_length=50, blank=True, null=True)
    vehicle_model = models.ForeignKey(Vehicle, null=True, blank=True, on_delete=models.SET_NULL)
    tour_package = models.ForeignKey(TourPackage, null=True, blank=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.guest_name} - {self.booking_type}"