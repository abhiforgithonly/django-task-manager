from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    # Weather endpoints - both with and without trailing slash
    path('api/weather/<str:city>/', views.get_weather, name='weather'),
    path('api/weather/<str:city>', views.get_weather, name='weather_no_slash'),
    
    # Analytics endpoint
    path('api/analytics/', views.task_analytics, name='analytics'),
    
    # Debug and test endpoints
    path('api/test/', views.test_endpoint, name='test'),
    path('api/debug-config/', views.debug_config, name='debug_config'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
]
