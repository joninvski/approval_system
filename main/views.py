from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import Order
from .models import Item
from django.views import generic
from django.contrib.auth.models import User
from .forms import OrderForm

def index(request):
    closed_orders = Order.objects.filter(closed=True)
    open_orders = Order.objects.filter(closed=False)

    context = {
        'open_orders': open_orders,
        'closed_orders': closed_orders,
    }
    fill_users(context)
    return render(request, 'main.html', context)

class OrderView(generic.DetailView):
    model = Order
    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['name'] = "name"
        fill_users(context)
        return context

class UserView(generic.DetailView):
    model = User
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        open_orders = Order.objects.filter(closed=False)
        closed_orders = Order.objects.filter(closed=True)
        context['open_orders'] = filter(lambda x: x.requester.user == context['object'], open_orders)
        context['closed_orders'] = filter(lambda x: x.requester.user == context['object'], closed_orders)
        fill_users(context)

        return context

def fill_users(context):
    context['users'] = User.objects.all()
