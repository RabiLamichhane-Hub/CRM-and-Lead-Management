from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/', views.customer_view, name='customer_list'),
    path('projects/', views.projects_view, name='projects'),
    path('tickets/', views.tickets, name='tickets'),
    path('leads/', views.leads, name='leads'),
    path('inquiries/', views.inquiries, name='inquiries'),
    path('reports/', views.reports, name='reports'),
    path('new-customer/', views.newCustomer, name='newCustomer'),
    path('new-Ticket/', views.newTicket, name='newTicket'),
    path('customer-detail/', views.customerDetail, name='customerDetail'),
    path('ticket-detail/', views.ticketDetail, name='ticketDetail'),
    path('client/', views.client, name='client'),
    path('client-access/', views.clientAccess, name='clientAccess'),
    path('client-ticket/', views.clientTicket, name='clientTicket'),
    path('inquiry/', views.inquiry, name='inquiry'),
]