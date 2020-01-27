from logging import Logger, getLogger
from typing import List, Tuple, Optional, Iterator, Pattern
from subprocess import Popen, PIPE
import re

from .fileio import FileIO


class NamedEntityRecognizer:
	"""固有表現抽出器です。"""
	
	def __init__(self, input_string: str = "", logger: Optional[Logger] = None):
		"""固有表現抽出器です。\n
		やりたい処理を.で繋げて，.stringまたは.string_listで最後の処理結果を見れます。\n
		:param input_string: 処理対象の文字列。"""
		self.__logger: Logger = getLogger("gintes") if logger is None else logger
		self.__fileio: FileIO = FileIO(self.__logger)
		self.__input_string: str = input_string
		self.__string: str = input_string
		self.__string_list: List[str] = list( )
		self.__logger.debug("固有表現抽出器が生成されました。")
	
	@property
	def input_string(self) -> str:
		""":return: 初期状態の文字列を返します。"""
		return self.__input_string
	
	@property
	def string(self) -> str:
		""":return: NamedEntityRecognizerが現在保持している文字列。"""
		return self.__string
	
	@string.setter
	def string(self, value: str):
		"""処理対象文字列を初期化します。\n
		:param value: 初期化する文字列。"""
		self.__set_string(value)
	
	def __set_string(self, value: str) -> str:
		if len(value) < 1:
			return ""
		self.__string = value
		self.__input_string = value
		self.__logger.debug("初期文字列がセットされました。")
		return value
	
	@property
	def string_list(self) -> List[str]:
		""":return: NamedEntityRecognizerが現在保持している文字列リスト。"""
		return self.__string_list
	
	def __set_string_list(self, value: Optional[List[str]]) -> List[str]:
		if value is None:
			return list( )
		if len(value) < 1:
			return list( )
		self.__string_list = value
		return value
	
	def __list2string(self):
		"""self.__string_listから改行コードCRLFを追加し，self.__stringに代入します。\n
		:return: 処理後の自身（NamedEntityRecognizerインスタンス）。"""
		self.__string = "\r\n".join(self.__string_list)
		return self
	
	def pre_process(self, input_string: str = ""):
		"""固有表現抽出のための前処理をします。\n
		:param input_string: 処理対象文字列。※ 初期化する場合のみ渡してください。
		:return: 処理後の自身（NamedEntityRecognizerインスタンス）。"""
		self.__set_string(input_string)
		self.__logger.debug("前処理をします。")
		self.__string = self.__fileio.replace_half_to_full_width(self.__fileio.replace_sign_to_full_width(self.__string)).replace("\r\n", "\n")
		return self
	
	def cabocha_ne(self, input_string: str = ""):
		"""CaboChaを呼び出して，固有表現を抽出します。\n
		:param input_string: 前処理済みの処理対象文字列。※ 初期化する場合のみ渡してください。
		:return: 処理後の自身（NamedEntityRecognizerインスタンス）。"""
		self.__set_string(input_string)
		self.__logger.debug("CaboCha 固有表現を抽出します。")
		process: Popen = Popen(["cabocha", "-n", "1", "-f1"], stdin = PIPE, stdout = PIPE)
		self.__string_list = process.communicate(self.__string.encode(encoding = "utf-8"))[0].decode(encoding = "utf-8").splitlines( )
		return self.__list2string( )
	
	def ginza_ne(self, input_string: str = ""):
		"""GiNZAを実行して，固有表現を抽出します。\n
		:param input_string: 前処理済みの処理対象文字列。※ 初期化する場合のみ渡してください。
		:return: 処理後の自身（NamedEntityRecognizerインスタンス）"""
		self.__set_string(input_string)
		self.__logger.debug("G 固有表現を抽出します。")
		process: Popen = Popen(["ginza", "-f", "1"], stdin = PIPE, stdout = PIPE)
		result: List[str] = process.communicate(self.__string.encode(encoding = "utf-8"))[0].decode(encoding = "utf-8").splitlines( )
		# GiNZA v2.xの出力をCaboChaと同じタグにする。v3.xだと意味ない？
		self.__string_list = list(map(self.__ginza2_to_irex_ne, result))
		return self.__list2string( )
	
	def __ginza2_to_irex_ne(self, ginza2: str) -> str:
		return ginza2.replace("\tB-ORG", "\tB-ORGANIZATION")\
			.replace("\tI-ORG", "\tI-ORGANIZATION")\
			.replace("\tB-LOC", "\tB-LOCATION")\
			.replace("\tI-LOC", "\tI-LOCATION")\
			.replace("\tB-PRODUCT", "\tB-ARTIFACT")\
			.replace("\tI-PRODUCT", "\tI-ARTIFACT")
	
	def after_process(self, string_list: Optional[List[str]] = None):
		"""CaboCha／GiNZAの解析結果をハイライト表示に便利な独自形式に整形します。\n
		:param string_list: CaboChaの実行結果。※ 初期化する場合のみ渡してください。
		:return: 処理後の自身（NamedEntityRecognizerインスタンス）。"""
		self.__set_string_list(string_list)
		self.__logger.debug("後処理をします。")
		# 漢数字が出てくるのか忘れたけど，なんか昔付けてたので，そのまま残してみた。
		pattern_id: Pattern = re.compile("^\\* (([0-9])|([〇一二三四五六七八九十百])){1,} -{0,1}(([0-9])|([〇一二三四五六七八九十百])){1,}D (([0-9])|([〇一二三四五六七八九十百])){1,}/(([0-9])|([〇一二三四五六七八九十百])){1,} -{0,1}(([0-9])|([〇一二三四五六七八九十百])){1,}.(([0-9])|([〇一二三四五六七八九十百])){1,}")
		# どうせアンダーバーは出てこないから，かわいらしい正規表現に。
		pattern_pos1: Pattern = re.compile("\t([^_]+?),([^_]+?),([^_]+?),[^_]+?,[^_]+?,[^_]+?,[^_]+?,[^_]+?,[^_]+?\t")
		pattern_pos2: Pattern = re.compile("\t([^_]+?),([^_]+?),([^_]+?),[^_]+?,[^_]+?,[^_]+?,[^_]+?\t")
		removed_ids: Iterator[str] = map(lambda result: pattern_id.sub("", result), self.__string_list)
		removed_poses1: Iterator[str] = map(lambda id: pattern_pos1.sub("\t\\1-\\2-\\3\t", id), removed_ids)
		removed_poses2: Iterator[str] = map(lambda pos1: pattern_pos2.sub("\t\\1-\\2-\\3\t", pos1), removed_poses1)
		self.__string_list = list(filter(lambda s: len(s) > 0, removed_poses2))
		return self.__list2string( )
