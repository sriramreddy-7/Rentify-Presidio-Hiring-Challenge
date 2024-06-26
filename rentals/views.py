from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from rentals.models import Property, UserProfile, PropertyPhoto, Like
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from decouple import config

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        user_type = request.POST.get('user_type')
        
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        user.save()
        user_profile = UserProfile(user=user, phone_number=phone_number, user_type=user_type)
        user_profile.save()
        login(request, user)
        return redirect('index')
    return render(request, 'register/register.html')

def user_login(request):
    if request.method == 'POST':
        username_or_email = request.POST['username_or_email']
        password = request.POST['password']
        user_type = request.POST['user_type']

        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            user = User.objects.filter(username=username_or_email).first()

        if user is not None and user.check_password(password):
            user_profile = UserProfile.objects.get(user=user)
            if user_profile.user_type == user_type:
                login(request, user)
                if user_type == "buyer":
                    return redirect('buyer_dashboard')
                elif user_type == "seller":
                    return redirect('seller_dashboard')
            else:
                return HttpResponse("Invalid user type")
        else:
            return HttpResponse("Invalid login details")
    return render(request, 'login/login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

@login_required
def seller_dashboard(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'seller/seller_dashboard.html', {'properties': properties})

@login_required
def buyer_dashboard(request):
    property_list = Property.objects.all()
    paginator = Paginator(property_list, 10)  

    page = request.GET.get('page')
    try:
        properties = paginator.page(page)
    except PageNotAnInteger:
        properties = paginator.page(1)
    except EmptyPage:
        properties = paginator.page(paginator.num_pages)

    return render(request, 'buyer/buyer_dashboard.html', {'properties': properties})

@login_required
def post_property(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        country = request.POST.get('country')
        state = request.POST.get('state')
        district = request.POST.get('district')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        area = request.POST.get('area')
        bedrooms = request.POST['bedrooms']
        bathrooms = request.POST['bathrooms']
        nearby_hospitals = request.POST['nearby_hospitals']
        nearby_colleges = request.POST['nearby_colleges']
        price = request.POST['price']
        photos = request.FILES.getlist('photos')

        property = Property(
            owner=request.user,
            title=title,
            description=description,
            country=country,
            state=state,
            district=district,
            pincode=pincode,
            city=city,
            area=area,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            nearby_hospitals=nearby_hospitals,
            nearby_colleges=nearby_colleges,
            price=price
        )
        property.save()

        for photo in photos:
            PropertyPhoto.objects.create(property=property, photo=photo)

        return redirect('seller_properties')

    return render(request, 'seller/post_property.html')

@login_required
def seller_properties(request):
    properties = Property.objects.filter(owner=request.user)
    return render(request, 'seller/seller_properties.html', {'properties': properties})

@login_required
def update_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, owner=request.user)

    if request.method == 'POST':
        property.title = request.POST['title']
        property.description = request.POST['description']
        property.country = request.POST.get('country')
        property.state = request.POST.get('state')
        property.district = request.POST.get('district')
        property.pincode = request.POST.get('pincode')
        property.city = request.POST.get('city')
        property.area = request.POST.get('area')
        property.bedrooms = request.POST['bedrooms']
        property.bathrooms = request.POST['bathrooms']
        property.nearby_hospitals = request.POST['nearby_hospitals']
        property.nearby_colleges = request.POST['nearby_colleges']
        property.save()

        return redirect('seller_properties')

    return render(request, 'seller/update_property.html', {'property': property})

@login_required
def delete_property(request, property_id):
    property = get_object_or_404(Property, id=property_id, owner=request.user)
    if request.method == 'POST':
        property.delete()
        return redirect('seller_properties')
    return render(request, 'seller/delete_property.html', {'property': property})

@login_required
def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    return render(request, 'buyer/property_detail.html', {'property': property})

@login_required
def property_filter(request):
    properties = Property.objects.all()

    if 'bedrooms' in request.GET:
        properties = properties.filter(bedrooms=request.GET['bedrooms'])
    if 'bathrooms' in request.GET:
        properties = properties.filter(bathrooms=request.GET['bathrooms'])
    if 'country' in request.GET:
        properties = properties.filter(country=request.GET['country'])
    if 'state' in request.GET:
        properties = properties.filter(state=request.GET['state'])
    if 'district' in request.GET:
        properties = properties.filter(district=request.GET['district'])
    if 'pincode' in request.GET:
        properties = properties.filter(pincode=request.GET['pincode'])
    if 'city' in request.GET:
        properties = properties.filter(city=request.GET['city'])
    if 'area' in request.GET:
        properties = properties.filter(area=request.GET['area'])
    if 'nearby_hospitals' in request.GET:
        properties = properties.filter(nearby_hospitals__icontains=request.GET['nearby_hospitals'])
    if 'nearby_colleges' in request.GET:
        properties = properties.filter(nearby_colleges__icontains=request.GET['nearby_colleges'])
    if 'price' in request.GET:
        properties = properties.filter(price=request.GET['price'])

    return render(request, 'buyer/buyer_dashboard.html', {'properties': properties})

@login_required
def express_interest(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    buyer = request.user
    seller = property.owner

    send_mail(
        'Interest in your property',
        f'Hi {seller.first_name},\n\n{buyer.first_name} {buyer.last_name} is interested in your property: {property.title}.\nYou can contact them at {buyer.email}.',
        config('EMAIL_HOST_USER'),
        [seller.email],
    )

    send_mail(
        'Property details',
        f'Hi {buyer.first_name},\n\nYou expressed interest in the property: {property.title}.\nSeller contact: {seller.email}',
        config('EMAIL_HOST_USER'),
        [buyer.email],
    )

    return render(request, 'buyer/interest_expressed.html', {'property': property})

@login_required
def like_property(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    like, created = Like.objects.get_or_create(property=property, user=request.user)
    if not created:
        like.delete()
    return redirect('buyer_dashboard')
