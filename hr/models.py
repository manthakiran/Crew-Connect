# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Employee(models.Model):

    EMPLOYMENT_TYPES = [
        ("Permanent", "Permanent"), #("database_value", "display_value")
        ("Contract", "Contract"),
        ("Part-time", "Part-time"),
        ("Intern", "Intern"),
    ]

    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True) # for one user have one employee
    employee_id = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.ForeignKey(Department,on_delete=models.PROTECT) # we cannot delete any employees present in this dept
    designation = models.ForeignKey(Designation,on_delete=models.PROTECT)# we cannot delete any employees present in this design
    joining_date = models.DateField()
    employment_type = models.CharField(max_length=20,choices=EMPLOYMENT_TYPES)
    salary = models.DecimalField(max_digits=10,decimal_places=2)
    address = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employee_id} - {self.name}"

class Leave(models.Model):

    LEAVE_TYPES = [
        ("EL", "Earned Leave"),
        ("SL", "Sick Leave"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="leaves"
    )

    leave_type = models.CharField(
        max_length=10,
        choices=LEAVE_TYPES
    )

    start_date = models.DateField()

    end_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    applied_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.employee_id} - {self.leave_type}"


class LeaveBalance(models.Model):

    employee = models.OneToOneField(
        Employee,
        on_delete=models.CASCADE,
        related_name="leave_balance"
    )

    earned_leave = models.PositiveIntegerField(
        default=12
    )

    sick_leave = models.PositiveIntegerField(
        default=8
    )

    def __str__(self):
        return f"{self.employee.employee_id} - Leave Balance"


class Attendance(models.Model):

    STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='attendance'
    )

    date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )

    class Meta:
        unique_together = ('employee', 'date')

    def __str__(self):
        return f"{self.employee} - {self.date} - {self.status}"


class Holiday(models.Model):

    HOLIDAY_TYPES = [
        ("Festival", "Festival"),
        ("National", "National Holiday"),
        ("Public", "Public Holiday"),
        ("Optional", "Optional Holiday"),
    ]

    name = models.CharField(max_length=100)

    date = models.DateField(unique=True)

    holiday_type = models.CharField(
        max_length=20,
        choices=HOLIDAY_TYPES,
        default="Festival"
    )

    description = models.TextField(blank=True)

    state = models.CharField(
        max_length=50,
        default="Andhra Pradesh"
    )

    def __str__(self):
        return f"{self.name} - {self.date}"


