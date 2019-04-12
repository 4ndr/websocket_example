import json

from django.shortcuts import render
from django.utils.safestring import mark_safe
from onyxerp.core.services.base_service import BaseService

from websockets_test.models.test import TestModel


class DataServiceV2(BaseService):
    """
    Classe de interface entre o Controller e os Services/Models relativos ao input de dados de exemplo
    """
    app = object()

    def __init__(self, app: object()) -> None:
        """
        Construtor
        :param: app object Rinzler Framework object
        :rtype: None
        """
        super(DataServiceV2, self).__init__(app)
        self.app = app

    @staticmethod
    def index() -> dict:
        """
        Executa a ação especificada para o end-point aqui.
        :rtype: dict
        """

        retorno = {
            'hello': "World"
        }

        return retorno

    @staticmethod
    def chat(request) -> dict:
        return render(request, 'index.html', {})

    @staticmethod
    def room(request, room_name):
        return render(request, 'room.html', {
            'room_name_json': mark_safe(json.dumps(room_name))
        })
