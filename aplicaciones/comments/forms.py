from django import forms
from django_comments.forms import CommentForm


class CommentFormWithArchive(CommentForm):
    archive = forms.FileField(required=False)

    def get_comment_create_data(self):
        data = super(CommentFormWithArchive, self).get_comment_create_data()
        data['archive'] = self.cleaned_data['archive']
        return data

    def form_valid(self, form):
        print 'paso'
