from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from recomands.models import UserNode, ItemNode, Recommendation, RatingNode
from recomands.serializers import CreateUserItemWithRatingSerializer

from neomodel import db

def calculate_similarity(user1, user2):
    if user1.username == user2.username:
        return 0.0
    query = (
        f"MATCH (u1:UserNode)-[:RATED_ITEM]->(r1:RatingNode)-[:RATED_ITEM]->(i:ItemNode)<-[:RATED_ITEM]-(r2:RatingNode)-[:RATED_BY]->(u2:UserNode) "
        f"WHERE u1.username = '{user1.username}' AND u2.username = '{user2.username}' "
        "RETURN COUNT(DISTINCT i) AS common_items, SUM(r1.value * r2.value) AS weighted_sum"
    )
    result, _ = db.cypher_query(query)
    common_items = result[0][0]
    weighted_sum = result[0][1]
    
    user1_items = set((rating.item.name, rating.value) for rating in user1.ratings.all())
    user2_items = set((rating.item.name, rating.value) for rating in user2.ratings.all())
    
    # Calculate Jaccard similarity
    if not user1_items or not user2_items:
        return 0.0
    
    jaccard_similarity = common_items / len(user1_items.union(user2_items))
    
    # Calculate weighted similarity
    weighted_similarity = weighted_sum / len(user1_items.union(user2_items))
    
    # Combine Jaccard and weighted similarity (you can adjust the weights as needed)
    similarity = 0.7 * jaccard_similarity + 0.3 * weighted_similarity
    
    return similarity



class RecommendationView(APIView):
    def get(self, request, username):
        try:
            user = UserNode.nodes.get(username=username)
        except UserNode.DoesNotExist:
            raise Http404("User does not exist")

        all_users = UserNode.nodes.exclude(username=username)

        # Find most similar user
        most_similar_user = max(all_users, key=lambda other_user: calculate_similarity(user, other_user))

        # Get items rated by the most similar user
        similar_user_rated_item_names = set([item.name for rating in most_similar_user.ratings.all() for item in rating.item.all() if rating.value >= 2.5])

        # Filter items not rated by the current user
        unrated_item_names = set([item.name for rating in user.ratings.all() for item in rating.item.all()])
        unrated_item_names = similar_user_rated_item_names.difference(unrated_item_names)

        # Get recommendations for unrated items
        recommendations = []

        for item_name in unrated_item_names:
            item = ItemNode.nodes.get(name=item_name)
            recommendations.append({"item": item.name})

        return Response({"recommendations": recommendations})


class CreateUserItemWithRatingView(APIView):
    def post(self, request, *args, **kwargs):
        # Get data from the request
        user_data = request.data.get('user')
        item_data = request.data.get('item')
        print(user_data)
        print(item_data)
        rating = request.data.get('rating', 0.0)  # Default rating to 0.0 if not provided

        try:
            existing_user = UserNode.nodes.filter(username=user_data['username']).first()
            if existing_user:
                new_user = existing_user
            else:
                raise UserNode.DoesNotExist  # Raise the exception to handle the case of non-existing user
        except UserNode.DoesNotExist:
            new_user = UserNode(username=user_data['username'])
            new_user.save()

        # Check if the item already exists
        try:
            existing_item = ItemNode.nodes.filter(name=item_data['name']).first()
            if existing_item:
                new_item = existing_item
            else:
                raise ItemNode.DoesNotExist  # Raise the exception to handle the case of non-existing item
        except ItemNode.DoesNotExist:
            new_item = ItemNode(name=item_data['name'])
            new_item.save()

        # Connect the user and item
        new_user.purchases.connect(new_item)

        try:
            rating_relationship = RatingNode.nodes.filter(uid=user_data['username']+'_'+str(rating)).first()
        except:
            rating_relationship = RatingNode(uid=user_data['username']+'_'+str(rating), value=rating)
            rating_relationship.save()  # Save the rating node first
        
        new_user.ratings.connect(rating_relationship)
        # Connect the user and item
        rating_relationship.user.connect(new_user)
        rating_relationship.item.connect(new_item)

        return Response(status=status.HTTP_201_CREATED)