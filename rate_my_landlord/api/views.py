from django.shortcuts import render
from rest_framework import status
from .models import Landlord, Review
from .serializers import LandlordSerializer, ReviewSerializer, CreateLandlordSerializer, CreateReviewSerializer
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from fuzzywuzzy import fuzz


def main(request):
     return HttpResponse("<h1>Hello</h1>")

# APIView has default get and post methods that we can override
class CreateLandlord(APIView):
     serializer_class = CreateLandlordSerializer
     # Handles a post request from frontend
     def post(self, request, format=None):
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               landlord_first_name = serializer.data.get('first_name')
               landlord_last_name = serializer.data.get('last_name')
          else:
               return Response({'Bad Request': 'couldn\'t deserialize CreateLandlord POST request'}, status=status.HTTP_400_BAD_REQUEST)
          # TODO: handle duplicate values --> what will we use to uniquely identify a landlord?
          new_landlord = Landlord(first_name=landlord_first_name, last_name=landlord_last_name)
          new_landlord.save()
          return Response(LandlordSerializer(new_landlord).data, status=status.HTTP_201_CREATED)

# APIView has default get and post methods that we can override
class GetLandlordById(APIView):
     serializer_class = LandlordSerializer
     lookup_url_kwarg = 'id'
     # Handles a get request from frontend
     def get(self, request, format=None):
          id = request.GET.get(self.lookup_url_kwarg)
          if id != None:
               landlord = Landlord.objects.filter(id=id)
               if len(landlord) > 0:
                    data = LandlordSerializer(landlord[0]).data
                    return Response(data, status=status.HTTP_200_OK)
               return Response({'Landlord Not Found': 'Invalid ID'}, status=status.HTTP_404_NOT_FOUND)
          return Response({'Bad Request': 'ID parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class GetAllLandlords(APIView):
     serializer_class = LandlordSerializer
     def get(self, request, format=None):
          queryset = Landlord.objects.all().order_by('first_name','last_name')
          data = LandlordSerializer(queryset, many=True).data
          return Response(data, status=status.HTTP_200_OK)

class GetMatchingLandlords(APIView):
     serializer_class = LandlordSerializer
     lookup_url_kwarg = 'searchkey'
     def get(self, request, format=None):
          searchKey = request.GET.get(self.lookup_url_kwarg)
          if searchKey != None:
               queryset = filter(
                    lambda landlord: fuzz.partial_ratio(
                              landlord.first_name.lower() + " " + landlord.last_name.lower(),
                              searchKey.lower()
                         ) > 80,
                    Landlord.objects.all().order_by('first_name','last_name')
               )
               data = LandlordSerializer(queryset, many=True).data
               return Response(data, status=status.HTTP_200_OK)
          return Response({'Bad Request': 'searchkey parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class GetAllReviews(APIView):
     serializer_class = ReviewSerializer
     def get(self, request, format=None):
          queryset = Review.objects.all()
          data = ReviewSerializer(queryset, many=True).data
          return Response(data, status=status.HTTP_200_OK)

class GetReviewsForLandlord(APIView):
     serializer_class = ReviewSerializer
     lookup_url_kwarg = 'landlordID'
     def get(self, request, format=None):
          givenID = request.GET.get(self.lookup_url_kwarg)
          if givenID != None:
               givenLandlord = Landlord.objects.get(id=givenID)
               if givenLandlord != None:
                    reviews = givenLandlord.review_set.all()
                    data = ReviewSerializer(reviews, many=True).data
                    return Response(data, status=status.HTTP_200_OK)
               return Response({'Landlord Not Found': 'Invalid ID'}, status=status.HTTP_404_NOT_FOUND)
          return Response({'Bad Request': 'landlordID parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)
     
# APIView has default get and post methods that we can override
class CreateReview(APIView):
     serializer_class = CreateReviewSerializer
     lookup_url_kwarg = 'landlordID'
     # Handles a post request from frontend
     def post(self, request, format=None):
          landlordID = request.GET.get(self.lookup_url_kwarg)
          if landlordID == None:
               return Response({'Bad Request': 'landlordID parameter not found in request', 'request': request.GET}, status=status.HTTP_400_BAD_REQUEST)
          landlord = Landlord.objects.get(id=landlordID)
          if landlord == None:
               return Response({'Landlord Not Found': 'Invalid ID'}, status=status.HTTP_404_NOT_FOUND)
          serializer = self.serializer_class(data=request.data)
          if serializer.is_valid():
               reviewer_name = serializer.data.get('reviewer_name')
               safety_rating = serializer.data.get('safety_rating')
               responsiveness_rating = serializer.data.get('responsiveness_rating')
               transparency_rating = serializer.data.get('transparency_rating')
               organization_rating = serializer.data.get('organization_rating')
               student_friendliness_rating = serializer.data.get('student_friendliness_rating')
               overall_rating = serializer.data.get('overall_rating')
          else:
               return Response({'Bad Request': 'couldn\'t deserialize CreateReview POST request'}, status=status.HTTP_400_BAD_REQUEST)
          # TODO: handle duplicate values --> what will we use to uniquely identify a reviewer?
          new_review = Review(reviewer_name=reviewer_name, landlord=landlord, safety_rating=safety_rating, 
               responsiveness_rating=responsiveness_rating, transparency_rating=transparency_rating,
               organization_rating=organization_rating, student_friendliness_rating=student_friendliness_rating,
               overall_rating=overall_rating)
          new_review.save()
          return Response(ReviewSerializer(new_review).data, status=status.HTTP_201_CREATED)