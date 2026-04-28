from django.shortcuts import render, get_object_or_404, redirect
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login ,User

# Home page
def index(request):
    return render(request, 'index.html')


# List tweets
@login_required
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})


# Create tweet
@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()

    return render(request, 'tweet_form.html', {'form': form})


# Edit tweet
@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user   # fixed
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'tweet_form.html', {'form': form})


# Delete tweet
@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')

    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})



def register(request):
  if request.method =='POST':
    form= UserRegistrationForm(request.POST) 
    if form.is_valid():
      user = form.save(commit=False)
      user.set_password(form.cleaned_data['password1'])
      user.save()
      login  (request,user)
      return redirect('tweet_list')
  else:
      form = UserRegistrationForm()
  return render(request, 'registration/register.html', {'form': form})    

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    if request.user in tweet.likes.all():
        tweet.likes.remove(request.user)   # unlike
    else:
        tweet.likes.add(request.user)      # like

    return redirect('tweet_list')

def profile(request, username):
    user = User.objects.get(username=username)
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')

    return render(request, 'profile.html', {
        'user_profile': user,
        'tweets': tweets
    })