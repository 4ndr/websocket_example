from collections import OrderedDict

from django.utils import timezone
from mongoengine.errors import ValidationError
from mongoengine.fields import IntField, ListField

from onyxerp.core.services.base_service import BaseService

from mongoengine import (
    Document, StringField, DateTimeField, DictField, EmbeddedDocumentListField, EmbeddedDocument, EmbeddedDocumentField
)

from websockets_test.models import Mongo


class Person(EmbeddedDocument):
    """
    Pessoa
    """
    name = StringField(required=True, max_length=100)
    gender = IntField(required=True, max_value=1)  # 0 = M, 1 = F
    birth = DateTimeField(required=True, default=timezone.now)


class StudantModel(Document, Mongo):
    """
    ExampleModel
    """
    id = StringField(primary_key=True, required=True, default=BaseService.get_uniqid)
    person = EmbeddedDocumentField(Person, required=True)
    appliances = ListField(required=True, default=['OO Programming', 'DBA'])
    grades = DictField(required=False, default={'OO Programming': 9.8, 'DBA': 6.5})
    partners = EmbeddedDocumentListField(Person, required=False)
    data_hora = DateTimeField(required=True, default=timezone.now)
    status = StringField(max_length=1, required=True, default="A")  # Active|Inactive

    # Table/Collection meta-data
    meta = {'collection': 'example'}

    def __str__(self):
        return str(self.id)

    def self_validate(self, app: object) -> bool:
        """
        Model data validation
        :param app: object
        :return bool
        """
        try:
            super(StudantModel, self).validate(True)
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
        data['person'] = self.person
        data['appliances'] = self.appliances
        data['grades'] = self.grades
        data['data_hora'] = self.data_hora.strftime("%Y-%m-%d %H:%M:%S")
        data['status'] = self.status

        return data
