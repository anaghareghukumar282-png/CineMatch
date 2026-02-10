from django.db import models

# Create your models here.

    
class tbl_genre(models.Model):
    genreid=models.AutoField(primary_key=True)
    genrename=models.CharField(max_length=100)

class tbl_movie(models.Model):
    movieid = models.AutoField(primary_key=True)
    moviename = models.CharField(max_length=100)
    genreid = models.ForeignKey(tbl_genre, on_delete=models.CASCADE, null=True, blank=True)
    releaseyear = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # duration in minutes
    rating = models.FloatField(null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)

    def __str__(self):
        return self.moviename


class tbl_movie_genre(models.Model):
    mgid = models.AutoField(primary_key=True)
    movie = models.ForeignKey(tbl_movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(tbl_genre, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie} - {self.genre}"
    
class tbl_language(models.Model):
    languageid=models.AutoField(primary_key=True)
    languagename=models.CharField(max_length=100)
    iso_639_1 = models.CharField(max_length=10, default='', blank=True)






    
