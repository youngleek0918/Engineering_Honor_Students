from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StudentSemesterStatus

@receiver(post_save, sender=StudentSemesterStatus)
def fill_in_overall_fields(sender, instance, created, raw, *args, **kwargs):
    if (created or raw) and instance.predecessor:
        prd = instance.predecessor

        instance.overall_hours_attempted = prd.overall_hours_attempted + prd.hours_attempted
        instance.overall_hours_earned = prd.overall_hours_earned + prd.hours_earned
        instance.overall_hours_passed = prd.overall_hours_passed + prd.hours_passed
        instance.overall_quality_points = prd.overall_quality_points + prd.quality_points
        instance.overall_gpa = prd.overall_gpa + prd.semester_gpa
        instance.previous_status = prd.status

        instance.save()
