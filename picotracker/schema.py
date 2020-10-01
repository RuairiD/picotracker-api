import graphene

import picotracker.games.schema.query


class Query(picotracker.games.schema.query.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
