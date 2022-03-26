from django.urls import path
from agenda.views import AgendamentoDetail, AgendamentoList
urlpatterns = [
    path('agendamentos/', AgendamentoList.as_view()),
    path('agendamentos/<int:pk>/', AgendamentoDetail.as_view())
]