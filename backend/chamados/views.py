from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chamado
from .serializers import ChamadoSerializer

STATUS_VALIDOS = {choice.value for choice in Chamado.Status}


class ChamadoListCreateView(generics.ListCreateAPIView):
    serializer_class = ChamadoSerializer

    def get_queryset(self):
        queryset = Chamado.objects.all().order_by("-criado_em")
        status_param = self.request.query_params.get("status")
        if status_param is None:
            return queryset
        if status_param not in STATUS_VALIDOS:
            raise ValidationError(
                {
                    "status": "Status inválido. Use ABERTO, EM_ANDAMENTO ou CONCLUIDO."
                }
            )
        return queryset.filter(status=status_param)


class ChamadoDetailView(generics.RetrieveUpdateAPIView):
    queryset = Chamado.objects.all()
    serializer_class = ChamadoSerializer


class IndicadoresView(APIView):
    def get(self, request):
        queryset = Chamado.objects.all()
        return Response(
            {
                "total": queryset.count(),
                "abertos": queryset.filter(status=Chamado.Status.ABERTO).count(),
                "em_andamento": queryset.filter(
                    status=Chamado.Status.EM_ANDAMENTO
                ).count(),
                "concluidos": queryset.filter(
                    status=Chamado.Status.CONCLUIDO
                ).count(),
            }
        )
