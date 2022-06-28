from django.urls import path
from userstrategies.views import UserStrategyView, AvailableMarginView, CurrentStatusView, UserStrategyPrepareView



urlpatterns = [
    path('',                  UserStrategyView.as_view({'get'     : 'list'}) ,        name="UserStrategyList"),
    path('<int:id>/',         UserStrategyView.as_view({'get'     : 'retrieve',
                                                        'post'    : 'create',
                                                        'patch'   : 'partial_update',
                                                        'delete'  : 'destroy'}) ,     name="UserStrategyDetail"),
    path('<int:id>/prepare/', UserStrategyPrepareView.as_view({'post' : 'create'}) ,  name="prepare"),
    path('availmargin/<str:asset>/<int:id>/', AvailableMarginView.as_view({'get': 'retrieve'}) , name="AvailableMargin"),
    # path('CurrentStatus/<int:secret_id>/',    CurrentStatusView.as_view({'get': 'list'}) ,   name="CurrentStatusView"),
    path('CurrentStatus/<int:secret_id>/',    CurrentStatusView.as_view({'get': 'retrieve'}) ,   name="CurrentStatusView"),
]