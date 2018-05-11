from django.db import models
from django.conf import settings
from posts.models import Post
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

# Create your models here.

# Using Model Manager for the comments

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent = None)
        return qs
    
    def filter_by_instance(self, instance):
        content_type        =       ContentType.objects.get_for_model(instance.__class__)
        obj_id              =       instance.id
        qs                  =       super(CommentManager, self).filter(content_type= content_type, object_id = obj_id).filter(parent = None)
        return qs


class Comment(models.Model):
    user            =       models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user', default = 1, on_delete=models.CASCADE)
    #post           =       models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE)
    content_type    =       models.ForeignKey(ContentType, on_delete=models.CASCADE, null= True)
    object_id       =       models.PositiveIntegerField(null = True)
    content_object  =       GenericForeignKey('content_type', 'object_id')
    parent          =       models.ForeignKey("self",null=True, blank=True, on_delete=models.CASCADE)
    content         =       models.TextField()
    timestamp       =       models.DateTimeField(auto_now_add =True)

    objects         =       CommentManager()

    def __str__(self):
        return self.content 

    def children(self):
        # these are the replies that belongs to a comment
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def get_absolute_url(self):
        return reverse('comments:comment_thread', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('comments:confirm_delete', kwargs={'id':self.id})

    class Meta:
        ordering            =       ['-timestamp']
        

