from django.urls import path
from . import views

urlpatterns = [
    path("", views.control_panel, name="dashboard"),
    path("set-washing-delay/", views.set_washing_machine_delay, name="set_washing_machine_delay"),
    path('set-low-cost-time/', views.set_low_cost_time, name='set_low_cost_time'),
]