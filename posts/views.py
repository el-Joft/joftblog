from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from urllib.parse import quote
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import Http404,HttpResponseRedirect, HttpResponse 
from comments.models import Comment
from comments.forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from posts.utils import get_read_time

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from posts.forms import HomeForm
from django.urls import reverse

from posts.models import Post

from django.db.models import Q

# Create your views here.
# def home(request):
#     args ={'user': request.user }
#     return HttpResponse('It works')

# Using the Generic view

class HomeView(TemplateView):
    template_name = 'posts/home.html'

    # create a method to overite the default django get method

    def get(self, request):
        'This method deals with the form handling'
        form = HomeForm()
        # using the below method is of no use since the it has been stated
        # in the model using class meta: to set the ordering
        # posts = Post.objects.all().order_by("-created")
        # post_list = Post.objects.all()
        # #users = User.objects.all()
        
        # # creating a share_string for the quote_plus
       

        # # the above users collected include the logged in user, which we don't want to
        # # show that, only others

        # paginator = Paginator(post_list, 1) # Show 25 contacts per page
        # page = request.GET.get('page')
        # posts = paginator.get_page(page)





        args = {
            'form'          :               form,
        }
        # note: template name is used because the template has already
        # been stored as a variable into the template_name variable
        return render(request, self.template_name, args)

    def post(self, request):
        """ creating a post method to handle the post request"""
        # No need to use if request.method == 'POST'

        # if not request.user.is_staff or not request.user.is_superuser:
        #     raise Http404

        form = HomeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.success(request, 'Post created Successfully.')
            title = form.cleaned_data['title']
            body  = form.cleaned_data['body']
            form = HomeForm()

            return redirect("posts:home")
        args = {
            'form'  : form,
            'title' : title,
            'body'  : body,
        }


        return render(request, self.template_name, args)

def editPost(request, slug):
    template_name = 'posts/edit_post.html'
    instance = get_object_or_404(Post, slug = slug)
    form = HomeForm(request.POST or None, instance = instance)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        messages.success(request, 'Post updated Successfully.')

        return redirect("posts:home")
    
    args = {
        'form'  : form,
        
    }
    return render(request, template_name , args)

def deletePost(request, id=None):
    
    instance = get_object_or_404(Post, id = id)
    instance.delete()

    return redirect("posts:home")



def postDetail(request, slug):
    'This method deals with the form handling'
    instance            =       get_object_or_404(Post, slug= slug)
    print(instance.read_time)
    share_string        =       quote(instance.body)
    # content_type        =       ContentType.objects.get_for_model(Post)
    # obj_id              =       instance.id
    #comments               =       Comment.objects.filter(content_type= content_type, object_id = obj_id)
    
    initial_data        =       {
        "content_type"  :   instance.get_content_type,
        "object_id"     :   instance.id
    }
    form        =       CommentForm(request.POST or None, initial = initial_data)

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
    #comments = instance.comments   
    comments             = Comment.objects.filter_by_instance(instance)
    # note: template name is used because the template has already
    # been stored as a variable into the template_name variable
    
    
    args = {
        'share_string'  :               share_string,
        'instance'      :               instance,
        'comments'      :               comments,
        'form'          :               form,
        
        
    }
    return render(request, 'posts/post_detail.html', args)


    




    
class PostListView(TemplateView):
    template_name = "posts/post_list.html"
    
    def get(self, request):
        # note that we ahve override the .all() from the model using the model Manager
        queryset_list = Post.objects.all()

        
            #users = User.objects.all()
            
            # creating a share_string for the quote_plus
        

            # the above users collected include the logged in user, which we don't want to
            # show that, only others

        paginator = Paginator(queryset_list, 1) # Show 25 contacts per page
        page = request.GET.get('page')
        posts = paginator.get_page(page)

        query = request.GET.get("q")

        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains =query) |
                Q(body__icontains =query) 
                #Q(author__icontains =query)
                # ).distint()
            )

        args = {
                'queryset_list'  :               queryset_list,
                'posts'          :               posts,
                
                
            }
        return render(request, self.template_name , args)
        
