
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/',include('accounts.urls')),
    path('api/v1/auth/',include('social_accounts.urls')),
    path('api/v1/user/',include('user.urls')),

    #* ======= This API Route from Workspace  ====== *#
    path('workspace/', include('workspaces.urls')),
]
