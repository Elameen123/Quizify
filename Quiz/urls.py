from django.urls import path
from django.contrib.auth import views

from .views import (ViewQuiz, MyQuizView, QuestionsView, AnswersView, quiz_data, quiz_view, create_question,
                    save_quiz, login_view, logout_view, register, create_quiz, create_answer)

app_name = 'Quiz'

urlpatterns = [
    path('', ViewQuiz.as_view(), name='main-view'),
    path('create-quiz/', create_quiz, name='create_quiz'),
    path('my-quizzes/', MyQuizView.as_view(), name="my_quizzes"),
    path('quiz/<pk>/questions/', QuestionsView.as_view(), name="quiz_questions"),
    path('quiz/<pk>/question/create', create_question,
         name="create_quiz_question"),
    path('question/<pk>/answers/', AnswersView.as_view(), name="question_answers"),
    path('question/<pk>/answer/create', create_answer,
         name="create_question_answer"),
    path('<pk>/', quiz_view, name='quiz-view'),
    path('<pk>/save/', save_quiz, name='save-quiz'),
    path('<pk>/data/', quiz_data, name='quiz-data'),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register"),
]
