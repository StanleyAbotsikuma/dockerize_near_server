from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.contrib.auth.hashers import make_password



class UserAuthManager(BaseUserManager):
    def create_user(self, phone_number, password, device_id, email=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required")
        user = self.model(phone_number=phone_number, device_id=device_id, email=email, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, device_id, email=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, device_id, email, **extra_fields)

class UserAuth(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=10, unique=True)
    device_id = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=128)

    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["device_id"]

    objects = UserAuthManager()

    def __str__(self):
        return self.phone_number

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
    
    def save(self, *args, **kwargs):
        # Hash the password before saving the user
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=10,unique=True)
    account = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    place_of_residence = models.CharField(max_length=100)
    ghana_card_number = models.CharField(max_length=20)
    ghana_card_picture = models.ImageField(upload_to='ghana_card_pictures/',default='images/default_ghana_card.jpg')
    photo = models.ImageField(upload_to='user_photos/', default='images/default_user.png')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = f"USER_{str(uuid.uuid4().int)[:8]}"
        super(User, self).save(*args, **kwargs)

class Staff(models.Model):
    staff_id = models.CharField(primary_key=True, max_length=20)
    staff_username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    account = models.ForeignKey(UserAuth, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            self.staff_id = f"STAFF_{str(uuid.uuid4().int)[:8]}"
        super(Staff, self).save(*args, **kwargs)

class Device(models.Model):
    device_id = models.CharField(primary_key=True, max_length=20)
    location_coordinate = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.device_id:
            self.device_id = f"DEVICE_{str(uuid.uuid4().int)[:8]}"
        super(Device, self).save(*args, **kwargs)

class Department(models.Model):
    department_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.department_id:
            self.department_id = f"DEPT_{str(uuid.uuid4().int)[:8]}"
        super(Department, self).save(*args, **kwargs)

class Cases(models.Model):
    case_id = models.CharField(primary_key=True, max_length=20)
    type = models.CharField(max_length=50)
    mode = models.CharField(max_length=50)
    case = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    realtime_updates = models.BooleanField(default=False)
    received_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.case_id:
            self.case_id = f"CASE_{str(uuid.uuid4().int)[:8]}"
        super(Cases, self).save(*args, **kwargs)

class CallLogs(models.Model):
    call_id = models.CharField(primary_key=True, max_length=20)
    from_number = models.CharField(max_length=20)
    duration = models.DurationField()
    received_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    case_id = models.ForeignKey(Cases, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.call_id:
            self.call_id = f"CALL_{str(uuid.uuid4().int)[:8]}"
        super(CallLogs, self).save(*args, **kwargs)

class Messages(models.Model):
    message_id = models.CharField(primary_key=True, max_length=20)
    from_number = models.CharField(max_length=20)
    message = models.TextField()
    type = models.CharField(max_length=50)
    received_by = models.ForeignKey(Staff, on_delete=models.CASCADE)
    case_id = models.ForeignKey(Cases, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.message_id:
            self.message_id = f"MSG_{str(uuid.uuid4().int)[:8]}"
        super(Messages, self).save(*args, **kwargs)

class Modes(models.Model):
    mode_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.mode_id:
            self.mode_id = f"MODE_{str(uuid.uuid4().int)[:8]}"
        super(Modes, self).save(*args, **kwargs)

class Types(models.Model):
    type_id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.type_id:
            self.type_id = f"TYPE_{str(uuid.uuid4().int)[:8]}"
        super(Types, self).save(*args, **kwargs)