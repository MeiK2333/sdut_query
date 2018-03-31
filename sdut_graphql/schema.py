from django.contrib.auth.models import User as UserModel

import graphene
from graphene_django.types import DjangoObjectType

from .models import dorm_id
from .spriders import AuthServer, Ecard, Ehall, Lib


class Query(object):
    grade = graphene.Float(username=graphene.String(), password=graphene.String())

    def resolve_grade(self, info, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        a = AuthServer()
        a.login(username, password)

        e = Ehall(a)
        e.login()
        c = Ecard(e)
        c.login()
        return float(c.balance()['balance'][:-3])
