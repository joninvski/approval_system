from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='dashboard'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.UserView.as_view(), name='user'),
    url(r'^order/(?P<pk>[0-9]+)/$', views.OrderView.as_view(), name='order'),
    url(r'^approval_decision/$', views.approval_decision, name='approval_decision'),
]
