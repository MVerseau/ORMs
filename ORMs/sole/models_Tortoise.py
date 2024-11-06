from tortoise.models import Model
from tortoise import fields


class T_Buyer(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=256)
    balance = fields.DecimalField(decimal_places=2, max_digits=9)
    age = fields.IntField()

    class Meta:
        table = 'sole_buyer'


class T_Game(Model):
    title = fields.CharField(max_length=100)
    cost = fields.DecimalField(decimal_places=2, max_digits=8)
    size = fields.DecimalField(decimal_places=1, max_digits=4)
    description = fields.TextField()
    age_limited = fields.BooleanField(default=False)
    buyer = fields.CharField(max_length=100, default=' ')

    class Meta:
        table = 'sole_game'
