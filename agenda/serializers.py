from django.contrib.auth.models import User
from datetime import timedelta, datetime, date
from rest_framework import serializers
from django.utils import timezone
from agenda.models import Agendamento

class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = '__all__' 
        
    # data_horario = serializers.DateTimeField()
    # nome_cliente = serializers.CharField(max_length=200)
    # email_cliente = serializers.EmailField()
    # telefone_cliente = serializers.CharField(max_length=20)
    prestador = serializers.CharField()

    def validate_prestador(self, value):
        try:
            prestador_obj = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("username não existe!")
        return prestador_obj

    def validate_data_horario(self,value):
        if value < timezone.now():
            raise serializers.ValidationError("Agendamento nao pode ser feito no passado!")
        return value

    def validate_telefone_cliente(self, value):
        telefone_cliente = value
        if len(telefone_cliente) < 8:
            raise serializers.ValidationError("Número de telefone deve conter mais de 7 dígitos.")
        
        for char in telefone_cliente:
            if char not in "0123456789()-+":
                raise serializers.ValidationError("Caractere de telefone não aceito.")
        if "+" in telefone_cliente and telefone_cliente[0] is not "+":
            raise serializers.ValidationError("O sinal de '+' apenas pode ser utilizado no começo do número de telefone.")
        return value

    # def validate_data_horario(self, value):
    #     for i in Agendamento.objects.all().datetimes("data_horario", "minute"):
    #         if abs(value - i) < timedelta(weeks=0, days=0, hours=0, minutes=30):
    #             print(value - i)
    #             raise serializers.ValidationError("Já existem outros agendamentos neste horário. Escolha outro horário.")
    #     if value.minute != 0 and value.minute != 30:
    #         raise serializers.ValidationError("não são permitidos horários quebrados.")
    #     return value
     
    def validate(self, attrs):
        telefone_cliente = attrs.get("telefone_cliente", "")
        email_cliente = attrs.get("email_cliente", "")
        data_horario = attrs.get("data_horario", "")
        confirmado = ("confirmado", "")

        if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
            raise serializers.ValidationError("Email brasileiro deve estar associado a um numero brasileiro (+55)")
        if data_horario.date() in Agendamento.objects.filter(email_cliente=email_cliente, confirmado=True).dates("data_horario", 'day'):# o ideal seria iterar pelos objetos com email igual e verificar se a data_horario.date() coincide
            raise serializers.ValidationError("Não se pode fazer mais de um agendamento diário.")
        
        for i in Agendamento.objects.all().datetimes("data_horario", "minute"):
            if abs(data_horario - i) < timedelta(weeks=0, days=0, hours=0, minutes=30) and confirmado == True:
                print(data_horario - i)
                raise serializers.ValidationError("Já existem outros agendamentos neste horário. Escolha outro horário.")
        if data_horario.minute != 0 and data_horario.minute != 30:
            raise serializers.ValidationError("não são permitidos horários quebrados.")
 


        return attrs

class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "agendamentos"]

    agendamentos = AgendamentoSerializer(many=True, read_only=True)

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
    #     return instance  .