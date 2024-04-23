from django.urls import path, re_path
from .views import file_management, file_download, file_delete, file_view, create_folder, delete_folder, rename_item, file_bulk_delete, file_bulk_download, folder_upload, folder_download, execute_command

urlpatterns = [
    path('', file_management, name='file_management'),
    path('download/<path:path>/', file_download, name='file_download'),  # New URL pattern for downloading files
    path('delete/<path:path>/', file_delete, name='file_delete'),
    path('view/<path:path>/', file_view, name='file_view'),
    path('create_folder/', create_folder, name='create_folder'),
    re_path(r'^delete_folder/(?P<path>.+)/$', delete_folder, name='delete_folder'),  
    path('rename/', rename_item, name='rename_item'),
    path('bulk_delete/', file_bulk_delete, name='file_bulk_delete'),  
    path('bulk_download/', file_bulk_download, name='file_bulk_download'),
    path('folder_upload/', folder_upload, name='folder_upload'),  
    path('download_folder/<path:path>/', folder_download, name='folder_download'),
    path('execute_command/', execute_command, name='execute_command'),  
    # Other patterns...
]
