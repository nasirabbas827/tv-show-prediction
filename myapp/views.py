from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import Show, Comment
from .forms import CommentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Show, Comment
from .forms import CommentForm , ProfileForm
from .models import Profile 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import sentiwordnet as swn
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')   
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to your dashboard or desired URL
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    # Retrieve all shows from the database
    shows = Show.objects.all()

    # Calculate ranking for each show based on sentiment analysis of comments
    ranked_shows = []
    for show in shows:
        comments = Comment.objects.filter(show=show)
        if comments.exists():
            # Perform sentiment analysis and calculate average sentiment score for the show
            total_sentiment_score = sum(comment.sentiment_score for comment in comments)
            average_sentiment_score = total_sentiment_score / comments.count()
            ranked_shows.append({
                'show': show,
                'average_sentiment_score': average_sentiment_score
            })

    # Sort the ranked shows based on average sentiment score (descending order)
    ranked_shows.sort(key=lambda x: x['average_sentiment_score'], reverse=True)

    # Check if there are any messages
    messages_list = messages.get_messages(request)
    shows = Show.objects.all()

    return render(request, 'dashboard.html', {'shows': shows, 'ranked_shows': ranked_shows, 'messages_list': messages_list})


@login_required
def comment_show(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    user = request.user

    existing_comment = Comment.objects.filter(show=show, user=user).exists()

    if existing_comment:
        messages.warning(request, "You have already commented on this show.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = user
            comment.show = show
            comment.save()

            # Perform sentiment analysis using SentiWordNet
            lemmatizer = WordNetLemmatizer()
            tokenized_text = word_tokenize(comment.text)
            pos_score = 0
            neg_score = 0

            for word in tokenized_text:
                lemma = lemmatizer.lemmatize(word)
                senti_synsets = list(swn.senti_synsets(lemma))
                if senti_synsets:
                    # Use the average positive and negative scores of all synsets for the word
                    pos_score += sum(s.pos_score() for s in senti_synsets) / len(senti_synsets)
                    neg_score += sum(s.neg_score() for s in senti_synsets) / len(senti_synsets)

            # Calculate the overall sentiment score
            sentiment_score = pos_score - neg_score

            # Determine sentiment label based on sentiment score
            if sentiment_score > 0:
                sentiment_label = 'Positive'
            elif sentiment_score < 0:
                sentiment_label = 'Negative'
            else:
                sentiment_label = 'Neutral'

            # Save sentiment score and label to the comment
            comment.sentiment_score = sentiment_score
            comment.sentiment_label = sentiment_label
            comment.save()

            messages.success(request, "Your comment has been successfully submitted.")
            return redirect('dashboard')
    else:
        form = CommentForm()

    return render(request, 'comment_show.html', {'show': show, 'form': form})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Comment, Profile

@login_required
def view_comments(request, show_id):
    show_comments = Comment.objects.filter(show_id=show_id)
    comments_with_user_info = []

    for comment in show_comments:
        user_profile = get_object_or_404(Profile, user=comment.user)
        comments_with_user_info.append({
            'comment': comment,
            'username': user_profile.user.username,
            'profile_picture': user_profile.profile_picture.url
        })

    # Query to get age distribution
    age_distribution = Profile.objects.values('age').annotate(comment_count=Count('user__comment'))

    # Prepare data for age distribution chart
    age_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61+']
    age_data = [0] * len(age_labels)
    for item in age_distribution:
        if item['age'] is not None:
            age_group_index = min(item['age'] // 10, len(age_labels) - 1)
            age_data[age_group_index] += item['comment_count']

    # Query to get gender distribution
    gender_distribution = Profile.objects.values('gender').annotate(comment_count=Count('user__comment'))

    # Prepare data for gender distribution chart
    gender_labels = ['Male', 'Female']
    gender_data = [0, 0]
    for item in gender_distribution:
        if item['gender'] == 'M':
            gender_data[0] += item['comment_count']
        elif item['gender'] == 'F':
            gender_data[1] += item['comment_count']

    context = {
        'age_labels': age_labels,
        'age_data': age_data,
        'gender_labels': gender_labels,
        'gender_data': gender_data,
        'comments_with_user_info': comments_with_user_info
    }
    return render(request, 'view_comments.html', context)

@login_required
def update_profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        # Create a profile if it doesn't exist
        profile = Profile(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # Pass request.FILES for file uploads
        if form.is_valid():
            form.save()
            # Redirect to the profile update success page or dashboard
            return redirect('dashboard')  # Replace 'dashboard' with your dashboard URL name
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'update_profile.html', {'form': form})


@login_required
def view_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'view_profile.html', {'user_profile': user_profile})




@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # To keep the user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')  # Replace 'dashboard' with your dashboard URL name
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})


def voter_logout(request):
    logout(request)
    return redirect('user_login') 
