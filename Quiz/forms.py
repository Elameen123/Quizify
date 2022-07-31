from django import forms

from Quiz import models

class CreateQuizForm(forms.ModelForm):
    class Meta:
        model = models.Quiz
        fields = ['name', 'topic', 'number_of_questions', 'duration', 'Pass_score', 'quiz_difficulty']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'topic': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_questions': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'Pass_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'quiz_difficulty': forms.Select(attrs={'class':'form-control'})
        }