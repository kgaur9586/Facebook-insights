from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework import status

from rest_framework import viewsets, filters, pagination

from insights.scrapper import FacebookScraper
from .models import Page, Post, SocialMediaUser
from .serializers import PageSerializer, PostSerializer, FollowerSerializer

class StandardPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category']
    pagination_class = StandardPagination
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by followers range
        min_followers = self.request.query_params.get('min_followers')
        max_followers = self.request.query_params.get('max_followers')
        
        if min_followers and max_followers:
            queryset = queryset.filter(
                followers_count__range=(min_followers, max_followers)
            )
        
        # Search by name or category
        search_term = self.request.query_params.get('search')
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) |
                Q(category__icontains=search_term)
            )
        
        return queryset.order_by('-updated_at')
    def list(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        if username:
            try:
                # Check if the page already exists in the database
                page = Page.objects.get(username=username)
            except Page.DoesNotExist:
                try:
                    scraper = FacebookScraper()
                    data = scraper.scrape_page(username)
                    
                    # Save even if some parts failed
                    if data['page']:
                        scraper.save_to_db(data)
                        
                        # Add warnings if posts or followers are missing
                        if not data['posts']:
                            data['warning'] = "Could not retrieve posts"
                        if not data['followers']:
                            data['warning'] = "Could not retrieve followers"
                        
                        # Serialize and return the created data
                        serializer = self.get_serializer(Page.objects.get(username=username))
                        return Response(serializer.data)
                    else:
                        # Handle missing page data
                        return Response(
                            {"error": "Failed to retrieve page data"},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE
                        )
                    
                except Exception as e:
                    # Return partial data in case of error
                    return Response(
                        {
                            "status": "partial",
                            "data": data if 'data' in locals() else None,
                            "error": str(e)
                        },
                        status=status.HTTP_206_PARTIAL_CONTENT
                    )
        # Default behavior for listing all pages
        return super().list(request, *args, **kwargs)

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PostSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        return Post.objects.filter(page_id=self.kwargs['page_pk']).order_by('-timestamp')

class FollowerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowerSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        return SocialMediaUser.objects.filter(following_pages=self.kwargs['page_pk'])