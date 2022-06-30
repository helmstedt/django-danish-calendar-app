from django.urls import path

from . import views

urlpatterns = [
	path('', views.kalindex, name='kal_index'),
	path('<year>', views.kalyear, name='kal_year'),
	path('<year>/<period>', views.kalperiod, name='kal_period'),
]