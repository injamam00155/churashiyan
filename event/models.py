from django.db import models

class Participant(models.Model):
    DRIVER_COMING_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )

    GENDER_CHOICES = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    TRANSPORT_CHOICES = (
        ('launch', 'Launch'),
        ('bus', 'Bus'),
    )

    PROFESSION_CHOICES = (
        ('service', 'Service'),
        ('business', 'Business'),
        ('engineer', 'Engineer'),
        ('doctor', 'Doctor'),
        ('lawyer', 'Lawyer'),
        ('housewife', 'House wife'),
        ('other', 'Other'),
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

    id_number = models.AutoField(primary_key=True, default=0)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    district = models.CharField(max_length=100,null=True)
    school_name = models.CharField(max_length=100, default=True)
    profession = models.CharField(max_length=100, choices=PROFESSION_CHOICES, default='other')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default= 'B+')
    spouse_name = models.CharField(max_length=100, null=True)
    driver_coming = models.CharField(max_length=3, choices=DRIVER_COMING_CHOICES, default='N')
    participant_image = models.ImageField(upload_to='participant_images/', blank=True)
    spouse_image = models.ImageField(upload_to='spouse_images/', blank=True)
    # paid_via = models.CharField(max_length=20)
    # paid_at = models.PositiveIntegerField()
    transaction_id = models.CharField(max_length=50, null=True)
    amount = models.DecimalField(max_digits=8, decimal_places=0, default=0)
    transport = models.CharField(max_length=6, choices=TRANSPORT_CHOICES, default= 'launch')

    def __str__(self):
        return self.name
