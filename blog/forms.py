from django import forms

from blog.models import Comment

BASE_INPUT_CLASS = "bg-gray-50 border rounded-lg text-heading text-sm focus:ring-brand focus:border-brand block w-full px-2.5 py-2 shadow-xs placeholder:text-body"

class CommentForm(forms.ModelForm):
    class Meta :
        model=Comment
        fields = ['user_name' , 'user_email' , 'content']
        labels = {
            'user_name' : 'Your Name' ,
            'user_email' :'Your Email' ,
            'content' :"Your comment"
        }
        widgets  = {
            'user_name' : forms.TextInput(attrs={'class':BASE_INPUT_CLASS}),
            'user_email' : forms.TextInput(attrs={'class':BASE_INPUT_CLASS}),
            'content':forms.Textarea(attrs={'class'  : BASE_INPUT_CLASS}) ,
        }


