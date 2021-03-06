import uuid, json
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.serializers.json import DjangoJSONEncoder
from django.core.exceptions import ValidationError
from django.conf import settings
def validate_json(value):
    try:
        json.loads(value)
    except:
        raise ValidationError(u'%s is not an Valid Json - ' % value)
# Create your models here.

class Contract(models.Model):
    """
    Identifier - an autogenerated random identifier for the contract
    Amount - the amount owed to the bank
    Interest rate - the monthly interest rate of the contract
    IP Address - IP of the contract submitter
    Submission date - the date the contract was submitted
    Bank - information about the bank for which the money is owed, can be simple text (e.g., name, tax id, etc.) or a separate model altogether
    Customer Metadata - information about the individual that owes the money, can be simple text (e.g., name, email, tax id, etc.) or a separate model altogether
    """
    #fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(default=0.00, max_digits=11, decimal_places=2, verbose_name="Amount owed to the Bank")
    interest_rate = models.DecimalField(default=0.000, max_digits=7, decimal_places=3, verbose_name="Monthly interest Rate")
    ip_address = models.GenericIPAddressField(protocol='both', unpack_ipv4=False, verbose_name="IP of the contract Submitter")
    submission_date = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Submission Date")
    bank = JSONField(encoder=DjangoJSONEncoder, default=dict,validators=[validate_json],verbose_name="Bank Information")
    customer_metadata = JSONField(encoder=DjangoJSONEncoder, default=dict,validators=[validate_json],verbose_name="Customer Metadata")
    # foreign keys
    owner_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User Owner")

    #Meta
    class Meta:
        verbose_name = _("Contract")
        verbose_name_plural = _("Contracts")
        ordering = ['-submission_date']

    #functions
    def __str__(self):
        return str(self.id)
