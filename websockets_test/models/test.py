from collections import OrderedDict

from mongoengine.errors import ValidationError
from mongoengine.fields import DictField

from onyxerp.core.services.base_service import BaseService

from mongoengine import Document, StringField

from websockets_test.models import Mongo


class TestModel(Document, Mongo):
    """
    ExampleModel
    """
    id = StringField(primary_key=True, required=True, default=BaseService.get_uniqid)
    did = StringField(max_length=30, required=True)
    app_id = StringField(max_length=30, required=True)
    language = StringField(max_length=30, required=True)
    label = StringField(required=True)
    value = DictField(required=False, null=True, default={})

    # Table/Collection meta-data
    meta = {'collection': 'test'}

    def __str__(self):
        return str(self.id)

    def self_validate(self, app: object) -> bool:
        """
        Model data validation
        :param app: object
        :return bool
        """
        try:
            super(TestModel, self).validate(True)
            return True
        except ValidationError:
            app['log'].error("Falha na validação do model %s" % (str(self.__class__)), exc_info=True)
            return False

    def self_serialize(self) -> OrderedDict:
        """
        Retona a representação deste Document em OrderedDict e JSON serializable
        :return: OrderedDict
        """
        data = OrderedDict()
        data['id'] = self.id
        data['did'] = self.did
        data['app_id'] = self.app_id
        data['language'] = self.language
        data['label'] = self.label
        data['value'] = self.value

        return data
