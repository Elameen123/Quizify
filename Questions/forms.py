from django import forms

from Questions import models


class QuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'})
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['text', 'correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
        }
