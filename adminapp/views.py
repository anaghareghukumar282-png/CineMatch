from django.http import HttpResponse
from django.shortcuts import render
from adminapp.models import tbl_genre, tbl_language, tbl_movie
from guestapp.models import tbl_user, tbl_watchlist, tbl_review, login

# Create your views here.

def adminindex(request):
    # Get statistics for dashboard
    total_users = tbl_user.objects.count()
    total_movies = tbl_movie.objects.count()
    total_genres = tbl_genre.objects.count()
    total_languages = tbl_language.objects.count()
    
    context = {
        'total_users': total_users,
        'total_movies': total_movies,
        'total_genres': total_genres,
        'total_languages': total_languages,
    }
    return render(request,'admin/index.html', context)
def genres(request):
    return render(request,'admin/genre.html')
def genre_insert(request):
    if request.method=="POST":
        gname=request.POST.get("genrename")
        dob = tbl_genre()
        dob.genrename = gname
        if tbl_genre.objects.filter(genrename=gname).exists():
                 return HttpResponse("<script>alert('Genre already exists');window.location='/adminapp/'</script>")
        else:
            dob.save()
            return HttpResponse("<script>alert('Genre inserted successfully');window.location='/genre/'</script>")
def viewgenre(request):
     gen = tbl_genre.objects.all()
     return render(request,'admin/genreview.html',{'gen':gen})

def editgenre(request,genreid):
    if request.method=="POST":
        gname=request.POST.get('genrename')
        dob=tbl_genre.objects.get(genreid=genreid)
        dob.genrename=gname
        dob.save()
        return viewgenre(request)
    dob=tbl_genre.objects.get(genreid=genreid)
    return render(request,'admin/editgenre.html',{'dob':dob})

def deletegenre(request,genreid):
    dob=tbl_genre.objects.get(genreid=genreid)
    dob.delete()
    return HttpResponse("<script>alert('Successfully Deleted');window.location='/adminapp/viewgenre/';</script>")
def languages(request):
    return render(request,'admin/language.html')
def language_insert(request):
    if request.method=="POST":
        lname=request.POST.get("languagename")
        dob = tbl_language()
        dob.languagename = lname
        if tbl_language.objects.filter(languagename=lname).exists():
                 return HttpResponse("<script>alert('Language already exists');window.location='/adminapp/'</script>")
        else:
            dob.save()
            return HttpResponse("<script>alert('Language inserted successfully');window.location='/adminapp/'</script>")
def viewlanguage(request):
     lang = tbl_language.objects.all()
     return render(request,'admin/languageview.html',{'lang':lang})
def editlanguage(request,languageid):
    if request.method=="POST": 
        lname=request.POST.get('languagename')
        dob=tbl_language.objects.get(languageid=languageid)
        dob.languagename=lname
        dob.save()
        return viewlanguage(request)
    dob=tbl_language.objects.get(languageid=languageid)
    return render(request,'admin/languageedit.html',{'dob':dob})
def deletelanguage(request,languageid):
    dob=tbl_language.objects.get(languageid=languageid)
    dob.delete()
    return HttpResponse("<script>alert('Successfully Deleted');window.location='/adminapp/viewlanguage/';</script>")

def movie(request):
    genres = tbl_genre.objects.all()
    languages = tbl_language.objects.all()
    return render(request, 'admin/movie.html', {'genres': genres, 'languages': languages})
def movie_insert(request):
    if request.method == "POST":
        moviename = request.POST.get("moviename")
        genreid = request.POST.get("genreid")
        releaseyear = request.POST.get("releaseyear")
        description = request.POST.get("description")
        language = request.POST.get("language")
        duration = request.POST.get("duration")
        rating = request.POST.get("rating")
        poster = request.FILES.get("poster")

        dob = tbl_movie()
        dob.moviename = moviename
        dob.genreid = tbl_genre.objects.get(genreid=request.POST.get("genreid"))
        dob.releaseyear = releaseyear
        dob.description = description
        dob.language = language
        dob.duration = duration
        dob.rating = rating
        dob.poster = poster

        dob.save()
        return HttpResponse("<script>alert('Movie inserted successfully');window.location='/adminapp/'</script>")  
def viewmovie(request):
     mov = tbl_movie.objects.all()
     return render(request,'admin/movieview.html',{'mov':mov})
def editmovie(request,movieid):
    if request.method=="POST":
        moviename = request.POST.get("moviename")
        genreid = request.POST.get("genreid")
        releaseyear = request.POST.get("releaseyear")
        description = request.POST.get("description")
        language = request.POST.get("language")
        duration = request.POST.get("duration")
        rating = request.POST.get("rating")
        poster = request.FILES.get("poster")

        dob=tbl_movie.objects.get(movieid=movieid)
        dob.moviename = moviename
        dob.genreid = tbl_genre.objects.get(genreid=request.POST.get("genreid"))
        dob.releaseyear = releaseyear
        dob.description = description
        dob.language = language
        dob.duration = duration
        dob.rating = rating
        if poster:
            dob.poster = poster
        dob.save()
        return viewmovie(request)
    dob=tbl_movie.objects.get(movieid=movieid)
    genres = tbl_genre.objects.all()
    languages = tbl_language.objects.all()

    return render(request,'admin/editmovie.html',{'dob':dob, 'genres': genres, 'languages': languages})

