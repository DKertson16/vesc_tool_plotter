from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Foil(models.Model):
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', null=True, max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'foils'

class Board(models.Model):
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', null=True, max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'boards'

class Motor(models.Model):
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', null=True, max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'motors'

class Propeller(models.Model):
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', null=True, max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'propellers'

class Controller(models.Model):
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', null=True, max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'controllers'

class Battery(models.Model):
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', null=True, max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'batteries'

class Remote(models.Model):
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', null=True, max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'remotes'

class Build(models.Model):
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', null=True, max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='build')
    date_added = models.DateField('date uploaded', False, True) # Automatically sets
    foil = models.ForeignKey(Foil, on_delete=models.CASCADE, null=True, related_name='build')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True, related_name='build')
    motor = models.ForeignKey(Motor, on_delete=models.CASCADE, null=True, related_name='build')
    propeller = models.ForeignKey(Propeller, on_delete=models.CASCADE, null=True, related_name='build')
    controller = models.ForeignKey(Controller, on_delete=models.CASCADE, null=True, related_name='build')
    battery = models.ForeignKey(Battery, on_delete=models.CASCADE, null=True, related_name='build')
    remote = models.ForeignKey(Remote, on_delete=models.CASCADE, null=True, related_name='build')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'builds'

# Ride data for V 0.1
class Ride(models.Model):
    rider = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='ride')
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description', null=True, max_length=200)
    ride_date = models.DateField('Date')
    location = models.CharField('Location', null=True, max_length=50)
    build = models.ForeignKey(Build, models.SET_NULL, null=True, related_name='ride')
    pub_date = models.DateField('date uploaded', False, True) # Automatically sets
    file = models.FileField(null=True);
    name = models.CharField('file name',null=True, max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'rides'


class CsvRow(models.Model):
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='row')
    ms_today = models.IntegerField()
    input_voltage = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    temp_mos_max = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    current_motor = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    current_in = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    erpm = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    duty_cycle = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    amp_hours_used = models.DecimalField(max_digits=14, decimal_places=4, null=True)
    watt_hours_used = models.DecimalField(max_digits=14, decimal_places=4, null=True)

    def getAllFields(self):
        return [str(self.ms_today), str(self.input_voltage), str(self.temp_mos_max), str(self.current_motor), str(self.current_in), str(self.erpm), str(self.duty_cycle), str(self.amp_hours_used), str(self.watt_hours_used)]
