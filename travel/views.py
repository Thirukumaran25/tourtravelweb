from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import re

# Create your views here.

def home(request):
    buses = Vehicle.objects.filter(category='bus')[:4] 
    luxury_cars = Vehicle.objects.filter(category='car')[:4]
    tours = TourPackage.objects.filter(is_active=True)[:4]
    vehicle_models = Vehicle.objects.values_list('name', flat=True).distinct()
    tour_packages = TourPackage.objects.filter(is_active=True).values_list('title', flat=True)

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        pickup_date = request.POST.get('pickup_date')

        if not re.fullmatch(r"[A-Za-z\s]+", name):
            messages.error(request, "Name should contain only letters.")
            return redirect('home')
        if not re.fullmatch(r"\d{10}", phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('home')

        booking_kwargs = {
            'guest_name': name,
            'phone': phone,
            'email': email,
            'pickup_date': pickup_date,
        }

        email_subject = ""
        email_message = ""

        try:
            if form_type == "car":
                vehicle_model_name = request.POST.get('vehicle_model')
                if not pickup_date or not vehicle_model_name:
                    messages.error(request, "Please select a date and vehicle model.")
                    return redirect('home')

                vehicle_instance = Vehicle.objects.get(name=vehicle_model_name)
                booking_kwargs.update({
                    'booking_type': 'rental',
                    'vehicle_model': vehicle_instance
                })

                Booking.objects.create(**booking_kwargs)

                email_subject = f"New Rental Booking from {name}"
                email_message = f"Guest: {name}\nPhone: {phone}\nVehicle: {vehicle_model_name}\nPickup: {pickup_date}"
                messages.success(request, "Your car booking has been submitted!")

            elif form_type == "tour":
                tour_package_name = request.POST.get('tour_package')
                if not pickup_date or not tour_package_name:
                    messages.error(request, "Please select a package and date.")
                    return redirect('home')

                package_instance = TourPackage.objects.get(title=tour_package_name)

                booking_kwargs.update({
                    'booking_type': 'tour',
                    'tour_package': package_instance
                })

                Booking.objects.create(**booking_kwargs)

                email_subject = f"New Tour Booking from {name}"
                email_message = f"Guest: {name}\nPackage: {tour_package_name}\nDate: {pickup_date}"
                messages.success(request, "Your tour booking has been submitted!")


            if email_subject and email_message:
                send_mail(
                    email_subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [settings.ADMIN_EMAIL], 
                    fail_silently=False,
                )

        except (Vehicle.DoesNotExist, TourPackage.DoesNotExist):
            messages.error(request, "The selected item is no longer available.")
        except Exception as e:
            messages.warning(request, "Booking saved but failed to send email notification.")

        return redirect('home')

    context = {
        'buses': buses,
        'luxury_cars': luxury_cars,
        'tours': tours,
        'vehicle_models': vehicle_models,
        'tour_packages': tour_packages,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request,'about.html')

def tour(request):
    packages = TourPackage.objects.filter(is_active=True)
    return render(request,'tour.html',{'packages': packages})


def tour_detail(request, slug):
    package = get_object_or_404(TourPackage, slug=slug)
    related_tours = TourPackage.objects.filter(is_active=True).exclude(id=package.id)[:4]
    return render(request, 'tour_detail.html', {
        'package': package,
        'related_tours': related_tours
    })


def car(request):
    vehicles = Vehicle.objects.all()
    return render(request,'car.html',{'vehicles': vehicles})


def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    related_vehicles = Vehicle.objects.filter(price_tag=vehicle.price_tag).exclude(pk=pk)[:4]
    return render(request, 'car_detail.html', {
                    'vehicle': vehicle,
                    'related_vehicles': related_vehicles
                })


def booking(request):
    categories = Vehicle.objects.values_list('category', flat=True).distinct()
    vehicles = Vehicle.objects.all()
    tour_packages = TourPackage.objects.filter(is_active=True)

    if request.method == "POST":
        form_type = request.POST.get('form_type')
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        city = request.POST.get('city', '').strip()
        message = request.POST.get('message', '').strip()
        pickup_date = request.POST.get('pickup_date') or None


        if not re.fullmatch(r"[A-Za-z\s]+", name):
            messages.error(request, "Name should contain only letters.")
            return redirect('booking')
        if not re.fullmatch(r"\d{10}", phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('booking')
        if not re.fullmatch(r"[A-Za-z\s]+", city):
            messages.error(request, "City should contain only letters.")
            return redirect('booking')

        email_subject = ""
        email_message = ""

        if form_type == "rental":
            vehicle_category = request.POST.get('vehicle_category', '')
            vehicle_model_id = request.POST.get('vehicle_model', '')
            num_person = request.POST.get('num_person') or 1

            if not vehicle_category or not vehicle_model_id:
                messages.error(request, "Please select a vehicle category and model.")
                return redirect('booking')
            vehicle_model = Vehicle.objects.get(id=vehicle_model_id)

            Booking.objects.create(
                booking_type='rental',
                guest_name=name,
                phone=phone,
                email=email,
                city=city,
                message=message,
                pickup_date=pickup_date,
                num_person=num_person,
                vehicle_category=vehicle_category,
                vehicle_model=vehicle_model
            )

            email_subject = f"New Rental Booking from {name}"
            email_message = f"""
                        New Rental Booking Received!

                        Guest Name: {name}
                        Phone: {phone}
                        Email: {email}
                        City: {city}
                        Vehicle Category: {vehicle_category}
                        Vehicle Model: {vehicle_model.price_tag}
                        Number of Persons: {num_person}
                        Pickup Date: {pickup_date if pickup_date else 'Not Provided'}
                        Message: {message if message else 'No message'}
                        """
            messages.success(request, f"Rental enquiry submitted for {vehicle_category}!")
        
        elif form_type == "tour":
            tour_package_id = request.POST.get('tour_package', '')
            if not tour_package_id:
                messages.error(request, "Please select a tour package.")
                return redirect('booking')

            tour_package = TourPackage.objects.get(id=tour_package_id)

            Booking.objects.create(
                booking_type='tour',
                guest_name=name,
                phone=phone,
                email=email,
                city=city,
                message=message,
                pickup_date=pickup_date,
                tour_package=tour_package
            )

            email_subject = f"New Tour Booking from {name}"
            email_message = f"""
                    New Tour Booking Received!

                    Guest Name: {name}
                    Phone: {phone}
                    Email: {email}
                    City: {city}
                    Tour Package: {tour_package.title}
                    Pickup Date: {pickup_date if pickup_date else 'Not Provided'}
                    Message: {message if message else 'No message'}
                    """
            messages.success(request, f"Tour enquiry submitted for {tour_package.title}!")
        
        if email_subject and email_message:   
            try:
                send_mail(
                    email_subject,
                    email_message,
                    settings.EMAIL_HOST_USER,
                    [settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
            except Exception as e:
                messages.warning(request, "Booking saved but failed to send email notification.")

        return redirect('booking')

    context = {
        'categories': categories,
        'vehicles': vehicles,
        'tour_packages': tour_packages,
    }
    return render(request, 'booking.html', context)


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        city = request.POST.get('city')
        message = request.POST.get('message')

        # Backend validation
        if not re.fullmatch(r"[A-Za-z\s]+", name):
            messages.error(request, "Name should contain only letters.")
            return redirect('contact')

        if not re.fullmatch(r"[0-9]{10}", phone):
            messages.error(request, "Phone number must be exactly 10 digits.")
            return redirect('contact')

        if not re.fullmatch(r"[A-Za-z\s]+", city):
            messages.error(request, "City should contain only letters.")
            return redirect('contact')

        # Save to database
        feedback_entry = Feedback.objects.create(
            name=name,
            phone=phone,
            email=email,
            city=city,
            message=message
        )

        subject = f"New Feedback from {name}"
        full_message = f"Name: {name}\nPhone: {phone}\nEmail: {email}\nCity: {city}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
            messages.success(request, "Your message has been successfully submitted!")
        except Exception:
            messages.warning(request, "Saved, but email failed.")

        return redirect('contact')

    return render(request, 'contact.html')


def service(request):
    return render(request,'service.html',)