from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import *


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    name = forms.CharField()
    profile_picture = forms.ImageField()

    class Meta:
        model = UserCreate
        fields = ['name', 'profile_picture']


class TeamForm(forms.ModelForm):
    
    class Meta:
        model = Team
        fields = ['name', 'description']


class PriorityForm(forms.ModelForm):
    
    class Meta:
        model = Priority
        fields = ['name', 'color']


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super(ProjectForm, self).__init__(*args, **kwargs)

        if team:
            self.fields['leader'].queryset = TeamMember.objects.filter(team=team, is_manager=True)

    priority = forms.ModelChoiceField(
        queryset=Priority.objects.all(),
    )
    
    class Meta:
        model = Project
        fields = ['name', 'description', 'start', 'end', 'status', 'leader', 'priority']
        widgets = {
            'start': forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}),
            'end': forms.DateInput(attrs={'type': 'date',  'format': '%Y-%m-%d'}),
        }
    

class ProjectBoardForm(forms.Form):
    SORT_CHOICES = [
        ('name', 'Name'),
        ('progress', 'Progress'),
        ('date', 'Date'),
    ]

    ORDER_CHOICES = [
        ('asc', 'Ascending'),
        ('desc', 'Descending'),
    ]

    sort_by = forms.ChoiceField(required=False, choices=SORT_CHOICES)
    order_by = forms.ChoiceField(required=False, choices=ORDER_CHOICES)
    name = forms.CharField(required=False, label='Name', initial='')
    priority = forms.ModelChoiceField(
        queryset=Priority.objects.all(),
        required=False,
        label='Priority',
        initial='',
        empty_label='Any'
    )
    
    class Meta:
        model = Project  
        fields = ['sort_by', 'order_by', 'name', 'priority']

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        team = kwargs.pop('team', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if team:
            self.fields['assigned_to'].queryset = TeamMember.objects.filter(team=team)

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'deadline', 'priority', 'status']
        widgets = {
                'deadline': forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'}),
                }


class TaskBoardForm(forms.Form):
    SORT_CHOICES = [
        ('name', 'Name'),
        ('date', 'Date'),
    ]

    ORDER_CHOICES = [
        ('asc', 'Ascending'),
        ('desc', 'Descending'),
    ]

    sort_by = forms.ChoiceField(required=False, choices=SORT_CHOICES, initial='name')
    order_by = forms.ChoiceField(required=False, choices=ORDER_CHOICES, initial='asc')
    name = forms.CharField(required=False, label='Name', initial='')
    priority = forms.ModelChoiceField(
        queryset=Priority.objects.all(),
        required=False,
        label='Priority',
        initial='',
        empty_label='Any'
    )
    
    class Meta:
        model = Task  
        fields = ['sort_by', 'order_by', 'name', 'priority']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
    

class Notification(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message', 'is_read']


class TeamInvitationForm(forms.ModelForm):
    class Meta:
        model = TeamInvitation
        fields = ['receiver', 'message']

    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        initial="Hello, I invite you to join my team!"
    )


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ['role', 'responsibilities', 'is_manager']


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['description', 'file']


class TeamDeleteForm(forms.Form):
    confirmation = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )


class LeaveTeamForm(forms.Form):
    confirmation = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )


class TeamUpdateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description']