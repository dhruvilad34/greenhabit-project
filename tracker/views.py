from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import UserProfileForm, GoalForm
from .models import UserProfile, Goal, Like, Comment, BlogPost  # ✅ Include BlogPost

# ✅ Home page
def home(request):
    return render(request, 'tracker/home.html')

# ✅ Goal submission
@login_required
def submit_goal(request):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goal_list')
    else:
        form = GoalForm()
    return render(request, 'tracker/submit_goal.html', {'form': form})

# ✅ Goal list with search and filter
def goal_list(request):
    query = request.GET.get('q')
    category = request.GET.get('category')

    goals = Goal.objects.all().order_by('-id')

    if query:
        goals = goals.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category and category != 'all':
        goals = goals.filter(category=category)

    paginator = Paginator(goals, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tracker/goal_list.html', {
        'goals': page_obj,
        'query': query or '',
        'selected_category': category or 'all',
        'page_obj': page_obj,
    })

# ✅ Like goal
@login_required
def like_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    if request.user not in goal.likes.all():
        goal.likes.add(request.user)
    return redirect('goal_list')

# ✅ Add comment
@login_required
def add_comment(request, goal_id):
    if request.method == 'POST':
        goal = get_object_or_404(Goal, id=goal_id)
        text = request.POST.get('text')
        if text:
            Comment.objects.create(goal=goal, user=request.user, text=text)
    return redirect('goal_list')

# ✅ My goals
@login_required
def my_goals(request):
    goals = Goal.objects.filter(user=request.user).order_by('-id')
    return render(request, 'tracker/my_goals.html', {'goals': goals})

# ✅ Edit goal
@login_required
def edit_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)

    if request.method == 'POST':
        form = GoalForm(request.POST, instance=goal)
        if form.is_valid():
            form.save()
            messages.success(request, "Goal updated successfully.")
            return redirect('my_goals')
    else:
        form = GoalForm(instance=goal)

    return render(request, 'tracker/edit_goal.html', {'form': form, 'goal': goal})

# ✅ Delete goal
@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    if request.method == 'POST':
        goal.delete()
        messages.success(request, "Goal deleted successfully.")
        return redirect('my_goals')
    return render(request, 'tracker/delete_goal.html', {'goal': goal})

# ✅ Profile view and edit
@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'tracker/profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'tracker/edit_profile.html', {'form': form})

# ✅ Visit history with session
def visit_history(request):
    now = timezone.now()
    visit_count = request.session.get('visit_count', 0)
    last_visit = request.session.get('last_visit')

    visit_count += 1
    request.session['visit_count'] = visit_count
    request.session['last_visit'] = str(now)

    return render(request, 'tracker/visit_history.html', {
        'visit_count': visit_count,
        'last_visit': last_visit
    })

# ✅ About page
def about(request):
    return render(request, 'tracker/about.html')

# ✅ Blog list
@login_required
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'tracker/blog_list.html', {'posts': posts})

# ✅ Blog detail
@login_required
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        text = request.POST.get('comment')
        if text:
            Comment.objects.create(post=post, user=request.user, text=text)
            return redirect('blog_detail', pk=pk)

    return render(request, 'tracker/blog_detail.html', {
        'post': post,
        'comments': comments,
    })
