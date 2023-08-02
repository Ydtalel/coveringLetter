from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, register, user_login, user_logout, user_profile, generate_cover_letter, CoverLetterViewSet, \
    ProcessedCoverLetterViewSet

router = DefaultRouter()
router.register(r'cover_letters', CoverLetterViewSet)
router.register(r'processed_cover_letters', ProcessedCoverLetterViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', user_profile, name='profile'),
    path('generate_cover_letter/', generate_cover_letter, name='generate_cover_letter'),
    path('api/', include(router.urls)),
]
