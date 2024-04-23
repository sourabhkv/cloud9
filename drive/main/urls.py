from django.urls import path  
from .views import home  
from django.contrib.auth.views import LogoutView  

urlpatterns = [  
    path('', home, name='home'),  
    path('logout/', LogoutView.as_view(), name='logout'),  
    # ... other URL patterns for your main app ...  
]  
