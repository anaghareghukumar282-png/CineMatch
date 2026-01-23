from django.db import models

# Create your models here  
class login(models.Model):
    loginid=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    usertype=models.CharField(max_length=100)
    def __str__(self):
        return self.username
    
class tbl_user(models.Model):
    userid=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    loginid=models.ForeignKey(login,on_delete=models.CASCADE)
    def __str__(self):
        return self.guestname

class tbl_watchlist(models.Model):
    watchid=models.AutoField(primary_key=True)
    moviename=models.CharField(max_length=100)
    addeddate=models.DateField()
    userid=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    movieid=models.ForeignKey('adminapp.tbl_movie',on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return self.moviename
    
class tbl_feedback(models.Model):
    feedbackid=models.AutoField(primary_key=True)
    subject=models.CharField(max_length=100)
    message=models.TextField()
    response=models.TextField()
    date=models.DateField()
    userid=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    def __str__(self):
        return self.message

class tbl_userpreference(models.Model):
    preferenceid=models.AutoField(primary_key=True)
    weight=models.CharField(max_length=100)
    genreid=models.ForeignKey('adminapp.tbl_genre',on_delete=models.CASCADE)
    userid=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    def __str__(self):
        return self.weight
    
class tbl_recommendationlog(models.Model):
    recommendationid=models.AutoField(primary_key=True)
    recommendeddate=models.DateField()
    score=models.CharField(max_length=100)
    movieid=models.ForeignKey('adminapp.tbl_movie',on_delete=models.CASCADE)
    userid=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    def __str__(self):
        return self.movieid
    
class tbl_review(models.Model):
    reviewid=models.AutoField(primary_key=True)
    rating=models.CharField(max_length=100)
    reviewtext=models.TextField()
    reviewdate=models.DateField()
    movieid=models.ForeignKey('adminapp.tbl_movie',on_delete=models.CASCADE)
    userid=models.ForeignKey(tbl_user,on_delete=models.CASCADE)
    def __str__(self):
        return self.reviewtext