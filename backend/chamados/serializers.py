from rest_framework import serializers

from .models import Chamado


class ChamadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chamado
        fields = [
            "id",
            "titulo",
            "descricao",
            "status",
            "criado_em",
            "atualizado_em",
        ]
        extra_kwargs = {
            "titulo": {
                "required": True,
                "allow_blank": False,
                "error_messages": {
                    "blank": "O título é obrigatório.",
                    "required": "O título é obrigatório.",
                },
            },
        }
        read_only_fields = [
            "id",
            "criado_em",
            "atualizado_em",
        ]

    def validate_titulo(self, value):
        if not value or not str(value).strip():
            raise serializers.ValidationError("O título é obrigatório.")
        return str(value).strip()
