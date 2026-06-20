from django.contrib import admin
from .models import Salarytbl

@admin.register(Salarytbl)
class SalarytblAdmin(admin.ModelAdmin):
	list_display = (
		'user',
		'month',
		'year',
		'present_days',
		'half_days',
		'paid_leaves',
		'absent_days',
		'gross_salary',
		'pf_amount',
		'net_salary',
		'generated_at',
	)
	list_filter = ('year', 'month', 'user__role')
	search_fields = ('user__username', 'user__first_name', 'user__last_name')
