from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile, Book, Author, Genre, Publisher


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Required')
    class Meta:
        model = UserProfile
        fields = ("email", "name" ,"username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-input'


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class AddAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'


class AddGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = '__all__'


class AddPublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = '__all__'
