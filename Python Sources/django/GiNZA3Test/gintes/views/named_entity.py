from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpRequest, HttpResponse
from django.template.context_processors import csrf
from logging import Logger, getLogger
from typing import List
from functools import reduce
from ginza import Japanese
from spacy.tokens.doc import Doc
from spacy import displacy
from multiprocessing import Process
from time import sleep
from os import kill
import timeout_decorator
import signal
import spacy

from ..models.fileio import FileIO
from ..models.named_entity_recognizer import NamedEntityRecognizer


class NamedEntity(View):
	def __init__(self):
		super( ).__init__( )
		self.__logger: Logger = getLogger("gintes")
		self.__fileio: FileIO = FileIO( )
	
	def post(self, request: HttpRequest, *args, **kawaii) -> HttpResponse:
		view_mode: str = request.POST.get(key = "view", default = "displacy")
		content_string: str = request.POST.get(key = "content", default = "")
		content: str = self.__fileio.replace_half_to_full_width(self.__fileio.replace_sign_to_full_width(content_string)).replace("\r\n", "\n")
		has_error: bool = len(content) < 1
		if view_mode == "displacy":
			self.__logger.info("displacyで固有表現を表示します。")
			redirect_to: str = "http://localhost:11315"
			result: str = self.__ginza(content)
			self.__logger.info("結果：\n" + result)
			return self.__response(request, has_error, result, redirect_to)
		if view_mode == "独自":
			self.__logger.info("独自で固有表現を表示します。")
			result: str = self.__ginza_original(content)
			self.__logger.info("結果：\n" + result)
			return self.__response(request, result = result)
	
	def __ginza(self, content: str) -> str:
		japanese_processor: Japanese = spacy.load('ja_ginza')
		doc: Doc = japanese_processor(content)
		# resultはログでしか使われない悲しい存在。
		results = list(
			map(lambda sent:
				reduce(lambda x, y: x + "\r\n" + y,
					map(lambda token: str(token.i) + "\t" + str(token.orth_) + "\t" + str(token.tag_) + "\t" + str(token.dep_), sent)), doc.sents))
		# displacyはWebサーバーとして動作する。WebサーバーからWebサーバーを呼ぶというヤバい（あまりオススメしない）構成になっている。そのため，別プロセスで呼び，リダイレクト後にそのプロセスを終了（timeout_decoratorと，予備でstop_disp）するようにしている。
		self.__disprocess = Process(target = self.disp, args = (doc,))
		stop_prpcess: Process = Process(target = self.stop_disp)
		self.__disprocess.daemon = True
		self.__disprocess.start( )
		stop_prpcess.start( )
		return self.ginza_result(results)
	
	def ginza_result(self, results: List[str]) -> str:
		sleep(5.0)
		self.__logger.debug("応答します")
		return "\r\n".join(results)
	
	@timeout_decorator.timeout(10.0)
	def disp(self, doc):
		self.__logger.info("displacyを起動します。\n5秒後に転送します。")
		# ポート番号はwellknown（1〜1024）とephemeral（49152〜65535）以外なら何でも良い。例では「いい みりてこ」にしている。みりてことはアイドルグループ「わーすた」のメンバーである。https://twitter.com/tws_miri
		displacy.serve(doc, style = "ent", port = 11315, host = "127.0.0.1")
	
	def stop_disp(self):
		pid: int = self.__disprocess.pid
		sleep(11.0)
		self.__logger.debug("displacyを停止します。　pid：" + str(pid))
		kill(pid, signal.SIGKILL)
	
	def __ginza_original(self, content: str) -> str:
		output: str = NamedEntityRecognizer(content).pre_process( ).ginza_ne( ).after_process( ).string
		return output
	
	def __response(self, request: HttpRequest, has_error: bool = False, result: str = "", redirect2: str = "") -> HttpResponse:
		context = {
			"error": has_error,
			"result": result
		}
		context.update(csrf(request))
		if len(redirect2) > 1:
			self.__logger.debug("リダイレクトします。")
			return redirect(redirect2, permanent = False)
		self.__logger.debug("応答します。")
		return render(request, "named-entity.html", context) if not has_error else render(request, "named-entity.html", context, status = 500)
