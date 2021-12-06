from .models import ToyComment
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404

#source: https://djangocentral.com/creating-comments-system-with-django/
def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()


    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def toy_post(request):
    template_name = 'post_detail.html'
    #post = get_object_or_404(Post, slug=slug)
    comments = ToyComment.objects.using('fuse_attend').all()
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = request.POST.get("body", None);
            author = request.POST.get("name", None);
            email = request.POST.get("email", None);
            print(comment, author, email)
            # Create Comment object but don't save to database yet
            new_comment = ToyComment.objects.using('fuse_attend').create(comment=comment, author=author)
            # Assign the current post to the comment
            #new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'code_share/template.html', {'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form})


def toyComment(request):
    if request.is_ajax and request.method == "POST":
        # get the nick name from the client side.
        #post = request.POST.get("username", None);
        comment = request.POST.get("comment", None);
        author = request.POST.get("author", None);
        
    if not str(comment).strip()=='':
        ToyComments.objects.using('fuse_attend').create(comment=str(comment), author = str(author))
        return HttpResponse('Successfully commented')
    
    else:
        return HttpResponse('Comment is empty')
