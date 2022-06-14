from django.db import models

from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# ----------> Custom User model and manager --->

class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None
        ):
        if not email:
            raise ValueError('You must have an email address')

        user = self.model(
            email = self.normalize_email(email),
            name = name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password=None):
        user = self.create_user(
            email,
            name=name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address',
                max_length=255,
                unique=True
            )
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin

# --------------------- End of Custom user and its manager ------->


#--------------------- Create cars models -------------------->

class Sacco(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Cars(models.Model):
    sacco = models.ForeignKey(Sacco, on_delete=models.PROTECT, blank=True, null=True)
    plate_name = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=100)
    seats = models.IntegerField()

    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return self.plate_name + self.plate_number


class Route(models.Model):
    departure = models.CharField(max_length=300)
    destination = models.CharField(max_length=300)

    class Meta:
        verbose_name = "Routes"
        verbose_name_plural = "Routes"

    def __str__(self):
        return self.departure + '|' + self.destination


class Schedules(models.Model):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    routes = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    full = models.BooleanField(default=False)
    qrcode = models.ImageField(upload_to='qrcode', null=True, blank=True)

    class Meta:
        verbose_name = "Schedules"
        verbose_name_plural = "Schedules"
    
    def __str__(self):
        return str(str(self.routes) + "  |" + str(self.date))
    
    @property
    def occupied_seats(self):
        boarded = self.schedule.all()
        seats = 0
        for x in boarded:
            seats += x.seats
        return seats

class Passengers(models.Model):
    schedules = models.ForeignKey(Schedules, on_delete=models.PROTECT, related_name='schedule')
    seats = models.IntegerField()
    name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    fare = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    confirm = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Passengers"
        verbose_name_plural = "Passengers"

    def __str__(self):
        return str(self.phone_number)