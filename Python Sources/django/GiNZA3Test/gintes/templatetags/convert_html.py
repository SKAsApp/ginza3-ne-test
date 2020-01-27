from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from typing import List, Pattern
import re
import os
from logging import Logger, getLogger


register = template.Library( )
logger: Logger = getLogger("gintes")


@register.filter
@stringfilter
def break_line(value: str):
	return mark_safe(value.replace("\r\n", "<br />\r\n"))


@register.filter(needs_autoescape = False)
@stringfilter
def cabocha(value: str):
	values: List[str] = value.splitlines( )
	pattern_tag: Pattern = re.compile("([^_]*?)\t([^_]+?)-([^_]+?)-([^_]+?)\t([BI]-[A-Za-z]{1,}_{0,1}[A-Za-z]{0,})")
	pattern_crlf: Pattern = re.compile("^(EOS)")
	pattern_o: Pattern = re.compile("([^_]*?)\t[^_]+?-[^_]+?-[^_]+?\tO")
	# hoge，piyo，fugaとかいう良くわからない名前は使わないこと！
	hoge: List[str] = list(map(lambda val: pattern_tag.sub('<span style="background-color: #a0ffff; color: #000000; padding-top: 3pt; padding-bottom: 3pt; padding-left: 5pt; padding-right: 5pt; text-align: justify; text-justify: inter-word;">\\1 <span style="color: #ff0000; text-align: justify; text-justify: inter-word;">\\5</span><span style="font-size: x-small; color: #000000; text-align: justify; text-justify: inter-word;">（\\2-\\3-\\4）</span></span> ', val), values))
	piyo: List[str] = list(map(lambda tags: pattern_crlf.sub('\r\n', tags), hoge))
	fuga: List[str] = list(map(lambda br: pattern_o.sub('\\1 ', br), piyo))
	output: str = "".join(fuga)
	# macの場合↓のコメント解除で完了通知ができる。
	# os.system("osascript -e 'display notification \"ブラウザーをご確認ください。\" with title \"固有表現抽出できました\" sound name \"\"'")
	return mark_safe(output)
