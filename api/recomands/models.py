# myapp/models.py

from django_neomodel import DjangoNode
import neomodel
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, FloatProperty, Relationship


class RatingNode(StructuredNode):
    uid = StringProperty(unique_index=True)
    value = FloatProperty()

    # Relationship with UserNode and ItemNode
    user = RelationshipTo('UserNode', 'RATED_BY')
    item = RelationshipTo('ItemNode', 'RATED_ITEM')

class ItemNode(StructuredNode):
    name = StringProperty(unique_index=True)
    purchased_by = RelationshipTo('UserNode', 'PURCHASED_BY')
    rated_by = Relationship('RatingNode', 'RATED_ITEM', cardinality=neomodel.OneOrMore)

class UserNode(StructuredNode):
    username = StringProperty(unique_index=True)
    purchases = RelationshipTo(ItemNode, 'PURCHASED')
    ratings = Relationship(RatingNode, 'RATED_BY', cardinality=neomodel.OneOrMore)


class Recommendation(DjangoNode):
    user = RelationshipTo(UserNode, 'FOR_USER')
    item = RelationshipTo(UserNode, 'RECOMMENDED_ITEM')
