from django.shortcuts import render, get_object_or_404
from django.http import Http404,HttpResponseRedirect, HttpResponse
from .models import Comment
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
# Create your views here.

def comment_thread(request, id):
    #obj                 =           get_object_or_404(Comment, id =id)
    try:
        obj             =           Comment.objects.get(id = id)
    except:
        raise Http404
    if not obj.is_parent:
        obj = obj.parent
        print(obj)
    content_object      =           obj.content_object
    content_id          =           obj.content_object.id
    form                =           CommentForm(request.POST or None)

    initial_data        =       {
        "content_type"  :   obj.content_type,
        "object_id"     :   obj.object_id
    }
    form        =       CommentForm(request.POST or None, initial = initial_data)
    #print(form.errors)
    if form.is_valid():
        c_type          =       form.cleaned_data.get("content_type")
        content_type    =       ContentType.objects.get(model = c_type)
        obj_id          =       form.cleaned_data.get("object_id")
        content_data    =       form.cleaned_data.get("content")
        parent_obj       =       None
       
        try:
            #checking if the parent_id is an integer
            parent_id   =   int(request.POST.get('parent_id'))

        except:
            parent_id   =   None

        if parent_id:
            parent_qs   =   Comment.objects.filter(id = parent_id)
            if parent_qs.exists() and parent_qs.count() == 1:
                parent_obj  =   parent_qs.first() 
        

        new_comment, created =  Comment.objects.get_or_create(
            user            =       request.user,
            content_type    =       content_type,
            object_id       =       obj_id,
            content         =       content_data,
            parent          =       parent_obj,
        )            

        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
    args = {
        'comment' : obj,
        'form'    : form 
    }
    return render(request, 'comments/comment_thread.html', args)


def confirm_delete(request, id):
    """This Method deletes the a thread"""

    #obj = get_object_or_404(Comment, id=id)
    try:
        obj = Comment.objects.get(id = id )
    except:
        raise Http404
    if obj.user  != request.user:
        messages.success(request, "You are not permitted to delete this post")
        raise Http404
    if request.method == "POST":
        parent_obj_url = obj.content_object.get_absolute_url()
        print(parent_obj_url)
        obj.delete()
        messages.success(request, "This thread has been deleted")
        return HttpResponseRedirect(parent_obj_url)

    args = {
        "object" : obj,
    }
    return render(request, "comments/confirm_delete.html", args)