# myapp/models.py

from django_neomodel import DjangoNode
import neomodel
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, FloatProperty, Relationship

class ItemNode(StructuredNode):
    name = StringProperty(unique_index=True)
    purchased_by = RelationshipTo('UserNode', 'PURCHASED_BY')
    rated_by = RelationshipFrom('UserNode', 'RATED_BY', cardinality=neomodel.OneOrMore)


class RatingNode(StructuredNode):
    uid = StringProperty(unique_index=True)
    value = FloatProperty()

    # Relationship with UserNode and ItemNode
    user = Relationship('UserNode', 'RATED_BY')
    item = Relationship('ItemNode', 'RATED_ITEM')


class UserNode(DjangoNode):
    username = StringProperty(unique_index=True)
    purchases = RelationshipTo(ItemNode, 'PURCHASED')
    ratings = RelationshipTo(RatingNode, 'RATED_BY', cardinality=neomodel.OneOrMore)


class Recommendation(DjangoNode):
    user = RelationshipTo(UserNode, 'FOR_USER')
    item = RelationshipTo(UserNode, 'RECOMMENDED_ITEM')
