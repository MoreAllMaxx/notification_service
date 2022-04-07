from rest_framework import routers

from .views import DispatchAPIViewSet, MessageAPIViewSet, ClientAPIViewSet, TagAPIViewSet

router = routers.DefaultRouter()
router.register(r'tag', TagAPIViewSet)
router.register(r'clients', ClientAPIViewSet)
router.register(r'dispatch', DispatchAPIViewSet)
router.register(r'messages', MessageAPIViewSet)

urlpatterns = router.urls
