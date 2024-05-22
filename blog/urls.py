from django.urls import path
from . import views

urlpatterns = [
    path('',views.HomeView.as_view(),name = 'home'),
    path('<slug:post>/',views.DetailPage.as_view(),name = 'detail_page'),
    path('tag/<slug:tag_slug>/',views.CategoryList.as_view(),name = 'post_list_by_category'),
    path('<slug:post>/comment/',views.PostComment.as_view(),name = 'comment'),
    path('comments/by-users/',views.ReviewPage.as_view(),name = 'review'),
    path('contacts/to-admin/',views.ContactPage.as_view(),name = 'contact'),
]