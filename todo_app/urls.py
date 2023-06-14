from django.urls import path
from .views import DataView, Details
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    # path("view/",my_post_view),
    path("post/",Details.as_view()),
    path('items/<int:id>/', Details.as_view(), name='delete_item'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('data/', DataView.as_view(), name='data'),

   
]