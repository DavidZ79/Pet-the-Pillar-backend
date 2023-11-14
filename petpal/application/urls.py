app_name="application"
urlpatterns = [
    path('create-application', views.createApplication),
    path('update-application', views.updateApplication),
    path('get-shelter-application-list', views.getShelterApplicationList),
]
# TODO Get application endpoint
