from django.db import models
import os
import cloudinary

def get_upload_path(instance, filename):
    # Customize the upload path based on the instance's attributes
    return os.path.join('uploads', 'participants', str(instance.id), filename)

class Participant(models.Model):
    SPOUSE_GOING_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    DRIVER_COMING_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    TRANSPORT_CHOICES = (
        ('launch', 'Launch'),
        ('self', 'Self'),
    )

    PROFESSION_CHOICES = (
        ('Service', 'Service'),
        ('Business', 'Business'),
        ('Engineer', 'Engineer'),
        ('Doctor', 'Doctor'),
        ('Lawyer', 'Lawyer'),
        ('Housewife', 'House wife'),
        ('Other', 'Other'),
    )

    BLOOD_GROUP_CHOICES = (
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
        ('জাকির হোসেন: 01988-691379', 'জাকির হোসেন: 01988-691379'),
        ('লায়ন মিজানুর রহমান: 01711-530423', 'লায়ন মিজানুর রহমান: 01711-530423'),
        ('মাহবুবুল হক (মাহবুব): 01762-085059', 'মাহবুবুল হক (মাহবুব): 01762-085059'),
    )

    id_number = models.AutoField(primary_key=True, default=0)
    name = models.CharField(max_length=28)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(null=True)
    district = models.CharField(max_length=20,default='')
    school_name = models.CharField(max_length=100, default='')
    profession = models.CharField(max_length=10, choices=PROFESSION_CHOICES, default='Service')
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='M')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default= 'B+')
    spouse_name = models.CharField(max_length=28, null=True , blank=True)
    spouse_coming = models.CharField(max_length=3, choices=SPOUSE_GOING_CHOICES, default='N')
    driver_coming = models.CharField(max_length=3, choices=DRIVER_COMING_CHOICES, default='N')
    participant_image = models.ImageField(upload_to='', blank=True)
    spouse_image = models.ImageField(upload_to='', blank=True)
    # paid_via = models.CharField(max_length=20)
    paid_at = models.CharField(max_length=35, choices=PAID_AT_CHOICES, default='আমিরুল ইসলাম মিরন: 01716953986')
    transaction_id = models.CharField(max_length=10, null=True)
    amount = models.IntegerField(default=1000)
    transport = models.CharField(max_length=10, choices=TRANSPORT_CHOICES, default= 'launch')
    is_verified = models.BooleanField(default=False)
    

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
            if self.name and self.spouse_coming=='Y' and self.driver_coming=='Y':
                 self.amount = 2500
            elif self.name and self.spouse_coming=='Y' and self.driver_coming=='N':
                self.amount = 2000
            if self.name and self.spouse_coming=='N' and self.driver_coming=='Y':
                 self.amount = 1500
            elif self.name and self.spouse_coming=='N' and self.driver_coming=='N':
                self.amount = 1000

            if self.id_number is None:  # Check if the instance is being saved for the first time
            # Rename participant image
                if self.participant_image:
                    ext = os.path.splitext(self.participant_image.name)[1]
                    self.participant_image.name = 'PP' + str(self.id_number) + ext

                # Rename spouse image
                if self.spouse_image:
                    ext = os.path.splitext(self.spouse_image.name)[1]
                    self.spouse_image.name = 'SP' + str(self.id_number) + ext

            super().save(*args, **kwargs)

