from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('question/<int:question_id>/answer/', views.post_answer, name='post_answer'),
    path('answer/<int:answer_id>/like/', views.like_answer, name='like_answer'),
    path('profile/', views.user_profile, name='user_profile'),
]
