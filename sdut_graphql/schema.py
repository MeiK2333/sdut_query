import graphene

from .models import dorm_id_set, EcardQuery, EhallQuery, LibQuery, JwglxtQuery
from .utils import get_fields


class Query(object):
    ecard = graphene.Field(EcardQuery, username=graphene.String(), password=graphene.String(), cookie=graphene.String())
    ehall = graphene.Field(EhallQuery, username=graphene.String(), password=graphene.String(), cookie=graphene.String())
    lib = graphene.Field(LibQuery, username=graphene.String(), password=graphene.String(), cookie=graphene.String())
    jwglxt = graphene.Field(JwglxtQuery, username=graphene.String(), password=graphene.String(), year=graphene.Int(),
                            semester=graphene.Int())

    def resolve_ecard(self, info, **kwargs):
        fields = get_fields(info)

        username = kwargs.get('username')
        password = kwargs.get('password')
        cookie = kwargs.get('cookie', '{}')

        ecard_query = EcardQuery(username=username, password=password, cookie=cookie)

        get_balance = True if 'balance' in fields.keys() else False
        get_consume = True if 'consume' in fields.keys() else False
        ecard_query.get_info(get_balance, get_consume)

        return ecard_query

    def resolve_ehall(self, info, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        cookie = kwargs.get('cookie', '{}')

        ehall_query = EhallQuery(username=username, password=password, cookie=cookie)

        ehall_query.get_info()

        return ehall_query

    def resolve_lib(self, info, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        cookie = kwargs.get('cookie', '{}')

        lib_query = LibQuery(username=username, password=password, cookie=cookie)

        lib_query.get_info()

        return lib_query

    def resolve_jwglxt(self, info, **kwargs):
        username = kwargs.get('username')
        password = kwargs.get('password')
        year = kwargs.get('year')
        semester = kwargs.get('semester')

        jwglxt_query = JwglxtQuery(username=username, password=password, year=year, semester=semester)

        jwglxt_query.get_info()

        return jwglxt_query
