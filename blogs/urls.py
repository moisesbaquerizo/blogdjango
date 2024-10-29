from django.urls import path
from blogs import views
from .views import PostDetailWithCommentsView, EditPostView, DeletePostView, OtherPostsView, HomePageView, PostRatingView

app_name = 'blogs'

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('post/<slug:slug>/', PostDetailWithCommentsView.as_view(), name='post'),
    path('post/<slug:slug>/rate/', PostRatingView.as_view(), name='rate_post'),
    path('featured/', views.FeaturedListView.as_view(), name='featured'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('crear-categoria/', views.create_category, name='create_category'),
    path('post/<slug:slug>/edit/', EditPostView.as_view(), name='edit_post'),
    path('post/<slug:slug>/delete/', DeletePostView.as_view(), name='delete_post'),
    path('other-posts/', OtherPostsView.as_view(), name='other_posts'),
]