"""
Módulo com as avalições exclusivas da RecadAPI
 - validate_aval: Validação do campo aval, em AvalModel.
"""

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

status_choices = (("A", "A"), ("D", "D"), ("I", "I"))
sim_nao_choices = (("S", "S"), ("N", "N"))
sync_status_choices = (("A", "A"), ("C", "C"), ("F", "F"))
file_types = ('pdf', 'csv')


def validate_aval(value: str) -> bool:
    """
    Determina se o valor informado para avaliação está na range permitda
    :param value: str
    :raises: ValidationError Se value for menor que 0 e maior que 6
    :return: bool
    """
    try:
        value = int(value)
        if value in range(1, 6):  # Se maior que 0 e menor que 6
            return True
    except ValueError:
        pass

    raise ValidationError(
        _('%(value)s não é uma valor aceito. Informe um número entre 1 e 5!'),
        params={'value': value},
    )


def validate_report_file_type(value: str) -> bool:
    """
    Determina se o valor informado para o campo file_type do dictionary params do ReportModel é valido
    :param value:
    :raises: ValidationError Se value for diferente de pdf e csv
    :return: bool
    """
    for opt in value.split(','):
        if opt not in file_types:
            raise ValidationError(
                _('%(value)s não é uma valor aceito. As opções são {0}!'.format(str(file_types))),
                params={'value': opt},
            )
    return True
