from rest_framework.routers import DefaultRouter

from .views import SnippetViewSet, TagViewSet

router = DefaultRouter()
router.register("snippets", SnippetViewSet, basename="snippet")
router.register("tags", TagViewSet, basename="tag")

urlpatterns = router.urls
