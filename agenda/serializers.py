from rest_framework import serializers
from django.utils import timezone
from agenda.models import Agendamento

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = ["id", "data_horario", "nome_cliente", "email_cliente", "telefone_cliente"]
        
    # data_horario = serializers.DateTimeField()
    # nome_cliente = serializers.CharField(max_length=200)
    # email_cliente = serializers.EmailField()
    # telefone_cliente = serializers.CharField(max_length=20)

    def validate_data_horario(self,value):
        if value < timezone.now():
            raise serializers.ValidationError("Agendamento nao pode ser feito no passado!")
        return value
    
    def validate(self, attrs):
        telefone_cliente = attrs.get("telefone_cliente", "")
        email_cliente = attrs.get("email_cliente", "")

        if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
            raise serializers.ValidationError("Email brasileiro deve estar associado a um numero brasileiro (+55)")
        return attrs

    # def create(self, validated_data):
    #     agendamento = Agendamento.objects.create(
    #         data_horario = validated_data["data_horario"],
    #         nome_cliente = validated_data["nome_cliente"],
    #         email_cliente = validated_data["email_cliente"],
    #         telefone_cliente = validated_data["telefone_cliente"],
    #     )
    #     return agendamento

    # def update(self, instance, validated_data):
    #     instance.data_horario = validated_data.get("data_horario", instance.data_horario)
    #     instance.nome_cliente = validated_data.get("nome_cliente", instance.nome_cliente)
    #     instance.email_cliente = validated_data.get("email_cliente", instance.email_cliente)
    #     instance.telefone_cliente = validated_data.get("telefone_cliente", instance.telefone_cliente)
    #     instance.save()
    #     return instance
    # .