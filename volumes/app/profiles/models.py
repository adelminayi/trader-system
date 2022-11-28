from pyexpat import model
from wsgiref.validate import validator
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

from stdimage.validators import MinSizeValidator, MaxSizeValidator
from stdimage.models import StdImageField

from phonenumber_field.modelfields import PhoneNumberField



class Profile(models.Model):
    user                        = models.OneToOneField(settings.AUTH_USER_MODEL,
                                                        on_delete=models.CASCADE, 
                                                        unique=True, 
                                                        related_name="authuserprofile")
    image                       = StdImageField(default='default.png', upload_to='profile_pics', 
                                                        validators=[MinSizeValidator(200, 200), MaxSizeValidator(500, 500)])
    # image                       = models.ImageField(upload_to = 'photos/%Y/%m/%d/', validator )
    dateOfBirth                 = models.DateField(blank=True, null=True)
    address                     = models.CharField(max_length=400, blank=True, null=True, unique=True)
    addressVerified             = models.BooleanField(default=False)
    cellPhoneNumber             = PhoneNumberField(unique=True)
    cellPhoneNumberVerified     = models.BooleanField(default=False)
    landingPhoneNumber          = PhoneNumberField(unique=True, blank=True, null=True)
    landingPhoneNumberVerified  = models.BooleanField(default=False)
    signedContract              = models.BooleanField(default=False, db_index=True)
    payedMemmber                = models.BooleanField(default=False, db_index=True)
    paymentTime                 = models.DateTimeField(auto_now_add=True, db_index=True)
    expirationTime              = models.DateTimeField(auto_now_add=True, db_index=True)
    isEnable                    = models.BooleanField(default=False, db_index=True)
    createTime                  = models.DateTimeField(auto_now_add=True)
    isActive                    = models.BooleanField(default=True, db_index=True)
    totalSL                     = models.FloatField(default=0)

    class Meta:
        db_table    = 'profiles'

    def __str__(self):
        return str(self.user) + " - " + str(self.cellPhoneNumber)

user_model = get_user_model()
