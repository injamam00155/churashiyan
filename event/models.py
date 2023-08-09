from django.db import models
import os
from django.core.files import File
import cloudinary
from django.core.validators import RegexValidator

def get_upload_path(instance, filename):
    # Customize the upload path based on the instance's attributes
    return os.path.join('uploads', 'participants', str(instance.id), filename)

class Participant(models.Model):
    SPOUSE_GOING_CHOICES = (
        ('', '--------------'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    DRIVER_COMING_CHOICES = (
        ('', '--------------'),
        ('Yes', 'Yes'),
        ('No', 'No'),
    )

    GENDER_CHOICES = (
        ('', '--------------'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    TRANSPORT_CHOICES = (
        ('', '--------------'),
        ('launch', 'Launch'),
        ('self', 'Self'),
    )

    PROFESSION_CHOICES = (
        ('', '--------------'),
        ('Service', 'Service'),
        ('Business', 'Business'),
        ('Engineer', 'Engineer'),
        ('Doctor', 'Doctor'),
        ('Lawyer', 'Lawyer'),
        ('Housewife', 'House wife'),
        ('Other', 'Other'),
    )

    BLOOD_GROUP_CHOICES = (
        ('', '--------------'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    )

    PAID_AT_CHOICES = (
        ('', '--------------'),
        ('লায়ন মিজানুর রহমান: 01711-530423', 'লায়ন মিজানুর রহমান: 01711-530423'),
        ('মাহবুবুল হক (মাহবুব): 01762-085059', 'মাহবুবুল হক (মাহবুব): 01762-085059'),
    )

    id_number = models.AutoField(
        primary_key=True, 
        default=0
        )

    name = models.CharField(
        max_length=28
        )
    
    contact_number = models.CharField(
        max_length=20
        )
    
    email = models.EmailField(
        null=True
        )
    
    district = models.CharField(
        max_length=20,
        default=''
        )
    
    school_name = models.CharField(
        max_length=100, 
        default=''
        )
    
    profession = models.CharField(
        max_length=10, 
        choices=PROFESSION_CHOICES, 
        default='',  
        validators=[
            RegexValidator(
                '^(?!-+$).*$',
                message='Profession field is required and should not be just hyphens.'
            )
        ]
        )

    gender = models.CharField(
        max_length=6, 
        choices=GENDER_CHOICES, default='',  
        validators=[
            RegexValidator(
                '^(?!-+$).*$',
                message='Profession field is required and should not be just hyphens.'
            )
        ]
        )
    
    blood_group = models.CharField(
        max_length=3, 
        choices=BLOOD_GROUP_CHOICES, 
        default='',  
        validators=[
            RegexValidator(
                '^(?!-+$).*$',
                message='Blood Group field is required and should not be just hyphens.'
            )
        ]
        )
    spouse_name = models.CharField(
        max_length=28, 
        null=True , 
        blank=True)

    spouse_coming = models.CharField(
        max_length=3, 
        choices=SPOUSE_GOING_CHOICES, 
        default='',  
        validators=[
            RegexValidator(
                '^(?!-+$).*$',
                message='Spouse Coming is required and should not be just hyphens.'
                )
        ]
        )
    
    driver_coming = models.CharField(
        max_length=3, 
        choices=DRIVER_COMING_CHOICES, 
        default='',  
                validators=[
            RegexValidator(
                '^(?!-+$).*$',
                message='Driver Coming is required and should not be just hyphens.'
                )
                ]
        )
    
    participant_image = models.ImageField(
        upload_to='', 
        blank=True
        )

    spouse_image = models.ImageField(
        upload_to='', 
        blank=True
        )
    # paid_via = models.CharField(max_length=20)
    paid_at = models.CharField(
        max_length=35, 
        choices=PAID_AT_CHOICES, 
        default='',  
        validators=[
            RegexValidator(
                '^(?!-+$).*$',
                message='Paid At is required and should not be just hyphens.'
            )
            ]
        )
    
    transaction_id = models.CharField(
        max_length=10, 
        null=True
        )
    amount = models.IntegerField(
        default=1000
        )
    transport = models.CharField(
        max_length=10, 
        choices=TRANSPORT_CHOICES, 
        default='',  
        validators=[
            RegexValidator(
                '^(?!-+$).*$',
                message='Transport field is required and should not be just hyphens.'
                )
                ]
                )
    is_verified = models.BooleanField(
        default=False
        )
    

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Delete the associated pictures from Cloudinary when the instance is deleted
        if self.participant_image:
            cloudinary.uploader.destroy(self.participant_image.name)
        if self.spouse_image:
            cloudinary.uploader.destroy(self.spouse_image.name)
        super(Participant, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.name and self.spouse_coming=='Yes' and self.driver_coming=='Yes':
             self.amount = 2500
        elif self.name and self.spouse_coming=='Yes' and self.driver_coming=='No':
            self.amount = 2000
        elif self.name and self.spouse_coming=='No' and self.driver_coming=='Yes':
             self.amount = 1500
        elif self.name and self.spouse_coming=='No' and self.driver_coming=='No':
            self.amount = 1000
        
        # if self.id_number is None:  # Check if the instance is being saved for the first time
        # Rename participant image
        # if self.participant_image:
        #     ext = os.path.splitext(self.participant_image.name)[1]
        #     self.participant_image.name = f'PP{self.id_number}{ext}'
        #     self.participant_image = f'media/SP{self.id_number}{ext}'
        # # Rename spouse image
        # if self.spouse_image:
        #     ext = os.path.splitext(self.spouse_image.name)[1]
        #     self.spouse_image.name = f'SP{self.id_number}{ext}'
        #     self.spouse_image = f'media/SP{self.id_number}{ext}'
        
        super().save(*args, **kwargs)

