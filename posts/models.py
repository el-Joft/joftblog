from django.db import models
#from Posts.helper import generateE_id
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import pre_save
from django.utils.text import slugify
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .utils import get_read_time
#importing requirements to the models

import base64
import uuid 
from datetime import date
from django.utils import timezone


# Create your models here.

class PostManager(models.Manager):
	"""Models manager controls how the models work e.g 
	the queryset such as all(), create(), etc
	"""
	def all(self, *args, **kwargs):
		return super(PostManager, self).all()


class Post(models.Model):
	"""Model representing the posts for the articless"""
	user			=			models.ForeignKey(settings.AUTH_USER_MODEL, default = 1 ,on_delete=models.CASCADE)
	title           =           models.CharField( max_length=200)
	slug = 						models.SlugField(unique = True, help_text="A short label, generally used in URLs.")
	#id              =           models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
	#key  			= 			models.CharField(max_length=200, null=False, blank=True, verbose_name='Book ID')
	read_time		=			models.IntegerField(default = 0)
	#author          =           models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	body            =           models.TextField(max_length = 1000)
	allow_comments  =           models.BooleanField( default=True)
	created         =           models.DateTimeField( auto_now_add=True)
	modified        =           models.DateTimeField()
	categories      =           models.ManyToManyField("Category", blank=True, null = True)
	image           =           models.FileField(null= True, blank=True,upload_to='uploads/img')
	draft			=			models.BooleanField(default=False)

	objects = PostManager()

	class Meta:
		verbose_name            =  'post'
		verbose_name_plural     =   'posts'
		db_table                =   'blog_posts'
		ordering                =   ['-created',]
		get_latest_by           =   'created'

	def __str__(self):
		return self.title

	def get_markdown(self):
		content = self.body
		markdown_text = markdown(content)
		return mark_safe(markdown_text)

	def get_absolute_url(self):
		
		return reverse('posts:post_detail', kwargs={'slug': self.slug})

	# @property
	# def comments(self):
	# 	instance = self
	# 	qs = Comment.objects.filter_by_instance(instance)
	# 	return qs

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type
	
	




	# def save(self,*args,**kwargs):
	# 	key = generateE_id()
	# 	self.key = key
	# 	#   print "generate id ", e_id
	# 	super(Post, self).save( *args, **kwargs)


class Category(models.Model):
	"""Category model."""
	title = models.CharField(max_length=100)
	slug = models.UUIDField( default=uuid.uuid4, editable=False)

	class Meta:
		verbose_name = ('category')
		verbose_name_plural = ('categories')
		db_table = 'blog_categories'
		ordering = ('title',)

	
	def __str__(self):

		return self.title


	@models.permalink
	def get_absolute_url(self):
		return ('post_category_detail', None, {'slug': self.slug})


def create_slug(instance,  new_slug = None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug = slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug,qs.first().id)
		return create_slug(instance, new_slug = new_slug)
	return slug

def pre_save_post_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

	if instance.body:
		html_string 		= 	instance.get_markdown()
		read_time_var 		= 	get_read_time(html_string)
		instance.read_time 	=	read_time_var


pre_save.connect(pre_save_post_reciever, sender = Post)