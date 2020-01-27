from django.urls import path

from .views.named_entity_entrance import NamedEntityEntrance
from .views.named_entity import NamedEntity


app_name = "gintes"


urlpatterns = [
	path("named-entity/entrance", NamedEntityEntrance.as_view( )),
	path("named-entity", NamedEntity.as_view( ))
]
