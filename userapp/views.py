from django.template.context_processors import request

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from adminapp.models import tbl_genre, tbl_language, tbl_movie, tbl_movie_genre
from guestapp.models import tbl_community_message, tbl_userpreference, tbl_user, tbl_watchlist, tbl_review, tbl_recommendationlog, tbl_community, tbl_community_member

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

    paginator = Paginator(movies, 20)  # Show 20 movies per page
    page_number = request.GET.get('page')

    try:
        movies_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        movies_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        movies_page = paginator.page(paginator.num_pages)
    
    # Get genres and languages for filter sidebar
    genres = tbl_genre.objects.all()
    languages = tbl_language.objects.all()
    
    context = {
        'movies': movies_page,
        'genres': genres,
        'languages': languages,
        'selected_genre': genre_id,
        'selected_language': language,
        'total_movies': paginator.count,
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
    
def account(request):
    """Display user account settings page"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    try:
        from guestapp.models import login
        login_obj = login.objects.get(loginid=request.session['loginid'])
        user = tbl_user.objects.get(loginid=login_obj)
        
        context = {
            'user': user,
        }
        
        return render(request, 'user/account.html', context)
    
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
        genres = tbl_genre.objects.all()
        
        # Get user from session
        login_obj = login.objects.get(loginid=request.session['loginid'])
        user = tbl_user.objects.get(loginid=login_obj)
        
        # Get user's watchlist items
        watchlist_items = tbl_watchlist.objects.filter(userid=user).order_by('-addeddate')
        
        context = {
            'user': user,
            'watchlist_items': watchlist_items,
            'total_items': watchlist_items.count(),
            'genres': genres,
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

def view_community(request):
    """Display community forum page"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    # Get current user
    from guestapp.models import login
    login_obj = login.objects.get(loginid=request.session['loginid'])
    user = tbl_user.objects.get(loginid=login_obj)
    
    genres = tbl_genre.objects.all()
    movies = tbl_movie.objects.all()
    communities = tbl_community.objects.filter(is_active=True).order_by('-created_date')
    
    # Add membership info to each community
    for community in communities:
        if community.created_by == user:
            community.user_is_member = True
        else:
            community.user_is_member = tbl_community_member.objects.filter(
                community=community, 
                user=user
            ).exists()
    
    context = {
        'genres': genres,
        'movies': movies,
        'communities': communities,
    }
    
    return render(request, 'user/community.html', context)

def create_community(request):
    """Create a new community"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    if request.method == 'POST':
        try:
            # Get the current user
            from guestapp.models import login
            login_obj = login.objects.get(loginid=request.session['loginid'])
            user = tbl_user.objects.get(loginid=login_obj)
            
            # Create the community
            community = tbl_community.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                community_type=request.POST.get('community_type'),
                created_by=user,
                related_genre_id=request.POST.get('related_genre_id') if request.POST.get('related_genre_id') else None,
                related_movie_id=request.POST.get('related_movie_id') if request.POST.get('related_movie_id') else None,
            )
            
            # Add the creator as a member and admin
            tbl_community_member.objects.create(
                community=community,
                user=user
                # Note: is_admin field not available in existing database
            )
            
            # Update member count
            community.member_count = 1
            community.save()
            
            return redirect('view_community')
            
        except Exception as e:
            # Handle errors - could add error messages here
            print(f"Error creating community: {e}")
            return redirect('view_community')
    
    return redirect('view_community')

def join_community(request, community_id):
    """Join a community"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    try:
        # print("Joining Community ID:", community_id)
        # Get the current user
        from guestapp.models import login
        login_obj = login.objects.get(loginid=request.session['loginid'])
        user = tbl_user.objects.get(loginid=login_obj)

        # print("User ID:------------------", user.userid)
        
        # Get the community
        community = tbl_community.objects.get(communityid=community_id, is_active=True)
        
        # Check if user is already a member
        if not tbl_community_member.objects.filter(community_id=community_id, user_id=user.userid).exists():
            # Add user as member
            tbl_community_member.objects.create(
                user_id=user.userid,
                community_id=community_id,
                role='member'  # Default role as member
            )
            
            # Update member count
            community.member_count += 1
            community.save()
        # return "User joined community successfully"
        
        return redirect('community_chat', community_id=community_id)
        
    except Exception as e:
        print(f"Error joining community: {e}")
        return redirect('view_community')

def community_chat(request, community_id):
    """Display community chat page"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    try:
        # Get the current user
        from guestapp.models import login
        login_obj = login.objects.get(loginid=request.session['loginid'])
        user = tbl_user.objects.get(loginid=login_obj)
        
        # Get the community
        community = tbl_community.objects.get(communityid=community_id, is_active=True)
        
        # Check if user is a member
        is_member = tbl_community_member.objects.filter(community=community, user=user).exists()
        if not is_member:
            return redirect('view_community')
        
        # Get messages
        from guestapp.models import tbl_community_message
        messages = tbl_community_message.objects.filter(community=community).order_by('sent_date')
        
        # Get member info
        member_info = tbl_community_member.objects.filter(community=community).select_related('user')
        
        context = {
            'community': community,
            'messages': messages,
            'member_info': member_info,
            'current_user': user,
        }
        
        return render(request, 'user/community_chat.html', context)
        
    except Exception as e:
        print(f"Error loading community chat: {e}")
        return redirect('view_community')

def send_community_message(request, community_id):
    """Send a message to community chat"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    if request.method == 'POST':
        try:
            # Get the current user
            print("Sending message to Community ID:", community_id)
            from guestapp.models import login
            login_obj = login.objects.get(loginid=request.session['loginid'])
            user = tbl_user.objects.get(loginid=login_obj)
            
            # Get the community
            community = tbl_community.objects.get(communityid=community_id, is_active=True)
            
            # Check if user is a member
            if not tbl_community_member.objects.filter(community=community, user=user).exists():
                return redirect('view_community')
            
            # Create message
            from guestapp.models import tbl_community_message
            message_text = request.POST.get('message', '').strip()
            print("-----------------Message Text:", message_text)
            if message_text:
                tbl_community_message.objects.create(
                    community=community,
                    sender=user,
                    message=message_text,
                    message_type='text',  # Default message type as text
                    related_movie_id=request.POST.get('related_movie_id') if request.POST.get('related_movie_id') else None
                )
            
            return redirect('community_chat', community_id=community_id)
            
        except Exception as e:
            print(f"Error sending message: {e}")
            return redirect('community_chat', community_id=community_id)
    
    return redirect('view_community')

def view_discussions(request):
    """Display discussions page"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    return render(request, 'user/discussions.html')

def new_discussion(request):
    """Display new discussion creation page"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    return render(request, 'user/new_discussion.html')

def discussion_detail(request, discussion_id):
    """Display detailed view of a specific discussion"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    return render(request, 'user/discussion_detail.html', {'discussion_id': discussion_id})   

def change_password(request):
    """Handle user password change"""
    if 'loginid' not in request.session:
        return redirect('loginhome')
    
    if request.method == 'POST':
        try:
            from guestapp.models import login
            
            # Get user from session
            login_obj = login.objects.get(loginid=request.session['loginid'])
            
            current_password = request.POST.get('current_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Verify current password
            if login_obj.password != current_password:
                return redirect('account')  # Add error message handling as needed
            
            # Check if new password and confirm password match
            if new_password != confirm_password:
                return redirect('account')  # Add error message handling as needed
            
            # Update password
            login_obj.password = new_password
            login_obj.save()
            
            return redirect('account')  # Add success message handling as needed
        
        except login.DoesNotExist:
            return redirect('loginhome')
    
    return redirect('account')