
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from adminapp.models import tbl_genre, tbl_language, tbl_movie, tbl_movie_genre
from guestapp.models import tbl_userpreference, tbl_user, tbl_watchlist, tbl_review, tbl_recommendationlog

# Create your views here.
def userhome(request):
    genres = tbl_genre.objects.all()
    languages = tbl_language.objects.all()
    context = {
        'genres': genres,
        'languages': languages,
    }
    return render(request,'user/index.html', context)

def browse_movies(request):
    """Display movies filtered by genre and language preferences"""
    genre_id = request.GET.get('genre', '')
    language = request.GET.get('language', '')
    
    # Get all movies
    movies = tbl_movie.objects.all()
    
    # Filter by genre if selected
    if genre_id:
        movies = movies.filter(genreid_id=genre_id)
    
    # Filter by language if selected
    if language:
        movies = movies.filter(language__icontains=language)
    
    # Get genres and languages for filter sidebar
    genres = tbl_genre.objects.all()
    languages = tbl_language.objects.all()
    
    context = {
        'movies': movies,
        'genres': genres,
        'languages': languages,
        'selected_genre': genre_id,
        'selected_language': language,
        'total_movies': movies.count(),
    }
    
    return render(request, 'user/browse_movies.html', context)

def profile(request):
    """Display user profile with detailed information"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    try:
        # Get user from login session
        from guestapp.models import login
        login_obj = login.objects.get(loginid=request.session['loginid'])
        user = tbl_user.objects.get(loginid=login_obj)
        
        # Get user statistics
        watchlist_count = tbl_watchlist.objects.filter(userid=user).count()
        reviews_count = tbl_review.objects.filter(userid=user).count()
        recommendations_count = tbl_recommendationlog.objects.filter(userid=user).count()
        
        # Get user preferences
        try:
            user_pref = tbl_userpreference.objects.filter(userid=user).first()
            preferred_genres = []
            preferred_languages = []
            
            if user_pref:
                if hasattr(user_pref, 'preferred_genres') and user_pref.preferred_genres:
                    preferred_genres = user_pref.preferred_genres.split(',')
                if hasattr(user_pref, 'preferred_languages') and user_pref.preferred_languages:
                    preferred_languages = user_pref.preferred_languages.split(',')
        except:
            user_pref = None
            preferred_genres = []
            preferred_languages = []
        
        context = {
            'user': user,
            'watchlist_count': watchlist_count,
            'reviews_count': reviews_count,
            'recommendations_count': recommendations_count,
            'user_preferences': user_pref,
            'preferred_genres': preferred_genres,
            'preferred_languages': preferred_languages,
        }
        
        return render(request, 'user/profile.html', context)
    
    except (tbl_user.DoesNotExist, login.DoesNotExist):
        return redirect('loginhome')

def preferences(request):
    """Display genre and language selection preferences page"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    genres = tbl_genre.objects.all()
    languages = tbl_language.objects.all()
    
    context = {
        'genres': genres,
        'languages': languages,
    }
    return render(request, 'user/preferences.html', context)


def save_preferences(request):
    """Save user preferences for genres and languages"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    if request.method == 'POST':
        try:
            from guestapp.models import login
            
            # Get user from session
            login_obj = login.objects.get(loginid=request.session['loginid'])
            user = tbl_user.objects.get(loginid=login_obj)
            
            # Get selected genres and languages from the form
            selected_genres = request.POST.getlist('genres')
            selected_languages = request.POST.getlist('languages')
            
            # Get or create user preference object
            try:
                user_pref = tbl_userpreference.objects.filter(userid=user).first()
                if not user_pref:
                    user_pref = tbl_userpreference.objects.create(userid=user)
            except tbl_userpreference.DoesNotExist:
                user_pref = tbl_userpreference.objects.create(userid=user)
            
            # Save preferences
            if selected_genres:
                user_pref.preferred_genres = ','.join(selected_genres)
            if selected_languages:
                user_pref.preferred_languages = ','.join(selected_languages)
            
            user_pref.save()
            
            # Redirect back to preferences page with success message
            return redirect('preferences')
        except (tbl_user.DoesNotExist, login.DoesNotExist):
            return redirect('loginhome')
    
    return redirect('preferences')

def add_to_watchlist(request, movie_id):
    """Add a movie to user's watchlist"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    try:
        from guestapp.models import login
        from datetime import date
        
        # Get user from session
        login_obj = login.objects.get(loginid=request.session['loginid'])
        user = tbl_user.objects.get(loginid=login_obj)
        
        # Get movie
        try:
            movie = tbl_movie.objects.get(movieid=movie_id)
        except tbl_movie.DoesNotExist:
            return redirect('browse_movies')
        
        # Check if movie is already in watchlist
        if tbl_watchlist.objects.filter(userid=user, movieid=movie).exists():
            # Movie already in watchlist, redirect to watchlist
            return redirect('view_watchlist')
        
        # Add movie to watchlist
        watchlist_item = tbl_watchlist.objects.create(
            moviename=movie.moviename,
            addeddate=date.today(),
            userid=user,
            movieid=movie
        )
        
        return redirect('view_watchlist')
    
    except (tbl_user.DoesNotExist, login.DoesNotExist) as e:
        return redirect('loginhome')
    except Exception as e:
        print(f"Error adding to watchlist: {str(e)}")
        return redirect('browse_movies')

def view_watchlist(request):
    """Display user's watchlist"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    try:
        from guestapp.models import login
        
        # Get user from session
        login_obj = login.objects.get(loginid=request.session['loginid'])
        user = tbl_user.objects.get(loginid=login_obj)
        
        # Get user's watchlist items
        watchlist_items = tbl_watchlist.objects.filter(userid=user).order_by('-addeddate')
        
        context = {
            'user': user,
            'watchlist_items': watchlist_items,
            'total_items': watchlist_items.count(),
        }
        
        return render(request, 'user/watchlist.html', context)
    
    except (tbl_user.DoesNotExist, login.DoesNotExist):
        return redirect('loginhome')

def remove_from_watchlist(request, watch_id):
    """Remove a movie from user's watchlist"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    try:
        from guestapp.models import login
        
        # Get user from session
        login_obj = login.objects.get(loginid=request.session['loginid'])
        user = tbl_user.objects.get(loginid=login_obj)
        
        # Get watchlist item
        watchlist_item = tbl_watchlist.objects.get(watchid=watch_id, userid=user)
        watchlist_item.delete()
        
        return redirect('view_watchlist')
    
    except (tbl_user.DoesNotExist, login.DoesNotExist, tbl_watchlist.DoesNotExist):
        return redirect('loginhome')