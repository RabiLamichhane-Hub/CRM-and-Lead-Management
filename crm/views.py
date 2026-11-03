from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import (
    Customer,
    Project,
    SupportTicket,
    Lead,
    Inquiry,
)
from . forms import InquiryForm, LeadForm, ProjectForm
from django.contrib import messages
from django.db.models import Count, Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme

# Create your views here.
def dashboard(request):
    today = timezone.localdate()

    active_tickets = SupportTicket.objects.exclude(
        status__in=[SupportTicket.Status.RESOLVED, SupportTicket.Status.CLOSED]
    )
    open_leads = Lead.objects.exclude(
        stage__in=[Lead.Stage.WON, Lead.Stage.LOST]
    )

    followups = list(
        open_leads.filter(follow_up_date__isnull=False)
        .order_by("follow_up_date")[:3]
    )
    for lead in followups:
        lead.is_overdue = lead.follow_up_date < today
        lead.is_today = lead.follow_up_date == today

    context = {
        "customer_count": Customer.objects.count(),
        "active_ticket_count": active_tickets.count(),
        "reopened_count": active_tickets.filter(
            status=SupportTicket.Status.REOPENED
        ).count(),
        "active_lead_count": open_leads.count(),
        "followups_due_count": open_leads.filter(
            follow_up_date__lte=today
        ).count(),
        "recent_tickets": SupportTicket.objects.select_related("customer")[:5],
        "followups": followups,
        "latest_reopened": SupportTicket.objects.select_related("customer")
            .filter(status=SupportTicket.Status.REOPENED)
            .order_by("-updated_at").first(),
        "latest_inquiry": Inquiry.objects.first(),
    }
    return render(request, 'dashboard.html', context)

def customer_view(request):
    customer = Customer.objects.annotate(
        project_count=Count("projects", distinct=True),
        active_tickets=Count(
            "support_tickets",
            filter=~Q(support_tickets__status__in=["resolved", "closed"]),
            distinct=True,
        ),
    )
    return render(request, 'customers.html', {'customer': customer})


def projects_view(request):
    projects = Project.objects.select_related("customer")
    return render(request, 'projects.html', {'projects': projects})

def newProject(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Project created.")
            return redirect("projects")
    else:
        form = ProjectForm()
    return render(request, 'newProject.html', {'form': form})

def editProject(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f"{project.name} updated.")
            return redirect("projects")
    else:
        form = ProjectForm(instance=project)
    return render(request, 'newProject.html', {'form': form, 'project': project})

def tickets(request):
    ticket_list = SupportTicket.objects.select_related("customer")
    return render(request, 'tickets.html', {'ticket_list': ticket_list})

def leads(request):
    today = timezone.localdate()
    all_leads = list(Lead.objects.select_related("converted_customer"))

    open_stages = {
        Lead.Stage.NEW,
        Lead.Stage.CONTACTED,
        Lead.Stage.QUALIFIED,
        Lead.Stage.PROPOSAL_SENT,
    }
    for lead in all_leads:
        lead.overdue = bool(
            lead.follow_up_date
            and lead.follow_up_date < today
            and lead.stage in open_stages
        )

    stages = [
        {
            "value": value,
            "label": label,
            "leads": [l for l in all_leads if l.stage == value],
        }
        for value, label in Lead.Stage.choices
    ]
    return render(request, 'leads.html', {'stages': stages})

def newLead(request):
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead added to the pipeline.")
            return redirect("leads")
    else:
        form = LeadForm()
    return render(request, 'newLead.html', {'form': form})


@require_POST
def updateLeadStage(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    stage = request.POST.get("stage")
    if stage not in Lead.Stage.values:
        return JsonResponse({"error": "Invalid stage"}, status=400)
    lead.stage = stage
    lead.save(update_fields=["stage", "updated_at"])
    return JsonResponse({"ok": True, "stage": lead.stage})

def inquiries(request):
    current_status = request.GET.get("status", "")
    if current_status not in Inquiry.ReviewStatus.values:
        current_status = ""

    inquiry_list = Inquiry.objects.all()
    if current_status:
        inquiry_list = inquiry_list.filter(review_status=current_status)

    counts = dict(
        Inquiry.objects.values_list("review_status")
        .annotate(n=Count("id"))
    )
    filters = [
        {
            "value": "",
            "label": "All",
            "count": sum(counts.values()),
            "active": current_status == "",
        }
    ] + [
        {
            "value": value,
            "label": label,
            "count": counts.get(value, 0),
            "active": current_status == value,
        }
        for value, label in Inquiry.ReviewStatus.choices
    ]

    return render(request, 'inquiries.html', {
        'inquiry_list': inquiry_list,
        'review_choices': Inquiry.ReviewStatus.choices,
        'filters': filters,
        'current_status': current_status,
        'current_url': request.get_full_path(),
    })

@require_POST
def updateInquiryStatus(request, pk):
    inquiry = get_object_or_404(Inquiry, pk=pk)

    back_url = request.POST.get("next", "")
    if not url_has_allowed_host_and_scheme(back_url, allowed_hosts={request.get_host()}):
        back_url = "inquiries"

    status = request.POST.get("review_status")
    if status not in Inquiry.ReviewStatus.values:
        messages.error(request, "Invalid review status.")
        return redirect(back_url)

    inquiry.review_status = status
    inquiry.reviewed_at = (
        None if status == Inquiry.ReviewStatus.PENDING else timezone.now()
    )
    inquiry.save(update_fields=["review_status", "reviewed_at"])
    messages.success(
        request,
        f"{inquiry.sender_name}'s inquiry marked as {inquiry.get_review_status_display().lower()}.",
    )
    return redirect(back_url)

def reports(request):
    return render(request, 'reports.html')

def newCustomer(request):
    return render(request, 'newCustomer.html')

def newTicket(request):
    return render(request, 'newTicket.html')

def customerDetail(req, pk):
    return render(req, 'customerDetail.html')

def ticketDetail(req, pk):
    ticket = get_object_or_404(
        SupportTicket.objects.select_related("customer", "project"),
        pk=pk,
    )
    return render(req, 'ticketDetail.html', {'ticket': ticket})

def client(req):
    return render(req, 'client.html')

def clientAccess(req):
    return render(req, 'clientAccess.html')

def inquiry(request):
    if request.method == "POST":
        form = InquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks! Your inquiry has been received.")
            return redirect("inquiry")
    else:
        form = InquiryForm()
    return render(request, 'inquiry.html', {'form': form})

def clientTicket(req):
    return render(req, 'clientTicket.html')