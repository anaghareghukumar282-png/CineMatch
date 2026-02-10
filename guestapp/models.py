from django.db import models

from adminapp.models import tbl_movie

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

class tbl_community(models.Model):
    communityid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    community_type = models.CharField(max_length=50, choices=[
        ('General', 'General'),
        ('Genre-based', 'Genre-based'),
        ('Movie-based', 'Movie-based'),
    ])
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    member_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    related_genre = models.ForeignKey('adminapp.tbl_genre', on_delete=models.SET_NULL, null=True, blank=True)
    related_movie = models.ForeignKey('adminapp.tbl_movie', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class tbl_community_member(models.Model):
    memberid = models.AutoField(primary_key=True)
    community = models.ForeignKey(tbl_community, on_delete=models.CASCADE)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, default='member')  # New field for role (admin/member)
    # Note: is_admin field not in existing database table

    def __str__(self):
        return f"{self.user.username} in {self.community.name}"

class tbl_community_message(models.Model):
    messageid = models.AutoField(primary_key=True)
    community = models.ForeignKey(tbl_community, on_delete=models.CASCADE)
    sender = models.ForeignKey(tbl_user, db_column='sender_id', on_delete=models.CASCADE)
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    message_type = models.CharField(max_length=50, default='text')  # must not be null
    related_movie = models.ForeignKey(tbl_movie, db_column='related_movie_id', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Message by {self.sender.username} in {self.community.name}"