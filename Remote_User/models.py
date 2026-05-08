from django.db import models

# Create your models here.



class ClientRegister_Model(models.Model):
    username = models.CharField(max_length=30, default="unknown")
    email = models.EmailField(max_length=30, default="unknown")
    password = models.CharField(max_length=10, default="unknown")
    phoneno = models.CharField(max_length=10, default="unknown")
    country = models.CharField(max_length=30, default="unknown")
    state = models.CharField(max_length=30, default="unknown")
    city = models.CharField(max_length=30, default="unknown")


class cardiac_arrest_prediction(models.Model):

    Fid= models.CharField(max_length=3000, default="unknown")
    Age_In_Days= models.CharField(max_length=3000, default="unknown")
    Sex= models.CharField(max_length=3000, default="unknown")
    ChestPainType= models.CharField(max_length=3000, default="unknown")
    RestingBP= models.CharField(max_length=3000, default="unknown")
    RestingECG= models.CharField(max_length=3000, default="unknown")
    MaxHR= models.CharField(max_length=3000, default="unknown")
    ExerciseAngina= models.CharField(max_length=3000, default="unknown")
    Oldpeak= models.CharField(max_length=3000, default="unknown")
    ST_Slope= models.CharField(max_length=3000, default="unknown")
    slp= models.CharField(max_length=3000, default="unknown")
    caa= models.CharField(max_length=3000, default="unknown")
    thall= models.CharField(max_length=3000, default="unknown")
    Prediction= models.CharField(max_length=3000, default="unknown")


class detection_accuracy(models.Model):

    names = models.CharField(max_length=300, default="unknown")
    ratio = models.CharField(max_length=300, default="unknown")

class detection_ratio(models.Model):

    names = models.CharField(max_length=300, default="unknown")
    ratio = models.CharField(max_length=300, default="unknown")



