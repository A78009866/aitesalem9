from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User, Post, FriendRequest, Message, Like, Comment
from .forms import PostForm

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, 'network/index.html', {'posts': posts})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'network/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirmation = request.POST["password_confirmation"]

        if password != password_confirmation:
            return render(request, "network/register.html", {
                "message": "كلمات المرور غير متطابقة."
            })

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "اسم المستخدم مستخدم بالفعل."
            })

        login(request, user)
        return redirect("index")

    return render(request, "network/register.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("index")
    else:
        form = PostForm()
    return render(request, "network/index.html", {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('index')

from django.http import JsonResponse

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return JsonResponse({
        'success': True,
        'liked': created,
        'like_count': post.likes.count()
    })

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id)
        body = request.POST.get("body")
        if body:
            comment = Comment.objects.create(user=request.user, post=post, body=body)
            return JsonResponse({
                'success': True,
                'username': comment.user.username,
                'body': comment.body,
                'timestamp': comment.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
    return JsonResponse({'success': False})

@login_required
def delete_comment(request, comment_id):  # جديد
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    comment.delete()
    return redirect('index')

@login_required
def edit_comment(request, comment_id):  # جديد
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    if request.method == "POST":
        body = request.POST.get("body")
        if body:
            comment.body = body
            comment.save()
            return redirect('index')
    return render(request, 'network/edit_comment.html', {'comment': comment})

@login_required
def users_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'network/users.html', {'users': users})

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect('users')

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.to_user.friends.add(friend_request.from_user)
    friend_request.from_user.friends.add(friend_request.to_user)
    friend_request.delete()
    return redirect('friend_requests')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.delete()
    return redirect('friend_requests')

@login_required
def friend_requests(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, "network/friend_requests.html", {"requests": requests})

@login_required
def send_message(request, user_id):
    if request.method == "POST":
        receiver = get_object_or_404(User, id=user_id)
        body = request.POST.get("body")
        if body:
            Message.objects.create(sender=request.user, receiver=receiver, body=body)
        return redirect('messages', user_id=user_id)
    return redirect('users')

@login_required
def messages(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(sender=request.user, receiver=other_user) | Message.objects.filter(sender=other_user, receiver=request.user)
    messages = messages.order_by('timestamp')
    return render(request, 'network/messages.html', {'messages': messages, 'other_user': other_user, 'room_name': f'{min(request.user.id, other_user.id)}_{max(request.user.id, other_user.id)}'})

@login_required
def message_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'network/message_list.html', {'users': users})

# ... (الدوال الأخرى تبقى كما هي)

@login_required
def profile(request):
    return render(request, 'network/profile.html')

from django.shortcuts import render

def splash(request):
    return render(request, 'splash.html')  # تأكد من أن لديك ملف splash.html في templates
