from collections import OrderedDict

from django.http.request import HttpRequest
from django.views.generic import TemplateView

from rinzler.core.response import Response

from websockets_test.services.data_service_v2 import DataServiceV2


class DataControllerV2(TemplateView):
    """
    Controller do namespace de end-points /v2/data desta API
    end-points:
     - GET /{app_id}/
    """

    api_name = "MetaAPI"
    service = object()

    def connect(self, app: dict):
        """
        Método responsável pelo acoplamento de um end-point a um callback service.
        :param app: Rinzler' object
        :return: object
        """
        self.service = DataServiceV2(app)

        router = app['router']

        router.get("/data/", self.index)
        router.get("/", self.chat)
        router.get("/{room_name}/", self.room)

        return app

    def index(self, request: HttpRequest, app: dict, **params: dict):
        """
        De acordo com a documentação em
        :param request: HttpRequest
        :param app: object
        :param params: dict
        :return: Response
        """
        try:

            resultado = self.service\
                .index()

            response = OrderedDict()
            response['success'] = True
            response["data"] = {
                self.api_name: resultado
            }

            return Response(response, content_type="application/json")
        except RuntimeError as e:
            app['log'].error("Exception: %s" % str(e), exc_info=True)
            return Response(None, content_type="application/json", status=500)

    def chat(self, request: HttpRequest, app: dict, **params: dict):
        """
        De acordo com a documentação em
        :param request: HttpRequest
        :param app: object
        :param params: dict
        :return: Response
        """
        try:

            resultado = self.service\
                .chat(request)

            return resultado
        except RuntimeError as e:
            app['log'].error("Exception: %s" % str(e), exc_info=True)
            return Response(None, content_type="application/json", status=500)

    def room(self, request: HttpRequest, app: dict, **params: dict):
        """
        De acordo com a documentação em
        :param request: HttpRequest
        :param app: object
        :param params: dict
        :return: Response
        """
        try:

            room_name = params['room_name']

            resultado = self.service\
                .room(request, room_name)

            return resultado
        except RuntimeError as e:
            app['log'].error("Exception: %s" % str(e), exc_info=True)
            return Response(None, content_type="application/json", status=500)
