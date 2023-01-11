from django.db import models
from django.contrib.auth.models import User,AbstractBaseUser,UserManager
from PIL import Image

# Create your models here.
class Users(AbstractBaseUser):
    username = models.CharField(max_length=100,unique=True)
    email = models.CharField(max_length=90)
    bio = models.TextField(max_length=100,blank=True)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=150)
    profile_pic = models.ImageField(upload_to='images/')

    USERNAME_FIELD = 'username'

    @property
    def is_staff(self):
        return self.is_admin

    objects = UserManager()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (20, 20)
            img.thumbnail(new_img)
            img.save(self.avatar.path)