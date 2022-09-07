from django.urls import path

from gallery.views import home, home_image_id, home_image_id_action


urlpatterns = [
    path('home', home, name="home"),
    path('home?image_id=<int:selected_image_id>', home_image_id, name="home_image_by_id"),
    path('home?image_id=<int:selected_image_id>?image_action=<str:image_action>',
         home_image_id_action, name="home_image_by_id_by_action"),
]
