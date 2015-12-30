from django.contrib.auth.models import User
from main.models import *
from subprocess import call
from datetime import datetime
from datetime import timedelta

call(["rm", "db.sqlite3"])
call(["python", "manage.py", "makemigrations", "main"])
call(["python", "manage.py", "migrate"])

user_sofia = User.objects.create_user(username="sofia", password='talkdesk')
user_sofia.is_superuser=True
user_sofia.is_staff=True
user_sofia.save()

user_magda = User.objects.create_user(username="magda", password="pass")
user_magda.is_superuser=True
user_magda.is_staff=True
user_magda.save()

user_milena = User.objects.create_user(username="milena", password="pass")
user_milena.save()

user_tiago = User.objects.create_user(username="tiago", password="pass")
user_tiago.save()

user_ben = User.objects.create_user(username="ben", password="pass")
user_ben.save()

vendor_information_ikeia = VendorInformation()
vendor_information_ikeia.name = "Ikea"
vendor_information_ikeia.address_first = "Rua de Longe"
vendor_information_ikeia.address_second = "Do outro lado"
vendor_information_ikeia.city = "Lisboa"
vendor_information_ikeia.st = ""
vendor_information_ikeia.zip = "1000"
vendor_information_ikeia.save()

vendor_information_fnac = VendorInformation()
vendor_information_fnac.name = "Fnac"
vendor_information_fnac.address_first = "Columbo"
vendor_information_fnac.address_second = "Benfica"
vendor_information_fnac.city = "Lisboa"
vendor_information_fnac.st = ""
vendor_information_fnac.zip = "1000"
vendor_information_fnac.save()

item_a = Item()
item_a.quantity = 1
item_a.description = "24Inch monitor LEG"
item_a.unit_price = 300.20
item_a.save()

item_b = Item()
item_b.quantity = 10
item_b.description = "Mac laptop"
item_b.unit_price = 1300.01
item_b.save()

item_c = Item()
item_c.quantity = 50
item_c.description = "Pretty chair"
item_c.unit_price = 13.00
item_c.save()

payment_method_a = PaymentMethod()
payment_method_a.description = "Vendor to invoice  Talkdesk -  Accounts PayableShipping"
payment_method_a.save()

payment_method_b = PaymentMethod()
payment_method_b.description = "Employee travel and expense report"
payment_method_b.save()

payment_method_c = PaymentMethod()
payment_method_c.description = "American Express - Corporate card"
payment_method_c.save()

approver_tiago = Approver()
approver_tiago.name = "Tiago"
approver_tiago.user = user_tiago
approver_tiago.save()

approver_milena = Approver()
approver_milena.name = "Milena"
approver_milena.user = user_milena
approver_milena.save()

approver_ben = Approver()
approver_ben.name = "Ben"
approver_ben.user = user_ben
approver_ben.save()

approver_sofia = Approver()
approver_sofia.name = "Sofia"
approver_sofia.user = user_sofia
approver_sofia.save()

requester_sofia = Requester()
requester_sofia.name = "Sofia"
requester_sofia.user = user_sofia
requester_sofia.save()

requester_magda = Requester()
requester_magda.name = "Magda"
requester_magda.user = user_magda
requester_magda.save()

priority_sofia = ApprovalPriority()
priority_sofia.user = approver_sofia 
priority_sofia.priority = 2
priority_sofia.save()

priority_ben = ApprovalPriority()
priority_ben.user = approver_ben
priority_ben.priority = 1
priority_ben.save()

priority_milena = ApprovalPriority()
priority_milena.user = approver_milena
priority_milena.priority = 1
priority_milena.save()

priority_tiago = ApprovalPriority()
priority_tiago.user = approver_tiago
priority_tiago.priority = 0
priority_tiago.save()

workflow_template_a = WorkflowTemplate()
workflow_template_a.name = "Departament A"
workflow_template_a.save()
workflow_template_a.approval_list = [priority_milena, priority_tiago, priority_sofia]
workflow_template_a.save()

workflow_template_b = WorkflowTemplate()
workflow_template_b.name = "Departament B"
workflow_template_b.save()
workflow_template_b.approval_list = [priority_milena, priority_tiago, priority_sofia]
workflow_template_b.save()

order_a = Order()
order_a.number = 1
order_a.time = datetime.now()
order_a.payment_method = payment_method_c 
order_a.requester = requester_magda 
order_a.vendor = vendor_information_ikeia
order_a.workflow_template = workflow_template_a
order_a.business_purpose = "We need it for the new staff"
order_a.save()
order_a.items = [item_a, item_b]
# order_a.approvals = [priority_sofia, priority_tiago, priority_milena]
order_a.save()

order_b = Order()
order_b.number = 2
order_b.time = datetime.now() - timedelta(1, 1500)
order_b.payment_method = payment_method_c 
order_b.requester = requester_magda 
order_b.vendor = vendor_information_ikeia
order_b.workflow_template = workflow_template_a
order_b.business_purpose = "These monitors are pretty"
order_b.save()
order_b.items = [item_c]
# order_b.approvals = [priority_sofia, priority_tiago, priority_milena]
order_b.save()

order_c = Order()
order_c.number = 3
order_c.time = datetime.now() - timedelta(1, 1500)
order_c.payment_method = payment_method_c 
order_c.requester = requester_magda 
order_c.vendor = vendor_information_ikeia
order_c.workflow_template = workflow_template_a
order_c.business_purpose = "We need new chairs"
order_c.closed = True
order_c.save()
order_c.items = [item_c]
# order_c.approvals = [priority_sofia, priority_tiago, priority_milena]
order_c.save()
