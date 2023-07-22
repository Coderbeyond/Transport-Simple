from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import Question, Answer, Like
from .forms import QuestionForm, AnswerForm, SignupForm

def home(request):
    questions = Question.objects.order_by('-timestamp')
    return render(request, 'quoraclone/home.html', {'questions': questions})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'quoraclone/login.html', {'message': 'Invalid username or password.'})
    return render(request, 'quoraclone/login.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'quoraclone/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect('question_detail', question_id=question.pk)
    else:
        form = QuestionForm()
    return render(request, 'quoraclone/ask_question.html', {'form': form})

def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    answers = Answer.objects.filter(question=question).order_by('-timestamp')
    return render(request, 'quoraclone/question_detail.html', {'question': question, 'answers': answers})

@login_required
def post_answer(request, question_id):
    question = Question.objects.get(pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id=question.pk)
    else:
        form = AnswerForm()
    return render(request, 'quoraclone/post_answer.html', {'form': form, 'question': question})

@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(pk=answer_id)
    like, created = Like.objects.get_or_create(user=request.user, answer=answer)
    if created:
        return redirect('question_detail', question_id=answer.question.pk)
    else:
        like.delete()
        return redirect('question_detail', question_id=answer.question.pk)

@login_required
def user_profile(request):
    user_questions = Question.objects.filter(author=request.user).order_by('-timestamp')
    user_answers = Answer.objects.filter(author=request.user).order_by('-timestamp')
    return render(request, 'quoraclone/user_profile.html', {'user_questions': user_questions, 'user_answers': user_answers})
