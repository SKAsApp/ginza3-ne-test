from django.shortcuts import render
from django.views.generic import View
from django.http import HttpRequest, HttpResponse
from django.template.context_processors import csrf
from logging import Logger, getLogger


class NamedEntityEntrance(View):
	def __init__(self):
		super( ).__init__( )
		self.__logger: Logger = getLogger("gintes")
	
	def get(self, request: HttpRequest, *args, **kawaii) -> HttpResponse:
		context = { }
		context.update(csrf(request))
		return render(request, "named-entity-entrance.html", context)