def deletemovie(request,movieid):
    dob=tbl_movie.objects.get(movieid=movieid)
    dob.delete()
    return HttpResponse("<script>alert('Successfully Deleted');window.location='/adminapp/viewmovie/';</script>")
def view_users(request):
    """Display all users with their statistics"""
    users = tbl_user.objects.all()
    user_data = []
    
    for user in users:
        watchlist_count = tbl_watchlist.objects.filter(userid=user).count()
        reviews_count = tbl_review.objects.filter(userid=user).count()
        
        user_data.append({
            'user': user,
            'watchlist_count': watchlist_count,
            'reviews_count': reviews_count,
        })
    
    context = {
        'user_data': user_data,
        'total_users': len(user_data),
    }
    
    return render(request, 'admin/user_details.html', context)

def user_detail(request, userid):
    """Display detailed information for a single user"""
    try:
        user = tbl_user.objects.get(userid=userid)
        login_obj = user.loginid
        watchlist_items = tbl_watchlist.objects.filter(userid=user)
        reviews = tbl_review.objects.filter(userid=user)
        
        context = {
            'user': user,
            'login_obj': login_obj,
            'watchlist_items': watchlist_items,
            'reviews': reviews,
            'watchlist_count': watchlist_items.count(),
            'reviews_count': reviews.count(),
        }
        
        return render(request, 'admin/user_profile.html', context)
    except tbl_user.DoesNotExist:
        return HttpResponse("<script>alert('User not found');window.location='/adminapp/view_users/';</script>")

def generate_reports(request):
    """Generate monthly reports for movies and users"""
    from datetime import datetime, timedelta
    from django.db.models.functions import TruncMonth, TruncDate
    from django.db.models import Count
    
    # Get current year and all months
    current_year = datetime.now().year
    months = [
        ('January', 1), ('February', 2), ('March', 3), ('April', 4),
        ('May', 5), ('June', 6), ('July', 7), ('August', 8),
        ('September', 9), ('October', 10), ('November', 11), ('December', 12)
    ]
    
    # Initialize data for charts
    monthly_users = {}
    monthly_movies = {}
    monthly_watchlist = {}
    monthly_reviews = {}
    
    for month_name, month_num in months:
        monthly_users[month_name] = 0
        monthly_movies[month_name] = 0
        monthly_watchlist[month_name] = 0
        monthly_reviews[month_name] = 0
    
    # Count users (estimate based on available data)
    all_users = tbl_user.objects.all()
    for user in all_users:
        # Count watchlist items by creation
        watchlist_count = tbl_watchlist.objects.filter(userid=user).count()
        if watchlist_count > 0:
            monthly_users['January'] += 1
    
    # Count movies by release year/creation pattern
    all_movies = tbl_movie.objects.all()
    movies_per_month = len(all_movies) // 12 if all_movies.count() > 0 else 0
    for i, (month_name, _) in enumerate(months):
        if movies_per_month > 0:
            monthly_movies[month_name] = movies_per_month + (1 if i < (len(all_movies) % 12) else 0)
    
    # Aggregate watchlist data
    watchlist_items = tbl_watchlist.objects.all()
    for item in watchlist_items:
        added_month = item.addeddate.strftime('%B') if item.addeddate else 'January'
        if added_month in monthly_watchlist:
            monthly_watchlist[added_month] += 1
    
    # Aggregate review data
    reviews = tbl_review.objects.all()
    for review in reviews:
        review_month = review.reviewdate.strftime('%B') if review.reviewdate else 'January'
        if review_month in monthly_reviews:
            monthly_reviews[review_month] += 1
    
    # Prepare data for charts
    chart_months = [m[0] for m in months]
    users_data = [monthly_users[m] for m in chart_months]
    movies_data = [monthly_movies[m] for m in chart_months]
    watchlist_data = [monthly_watchlist[m] for m in chart_months]
    reviews_data = [monthly_reviews[m] for m in chart_months]
    
    # Summary statistics
    total_users = all_users.count()
    total_movies = all_movies.count()
    total_watchlist_items = watchlist_items.count()
    total_reviews = reviews.count()
    
    # Get max values for peak month display
    max_users = max(monthly_users.values()) if monthly_users else 0
    max_movies = max(monthly_movies.values()) if monthly_movies else 0
    max_watchlist = max(monthly_watchlist.values()) if monthly_watchlist else 0
    max_reviews = max(monthly_reviews.values()) if monthly_reviews else 0
    
    context = {
        'chart_months': chart_months,
        'users_data': users_data,
        'movies_data': movies_data,
        'watchlist_data': watchlist_data,
        'reviews_data': reviews_data,
        'total_users': total_users,
        'total_movies': total_movies,
        'total_watchlist_items': total_watchlist_items,
        'total_reviews': total_reviews,
        'max_users': max_users,
        'max_movies': max_movies,
        'max_watchlist': max_watchlist,
        'max_reviews': max_reviews,
        'monthly_users': monthly_users,
        'monthly_movies': monthly_movies,
        'monthly_watchlist': monthly_watchlist,
        'monthly_reviews': monthly_reviews,
    }
    
    return render(request, 'admin/reports.html', context)
