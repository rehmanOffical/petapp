from django.db import models

# Create your models here.
class Appuser(models.Model):
    id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=500,null=False)
    last_name=models.CharField(max_length=500,null=False)
    country=models.CharField(max_length=500,null=False)
    email=models.CharField(max_length=500,null=False)
    phone_no=models.CharField(max_length=500,null=False)
    password=models.CharField(max_length=500,null=False)
    created_at=models.DateTimeField(null=True)
    updated_at=models.DateTimeField(null=True)
    login_at=models.DateTimeField(null=True)
    logout_at=models.DateTimeField(null=True)
    profile_img=models.ImageField(upload_to='profile_pic/',null=True)
    role_id=models.ForeignKey('Role',on_delete=models.CASCADE,default=2)
class logout(models.Model):
    access_token=models.CharField(max_length=500,null=False)
    user_id=models.ForeignKey(Appuser,on_delete=models.CASCADE)

class category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500,null=False)
    image=models.ImageField(upload_to='category')

class userpet(models.Model):
    id=models.AutoField(primary_key=True)
    images=models.JSONField(default=list)
    name=models.CharField(max_length=500,null=False)
    age=models.CharField(max_length=500,null=False,default=1)
    breed=models.CharField(max_length=500,null=False,default="Original")
    sex=models.CharField(max_length=500,null=False,default="Male")
    price=models.IntegerField(null=True)
    status=models.CharField(max_length=500,null=True,default="Sale")
    location=models.CharField(max_length=500,null=False)
    address=models.CharField(max_length=500,null=False)
    whatsapp_no=models.CharField(max_length=500,null=False)
    description=models.CharField(max_length=500,null=True)
    created_at=models.DateTimeField(null=True)
    updated_at=models.DateTimeField(null=True)
    deleted_at=models.DateTimeField(null=True)
    delete=models.BooleanField(default=False)
    categ_id=models.ForeignKey(category,on_delete=models.CASCADE)
    user_id=models.ForeignKey(Appuser,on_delete=models.CASCADE)


class Favourite(models.Model):
    id=models.AutoField(primary_key=True)
    status=models.BooleanField(null=True)
    pet_id=models.ForeignKey(userpet,on_delete=models.CASCADE)
    user_id=models.ForeignKey(Appuser,on_delete=models.CASCADE)

class Find_Lost_Pet(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500,null=True)
    images=models.JSONField(default=list)
    age=models.CharField(max_length=500,null=True)
    categ_id=models.ForeignKey(category,on_delete=models.CASCADE)
    breed=models.CharField(max_length=500,null=True)
    sex=models.CharField(max_length=500,null=True)
    color=models.CharField(max_length=500,null=True)
    identity_mark=models.CharField(max_length=500,null=True)
    status=models.CharField(max_length=500,null=True)
    person_name=models.CharField(max_length=500,null=False)
    address=models.CharField(max_length=500,null=True)
    location=models.CharField(max_length=500,null=True)
    phone_no=models.CharField(max_length=500,null=True)
    description=models.CharField(max_length=500,null=True)
    created_at=models.DateTimeField(null=True)
    updated_at=models.DateTimeField(null=True)
    delete=models.BooleanField(default=False,null=True)
    user_id=models.ForeignKey(Appuser,on_delete=models.CASCADE)

class Animal_Shellter(models.Model):
    id=models.AutoField(primary_key=True)
    house_name=models.CharField(max_length=500,null=True)
    capacity=models.CharField(max_length=500,null=True)
    current_occupancy=models.CharField(max_length=500,null=True)
    address=models.CharField(max_length=500,null=True)
    location=models.CharField(max_length=500,null=True)
    email=models.CharField(max_length=500,null=True)
    owner_name=models.CharField(max_length=500,null=True)
    phone_no=models.CharField(max_length=500,null=True)
    created_at=models.DateTimeField(null=True)
    updated_at=models.DateTimeField(null=True)
    user_id=models.ForeignKey(Appuser,on_delete=models.CASCADE)
    delete=models.BooleanField(null=True,default=False)

class Role(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500,null=True)

class Vet_Clinic(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500,null=True)
    address=models.CharField(max_length=500,null=True)
    location=models.CharField(max_length=500,null=True)
    email=models.CharField(max_length=500,null=True)
    phone_no=models.CharField(max_length=500,null=True)
    owner_name=models.CharField(max_length=500,null=True)
    country=models.CharField(max_length=500,null=True)
    created_at=models.DateTimeField(null=True)
    updated_at=models.DateTimeField(null=True)
    delete=models.BooleanField(default=False)
    user_id=models.ForeignKey(Appuser,on_delete=models.CASCADE)
    
class fcm_token(models.Model):
    id=models.AutoField(primary_key=True)
    token=models.CharField(max_length=500,null=True)
    enable=models.BooleanField(null=True)
    user_id=models.ForeignKey(Appuser,on_delete=models.CASCADE)
    
class POST_ADD(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255,null=False)
    desc=models.TextField(null=True)
    images=models.JSONField(default=list)
    user_id=models.ForeignKey(Appuser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_created=True,null=True)
    updated_at=models.DateTimeField(auto_created=True,null=True)
    
class Favourite_Profile(models.Model):
    id=models.AutoField(primary_key=True)
    status=models.BooleanField(null=True)
    user_id=models.ForeignKey(Appuser,on_delete=models.CASCADE)
    favourite_by=models.CharField(max_length=255,null=True)
    
class Sub_Category(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=500,null=True)
    image=models.ImageField(null=True,upload_to='sub_category')
    categ_id=models.ForeignKey(category,on_delete=models.CASCADE)