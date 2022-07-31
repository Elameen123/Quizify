from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import (HttpResponse, HttpResponseRedirect, JsonResponse,
                         request)
from django.shortcuts import redirect, render, reverse
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from Quiz import forms
from Questions import forms as question_forms
from Questions.models import Answer, Question
from Results.models import Result
from .models import Owner, Quiz

# Create your views here.


class ViewQuiz(ListView):
    model = Quiz
    template_name = 'Quiz/index.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ViewQuiz, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Quiz.objects.all().exclude(user=self.request.user)


@login_required
def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, 'Quiz/quiz.html', {
        'obj': quiz
    })


@login_required
def create_quiz(request):
    form = forms.CreateQuizForm
    if request.method == "POST":
        body = request.POST
        form = form(body)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return HttpResponseRedirect(reverse('Quiz:main-view'))

        return render(request, 'Quiz/create_quiz.html', {"form": form})
    else:
        return render(request, 'Quiz/create_quiz.html', {"form": form})


class MyQuizView(ListView):
    context_object_name = 'my_quizzes'
    template_name = 'Quiz/my_quizzes.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(MyQuizView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return Quiz.objects.all().filter(user=self.request.user)


class QuestionsView(ListView):
    context_object_name = 'questions'
    template_name = 'Quiz/questions.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuestionsView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        quiz_pk = self.kwargs.get('pk')
        return Question.objects.all().filter(quiz__user=self.request.user, quiz=quiz_pk)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['quiz_id'] = self.kwargs.get('pk')
        return context


@login_required
def create_question(request, pk):
    form = question_forms.QuestionForm

    if request.method == "POST":
        body = request.POST
        form = form(body)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.quiz_id = pk
            obj.save()
            return HttpResponseRedirect(reverse('Quiz:quiz_questions', kwargs={'pk': pk}))

    return render(request, 'Quiz/create_question.html', {'form': form, 'quiz_id': pk})


class AnswersView(ListView):
    context_object_name = 'answers'
    template_name = 'Quiz/answers.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AnswersView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        question_pk = self.kwargs.get('pk')
        return Answer.objects.all().filter(question__quiz__user=self.request.user, question=question_pk)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['question_id'] = self.kwargs.get('pk')
        return context


@login_required
def create_answer(request, pk):
    form = question_forms.AnswerForm

    if request.method == "POST":
        body = request.POST
        form = form(body)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.question_id = pk
            obj.save()
            return HttpResponseRedirect(reverse('Quiz:question_answers', kwargs={'pk': pk}))

    return render(request, 'Quiz/create_answer.html', {'form': form, 'question_id': pk})


@login_required
def quiz_data(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    return JsonResponse({
        'data': questions,
        'time': quiz.duration,
    })


@login_required
def save_quiz(request, pk):
    # checking if the request is an ajax request
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        # deleting csrf token from data
        data_.pop('csrfmiddlewaretoken')

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        # The Quiz Result

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            # getting the selected answer
            a_selected = request.POST.get(q.text)

            # checking if the chosen answer is the correct answer, marking it and saving the score
            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                # if quesion is answered, provide the chosen answer and the correct answer
                results.append({str(q): {
                    'correct_answer': correct_answer,
                    'answered': a_selected,
                }})
            else:
                # if question is not answered,   display not answered
                results.append({str(q): 'not answered'})

        # calculating the final score
        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        # check if the user Passed or fail the quiz
        if score_ >= quiz.Pass_score:
            return JsonResponse({'Passed': True, 'score': score_, 'result': results})

        else:
            return JsonResponse({'Passed': False, 'score': score_, 'result': results})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("Quiz:main-view"))
        else:
            return render(request, "Quiz/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Quiz/login.html")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("Quiz:main-view"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Quiz/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = Owner.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Quiz/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("Quiz:main-view"))
    else:
        return render(request, "Quiz/register.html")
