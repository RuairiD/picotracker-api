import graphene


class DeveloperType(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    bbs_id = graphene.Int()

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            username=model.username,
            bbs_id=model.bbs_id,
        )

    def __eq__(self, other):
        return all([
            self.id == other.id,
        ])


class GameType(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    image_url = graphene.String()
    bbs_id = graphene.Int()
    stars = graphene.Int()
    comments = graphene.Int()
    rating = graphene.Float()
    time_created = graphene.types.datetime.DateTime()
    developer = graphene.Field(DeveloperType)

    @classmethod
    def from_model(cls, model):
        return cls(
            id=model.id,
            name=model.name,
            image_url=model.image_url,
            bbs_id=model.bbs_id,
            stars=model.stars,
            comments=model.comments,
            rating=model.rating,
            time_created=model.time_created,
            developer=DeveloperType.from_model(model.developer),
        )

    def __eq__(self, other):
        return all([
            self.id == other.id,
        ])
