from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("graph/", views.graph, name="graph"),
    path("graph/<int:ride_id>/", views.graph, name="graph"),
    path("profile/<username>/", views.profile, name="profile"),
    path("build/", views.add_build, name="add_build"),
    path("build/<int:build_id>/edit", views.edit_build, name="edit_build"),
    path("build/<int:build_id>/delete", views.delete_build, name="delete_build"),
]
