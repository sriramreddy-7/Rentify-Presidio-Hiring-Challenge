# core/models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15) 
    user_type=models.CharField(max_length=15,default="None")

    def __str__(self):
        return self.user.username

class Property(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=100,default="Your Default Country")  
    state = models.CharField(max_length=100,default="Your Default State")    
    district = models.CharField(max_length=100,default="Your Default District") 
    pincode = models.CharField(max_length=10,default="Your Default Pincode")   
    city = models.CharField(max_length=255,default="Your Default City")     
    area = models.CharField(max_length=255,default="Your Default Area") 
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    nearby_hospitals = models.TextField()
    nearby_colleges = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.FloatField(default=0)

    def __str__(self):
        return self.title


class PropertyPhoto(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='property_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.property.title} - Photo"
    
class Like(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)