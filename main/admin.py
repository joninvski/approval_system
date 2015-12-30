from django.contrib import admin
from datetime import datetime

from .models import Approval
from .models import ApprovalPriority
from .models import Approver
from .models import Item
from .models import PaymentMethod
from .models import VendorInformation
from .models import WorkflowTemplate
from .models import Order
from .models import Requester

class ItemInline(admin.TabularInline):
    model = Order.items.through
    extra = 2

class ApprovalPriorityInline(admin.TabularInline):
    model = Order.approvals.through
    extra = 3

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
        ApprovalPriorityInline,
    ]
    exclude = ['items', 'approvals', 'number']
    def save_model(self, request, obj, form, change):
        if obj.pk:
            obj.save()
            return

        obj.number = "%s-%d" % (datetime.now().year, Order.objects.count()+1)
        obj.save()
        obj.approvals = clone_approvals(obj.workflow_template)
        obj.save()

def clone_approvals(workflow_template):
    approvals = []
    for approval_priority in workflow_template.approval_list.all():
        user = approval_priority.user
        approval = Approval()
        approval.time = datetime.now()
        approval.user = approval_priority.user
        approval.save()
        approvals.append(approval)
    return approvals

# Register your models here.
admin.site.register(Approval)
admin.site.register(ApprovalPriority)
admin.site.register(Approver)
admin.site.register(Item)
admin.site.register(PaymentMethod)
admin.site.register(VendorInformation)
admin.site.register(WorkflowTemplate)
admin.site.register(Order, OrderAdmin)
admin.site.register(Requester)
