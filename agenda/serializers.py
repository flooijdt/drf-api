from datetime import timedelta
from rest_framework import serializers
from django.utils import timezone
from agenda.models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = [
            "id",
            "data_horario",
            "nome_cliente",
            "email_cliente",
            "telefone_cliente",
        ]

    # data_horario = serializers.DateTimeField()
    # nome_cliente = serializers.CharField(max_length=200)
    # email_cliente = serializers.EmailField()
    # telefone_cliente = serializers.CharField(max_length=20)

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "Agendamento nao pode ser feito no passado!"
            )
        return value

    def validate_telefone_cliente(self, value):
        telefone_cliente = value
        if len(telefone_cliente) < 8:
            raise serializers.ValidationError(
                "Número de telefone deve conter mais de 7 dígitos."
            )

        for char in telefone_cliente:
            if char not in "0123456789()-+":
                raise serializers.ValidationError("Caractere de telefone não aceito.")
        if "+" in telefone_cliente and telefone_cliente[0] is not "+":
            raise serializers.ValidationError(
                "O sinal de '+' apenas pode ser utilizado no começo do número de telefone."
            )
        return value

    def validate_data_horario(self, value):
        for i in Agendamento.objects.all().datetimes("data_horario", "minute"):
            if value - i < timedelta(minutes=30):
                raise serializers.ValidationError(
                    "Já existem outros agendamentos neste horário. Escolha outro horário."
                )
        return value

    def validate(self, attrs):
        telefone_cliente = attrs.get("telefone_cliente", "")
        email_cliente = attrs.get("email_cliente", "")
        data_horario = attrs.get("data_horario", "")

        if (
            email_cliente.endswith(".br")
            and telefone_cliente.startswith("+")
            and not telefone_cliente.startswith("+55")
        ):
            raise serializers.ValidationError(
                "Email brasileiro deve estar associado a um numero brasileiro (+55)"
            )

        if data_horario in Agendamento.objects.filter(
            email_cliente=email_cliente
        ).dates(
            "data_horario", "day"
        ):  # o ideal seria iterar pelos objetos com email igual e verificar se a data_horario.date() coincide
            raise serializers.ValidationError(
                "Não se pode fazer mais de um agendamento diário."
            )

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
    #     return instance  .
