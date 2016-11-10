def get_model():
    from .models import CommentWithArchive
    return CommentWithArchive


def get_form():
    from .forms import CommentFormWithArchive
    return CommentFormWithArchive
