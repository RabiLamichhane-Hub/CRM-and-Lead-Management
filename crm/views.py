from django.shortcuts import render
from . models import Customer

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def customer_view(request):
    return render(request, 'customers.html')

def projects_view(request):
    return render(request, 'projects.html')

def tickets(request):
    return render(request, 'tickets.html')

def leads(request):
    return render(request, 'leads.html')

def inquiries(request):
    return render(request, 'inquiries.html')

def reports(request):
    return render(request, 'reports.html')

def newCustomer(request):
    return render(request, 'newCustomer.html')

def newTicket(request):
    return render(request, 'newTicket.html')

def customerDetail(req):
    return render(req, 'customerDetail.html')

def ticketDetail(req):
    return render(req, 'ticketDetail.html')

def client(req):
    return render(req, 'client.html')

def clientAccess(req):
    return render(req, 'clientAccess.html')

def inquiry(req):
    return render(req, 'inquiry.html')

def clientTicket(req):
    return render(req, 'clientTicket.html')