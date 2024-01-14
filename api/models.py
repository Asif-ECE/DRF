from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission


# Our custom user model for authentication
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Adding unique related_name attributes
    groups = models.ManyToManyField(
        Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='customuser_set', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


# Our regular models
class Category(models.Model):
    name = models.CharField(max_length=100)
    itemsAvailable = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.itemsAvailable}"

    @property
    def on_sale(self):
        return f"We have {self.itemsAvailable} items on sale."


class Product(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, db_constraint=False)

    def save(self, *args, **kwargs):
        self.category.itemsAvailable += 1
        self.category.save()
        super(Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        print("Deleting product:", self.id)
        if self.category:
            print("Category exists:", self.category.id)
            self.category.itemsAvailable -= 1
            self.category.save()
        super(Product, self).delete(*args, **kwargs)
        print("Product deleted successfully.")

    def __str__(self):
        return f"{self.id} | {self.name} | {self.category.name}"


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
