from django import forms
from .models import Inquiry, Lead, Project
from django.utils import timezone


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ["sender_name", "email", "message"]
        labels = {
            "sender_name": "Your name",
            "email": "Email address",
            "message": "How can we help?",
        }
        widgets = {
            "sender_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Tell us about your project…"}),
        }

    def clean_message(self):
        message = self.cleaned_data["message"].strip()
        if len(message) < 10:
            raise forms.ValidationError("Please write at least a short sentence so we can help.")
        return message



class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "company_name",
            "contact_name",
            "email",
            "description",
            "stage",
            "follow_up_date",
        ]
        labels = {
            "company_name": "Company name",
            "contact_name": "Contact person",
            "email": "Email address",
            "description": "What do they need?",
            "stage": "Pipeline stage",
            "follow_up_date": "Follow-up date",
        }
        widgets = {
            "company_name": forms.TextInput(attrs={"placeholder": "Company or business name"}),
            "contact_name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@company.com"}),
            "description": forms.TextInput(attrs={"placeholder": "e.g. Clinic website and inquiry forms"}),
            "follow_up_date": forms.DateInput(attrs={"type": "date"}),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            "customer",
            "name",
            "description",
            "status",
            "progress",
            "start_date",
            "due_date",
        ]
        labels = {
            "customer": "Customer",
            "name": "Project name",
            "description": "Description",
            "status": "Status",
            "progress": "Progress (%)",
            "start_date": "Start date",
            "due_date": "Due date",
        }
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. Brand website"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "What is this project about?"}),
            "progress": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "start_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
            "due_date": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        }

    def clean_progress(self):
        progress = self.cleaned_data["progress"]
        if progress > 100:
            raise forms.ValidationError("Progress cannot be more than 100%.")
        return progress

    def clean(self):
        cleaned = super().clean()
        start, due = cleaned.get("start_date"), cleaned.get("due_date")
        if start and due and due < start:
            self.add_error("due_date", "The due date cannot be before the start date.")
        if cleaned.get("status") == Project.Status.COMPLETED:
            cleaned["progress"] = 100
        return cleaned

    def save(self, commit=True):
        project = super().save(commit=False)
        if project.status == Project.Status.COMPLETED:
            if not project.completed_at:
                project.completed_at = timezone.localdate()
        else:
            project.completed_at = None
        if commit:
            project.save()
        return project