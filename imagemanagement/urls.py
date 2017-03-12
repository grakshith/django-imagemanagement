from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^test$',views.test,name='test'),
	url(r'^ajax/view/(?P<imageid>.*)',views.ajaxView,name='ajax'),
	url(r'^update/(?P<filename>.*)',views.update_or_delete,name='update_or_delete'),
	url(r'^',views.upload,name='upload'),

]