"""
Email notification utilities for the Student Project Tracker.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_milestone_uploaded_email(milestone):
    """
    Send an email notification to the Guide when a Student uploads a new Milestone.
    
    Args:
        milestone: The Milestone object that was uploaded
    """
    project = milestone.project
    guide = project.guide
    
    if not guide or not guide.email:
        return False
    
    subject = f"New Milestone Uploaded: {project.title} - {milestone.get_stage_display()}"
    
    # Render HTML email content
    html_message = render_to_string('emails/milestone_uploaded.html', {
        'project': project,
        'milestone': milestone,
        'guide': guide,
    })
    
    # Plain text fallback
    message = f"""
Hello {guide.name},

A new milestone has been uploaded for the project "{project.title}".

Milestone Details:
- Stage: {milestone.get_stage_display()}
- File: {milestone.file.name}
- Uploaded on: {milestone.id}

Please review the milestone at your earliest convenience.

Best regards,
Student Project Tracker
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[guide.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_evaluation_submitted_email(evaluation):
    """
    Send an email notification to the Student when their Guide submits an Evaluation.
    
    Args:
        evaluation: The Evaluation object that was submitted
    """
    project = evaluation.project
    
    # Get student email from project
    student_emails = []
    if project.student1_email:
        student_emails.append(project.student1_email)
    
    if not student_emails:
        return False
    
    subject = f"Evaluation Submitted: {project.title}"
    
    # Render HTML email content
    html_message = render_to_string('emails/evaluation_submitted.html', {
        'project': project,
        'evaluation': evaluation,
    })
    
    # Plain text fallback
    message = f"""
Hello Team,

Your Guide has submitted an evaluation for the project "{project.title}".

Evaluation Details:
- Rating: {evaluation.get_guide_rating_display()}
- Marks: {evaluation.marks if evaluation.marks else 'Pending'}
- Comments: {evaluation.comments}

{"The project is ready for publication!" if evaluation.publication_status else ""}

Please log in to view the full evaluation details.

Best regards,
Student Project Tracker
    """
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=student_emails,
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False