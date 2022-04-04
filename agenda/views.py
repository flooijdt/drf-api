from django.contrib.auth.models import User
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from rest_framework import generics, permissions
# Create your views here.

class IsOwnerOrCreateOnly(permissions.BasePermission):# /api/agendamentos/?username=flooijdt
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        username = request.query_params.get("username", None)
        if request.user.username == username:
            return True
        return False

class IsPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True
        return False

class AgendamentoList(generics.ListCreateAPIView):#/api/agendamentos/
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]
    
    def get_queryset(self):
        username = self.request.query_params.get("username", None)
        confirmado = self.request.query_params.get("confirmado", None)
        queryset = Agendamento.objects.filter(prestador__username=username, confirmado=confirmado)
        return queryset

class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):#/api/agendamentos/?username=flooijdt
   permission_classes = [IsPrestador]
   queryset = Agendamento.objects.all()
   serializer_class = AgendamentoSerializer
#    permission_classes = [IsOwnerOrCreateOnly]

class PrestadorList(generics.ListAPIView):
    serializer_class = PrestadorSerializer
    queryset = User.objects.all()

# @api_view(http_method_names=["GET", "PATCH", "DELETE"])
# def agendamento_detail(request, id):
#     if request.method == "GET":
#         obj = get_object_or_404(Agendamento, id=id)
#         serializer = AgendamentoSerializer(obj)
#         return JsonResponse(serializer.data)
#     if request.method == "PATCH":
#         obj = get_object_or_404(Agendamento, id=id)
#         serializer = AgendamentoSerializer(obj, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=200)
#         return JsonResponse(serializer.errors, status=400)
#     if request.method == "DELETE":
#         obj = get_object_or_404(Agendamento, id=id)
#         # obj.delete()
#         obj.cancelado = True
#         obj.save()
#         return Response(status=204)
# @api_view(http_method_names=["GET", "POST"])
# def agendamento_list(request):
#     if request.method == "GET":
#         qs = Agendamento.objects.all().filter(cancelado=False)
#         serializer = AgendamentoSerializer(qs, many=True)
#         return JsonResponse(serializer.data, safe=False)
    
#     if request.method == "POST":
#         data = request.data # {"nome_cliente": "table"...}
#         serializer = AgendamentoSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)