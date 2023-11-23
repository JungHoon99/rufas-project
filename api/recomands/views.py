from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from recomands.models import UserNode, ItemNode, Recommendation, RatingNode
from recomands.serializers import CreateUserItemWithRatingSerializer
import json
import math
import requests

from neomodel import db

def scale_to_minus_one_one(x):
    x -= 10
    # 아크탄젠트 함수를 사용하여 -π/2에서 π/2 사이의 각도를 구함
    angle = math.atan(x)
    
    # 구한 각도를 -1에서 1 사이로 스케일링
    scaled_value = (2 / math.pi) * angle
    
    return scaled_value


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
        similar_user_rated_item_names = set([item.name for rating in most_similar_user.ratings.all() for item in rating.item.all() if rating.value >= 2.3])

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
            existing_user = UserNode.nodes.filter(username=user_data).first()
            if existing_user:
                new_user = existing_user
            else:
                raise UserNode.DoesNotExist  # Raise the exception to handle the case of non-existing user
        except UserNode.DoesNotExist:
            new_user = UserNode(username=user_data)
            new_user.save()

        # Check if the item already exists
        try:
            existing_item = ItemNode.nodes.filter(name=item_data).first()
            if existing_item:
                new_item = existing_item
            else:
                raise ItemNode.DoesNotExist  # Raise the exception to handle the case of non-existing item
        except ItemNode.DoesNotExist:
            new_item = ItemNode(name=item_data)
            new_item.save()

        # Connect the user and item
        new_user.purchases.connect(new_item)

        try:
            rating_node = RatingNode.nodes.get(uid = user_data+'_'+item_data)
            if rating_node:
                # 이미 해당 사용자가 해당 아이템에 대한 평가가 존재하는 경우
                current_value = rating_node.value
                new_value = current_value + rating  # 더하거나 빼고 싶은 값 설정
                if(new_value>5):
                    rating_node.value = 5
                else:    
                    rating_node.value = new_value
            else:
                # 해당 사용자가 해당 아이템에 대한 평가가 없는 경우
                new_value = rating  # 더하거나 빼고 싶은 값 설정
                rating_node = RatingNode(uid = user_data+'_'+item_data, value=new_value)
        except RatingNode.DoesNotExist:
            # 해당 사용자 또는 아이템이 존재하지 않는 경우
            new_value = rating  # 더하거나 빼고 싶은 값 설정
            rating_node = RatingNode(uid = user_data+'_'+item_data, value=new_value)
        
        rating_node.save()

        rating_node.user.connect(new_user)
        rating_node.item.connect(new_item)

        new_user.ratings.connect(rating_node)

        return Response(status=status.HTTP_201_CREATED)
    
class track(APIView):
    def post(self, request, *args, **kwargs):
        s = json.loads(request.body.decode('utf-8'))
        print(s)
        if("http://127.0.0.1:8080/mall/" in s['링크']):
            s['링크'] = s['링크'].replace("http://127.0.0.1:8080/mall/", "")
        
        if("http://127.0.0.1:8080/mall/" in s['링크 클릭']):
            s['링크 클릭'] = s['링크 클릭'].replace("http://127.0.0.1:8080/mall/", "")
        if('buy' in s['링크 클릭']):
            id = s['링크 클릭'].split('/')[1]
            value = s['체류 시간']/1000
            user_id = s['user_id']
            value = scale_to_minus_one_one(value)
            value = value + 3
            item = "http://127.0.0.1:8080/mall/detail/"+str(id)+"/"
            url = "http://127.0.0.1:8000/recomand/create-user-item/"
            data = {"user":user_id, "item": item, "rating": value}
            response = requests.post(url, json=data)
            print(response.status_code)
            pass
        if('cart' in s['링크 클릭']):
            id = s['링크 클릭'].split('/')[1]
            value = s['체류 시간']/1000
            user_id = s['user_id']
            value = scale_to_minus_one_one(value)
            value = value + 2
            item = "http://127.0.0.1:8080/mall/detail/"+str(id)+"/"
            url = "http://127.0.0.1:8000/recomand/create-user-item/"
            data = {"user":user_id, "item": item, "rating": value}
            response = requests.post(url, json=data)
            print(response.status_code)
            pass
        if("detail" in s['링크 클릭']):
            id = s['링크 클릭'].split('/')[1]
            value = s['체류 시간']/1000
            user_id = s['user_id']
            value = scale_to_minus_one_one(value)
            value = value + 0.5
            item = "http://127.0.0.1:8080/mall/detail/"+str(id)+"/"
            url = "http://127.0.0.1:8000/recomand/create-user-item/"
            data = {"user":user_id, "item": item, "rating": value}
            response = requests.post(url, json=data)
            print(response.status_code)
        

        return Response({"recommendations": s})