# Apache License, Version 2.0の「mojimoji」（by Studio Ousia）を用いています。

from typing import Optional
from logging import Logger, getLogger
import mojimoji


class FileIO:
	def __init__(self, logger: Optional[Logger] = None):
		self.__logger: Logger = getLogger("gintes") if logger is None else logger
	
	def replace_carriage_return_line_feed_to_space(self, before_string: str) -> str:
		""" CRLF，LF，CRを空白文字に置き換える。そもそもCRって使うことあるのか？"""
		replaced_carriage_return_line_feed = before_string.replace("\r\n", "　")
		replaced_line_feed = replaced_carriage_return_line_feed.replace("\n", "　")
		return replaced_line_feed.replace("\r", "　")
	
	def replace_sign_to_full_width(self, before_string: str) -> str:
		"""ASCII半角記号は正規表現などいろいろと影響しそうなので全角記号に置き換える。"""
		# 半角→全角にする記号
		half: str = "\"#%&'()*+" + "<=>?@" + "[\]^`" + "{|}~" + "‐"
		full: str = "＂＃％＆＇（）＊＋" + "＜＝＞？＠" + "［＼］＾｀" + "｛｜｝〜" + "-"
		translate_table = str.maketrans(half, full)
		return before_string.translate(translate_table)
	
	def replace_half_to_full_width(self, before_string: str) -> str:
		"""英数字は半角に統一する。"""
		translate_table = self.__set_translate_table_latin( )
		translate_latin: str =  before_string.translate(translate_table)
		return mojimoji.han_to_zen(translate_latin, digit = False, ascii = False)
	
	def __set_translate_table_latin(self) -> dict:
		half_character = list( )
		full_character = list( )
		# 数字
		for i in range(10):
			half_character.append(chr(0x0030 + i))
			full_character.append(chr(0xff10 + i))
		# 英大文字
		for i in range(26):
			half_character.append(chr(0x0041 + i))
			full_character.append(chr(0xff21 + i))
		# 英小文字
		for i in range(26):
			half_character.append(chr(0x0061 + i))
			full_character.append(chr(0xff41 + i))
		half: str = "".join(half_character)
		full: str = "".join(full_character)
		return str.maketrans(full, half)
