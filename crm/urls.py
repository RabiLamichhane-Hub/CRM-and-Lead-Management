from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('customers/', views.customer_view, name='customer_list'),
    path('projects/', views.projects_view, name='projects'),
    path('new-project/', views.newProject, name='newProject'),
    path('projects/<int:pk>/edit/', views.editProject, name='editProject'),

    path('tickets/', views.tickets, name='tickets'),

    path('leads/', views.leads, name='leads'),
    path('new-lead/', views.newLead, name='newLead'),
    path('leads/<int:pk>/stage/', views.updateLeadStage, name='updateLeadStage'),

    path('inquiries/', views.inquiries, name='inquiries'),
    path('inquiries/<int:pk>/review/', views.updateInquiryStatus, name='updateInquiryStatus'),
    path('inquiry/', views.inquiry, name='inquiry'),

    path('reports/', views.reports, name='reports'),
    path('new-customer/', views.newCustomer, name='newCustomer'),
    path('new-Ticket/', views.newTicket, name='newTicket'),
    path('customer-detail/<int:pk>/', views.customerDetail, name='customerDetail'),
    path('ticket-detail/<int:pk>/', views.ticketDetail, name='ticketDetail'),

    path('client/', views.client, name='client'),
    path('client-access/', views.clientAccess, name='clientAccess'),
    path('client-ticket/', views.clientTicket, name='clientTicket'),

    
]