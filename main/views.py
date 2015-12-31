from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from .models import Order
from .models import Approver
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

def approval_decision(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        from .forms import MyForm
        form = MyForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            decision = form.data[u'my_choice_field']
            order_id = form.data[u'order_id']

            order = Order.objects.get(id=order_id)
            user = request.user

            approver = Approver.objects.get(user=user)
            approval = order.approvals.get(user=approver)
            approval.approved = decision
            approval.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/main/order/%s' % (order_id))

    # if a GET (or any other method) we'll create a blank form
    return HttpResponseRedirect('/')

class OrderView(generic.DetailView):
    model = Order
    template_name = 'order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['name'] = "name"
        from .forms import MyForm
        order = context['object']
        form = MyForm(initial={'order_id': order.id})
        context['form'] = form
        user = self.request.user

        context['is_approver'] = order.is_approver(user)
        
        fill_users(context)
        return context

class UserView(generic.DetailView):
    model = User
    template_name = 'user.html'

    def get_context_data(self, **kwargs):
        context = super(UserView, self).get_context_data(**kwargs)
        open_orders = Order.objects.filter(closed=False)
        closed_orders = Order.objects.filter(closed=True)

        context['requester_open_orders'] = filter(lambda x: x.requester.user == context['object'], open_orders)
        context['requester_closed_orders'] = filter(lambda x: x.requester.user == context['object'], closed_orders)

        user = kwargs['object']
        require_user_approval = get_require_approval(user)

        require_user_approval_open = filter(lambda x: x.closed == False, require_user_approval)
        require_user_approval_closed = filter(lambda x: x.closed == True, require_user_approval)

        context['require_user_approval_open'] = map(lambda x: [x, x.my_approval(user)], require_user_approval_open)
        context['require_user_approval_closed'] = map(lambda x: [x, x.my_approval(user)], require_user_approval_closed)

        fill_users(context)

        return context

def get_require_approval(user):
    all_orders = Order.objects.all()

    require_user_approval = []
    for order in all_orders:
        for approval in order.approvals.all():
            if approval.user.user == user:
                require_user_approval.append(order)

    return require_user_approval

def fill_users(context):
    context['users'] = User.objects.all()
