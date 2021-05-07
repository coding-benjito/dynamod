# Generated from Dynamod.g4 by ANTLR 4.9.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


from antlr4.Token import CommonToken
import re
import importlib
# Allow languages to extend the lexer and parser, by loading the parser dynamically
module_path = __name__[:-5]
language_name = __name__.split('.')[-1]
language_name = language_name[:-5]  # Remove Lexer from name
LanguageParser = getattr(importlib.import_module('{}Parser'.format(module_path)), '{}Parser'.format(language_name))



def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\2\66")
        buf.write("\u01ca\b\1\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7")
        buf.write("\t\7\4\b\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r")
        buf.write("\4\16\t\16\4\17\t\17\4\20\t\20\4\21\t\21\4\22\t\22\4\23")
        buf.write("\t\23\4\24\t\24\4\25\t\25\4\26\t\26\4\27\t\27\4\30\t\30")
        buf.write("\4\31\t\31\4\32\t\32\4\33\t\33\4\34\t\34\4\35\t\35\4\36")
        buf.write("\t\36\4\37\t\37\4 \t \4!\t!\4\"\t\"\4#\t#\4$\t$\4%\t%")
        buf.write("\4&\t&\4\'\t\'\4(\t(\4)\t)\4*\t*\4+\t+\4,\t,\4-\t-\4.")
        buf.write("\t.\4/\t/\4\60\t\60\4\61\t\61\4\62\t\62\4\63\t\63\4\64")
        buf.write("\t\64\4\65\t\65\4\66\t\66\4\67\t\67\48\t8\49\t9\4:\t:")
        buf.write("\4;\t;\4<\t<\4=\t=\4>\t>\4?\t?\4@\t@\4A\tA\3\2\3\2\3\3")
        buf.write("\3\3\3\4\3\4\3\5\3\5\3\6\3\6\3\7\3\7\3\b\3\b\3\b\3\t\3")
        buf.write("\t\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\n\3\13\3\13\3\13\3\13")
        buf.write("\3\13\3\13\3\13\3\13\3\13\3\13\3\13\3\f\3\f\3\f\3\f\3")
        buf.write("\f\3\f\3\f\3\f\3\f\3\f\3\f\3\r\3\r\3\r\3\r\3\r\3\r\3\r")
        buf.write("\3\r\3\r\3\r\3\r\3\r\3\r\3\16\3\16\3\16\3\16\3\16\3\16")
        buf.write("\3\16\3\16\3\16\3\17\3\17\3\17\3\17\3\17\3\17\3\17\3\17")
        buf.write("\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\20\3\21\3\21\3\21")
        buf.write("\3\21\3\21\3\21\3\21\3\22\3\22\3\22\3\22\3\22\3\22\3\22")
        buf.write("\3\23\3\23\3\23\3\23\3\24\3\24\3\24\3\25\3\25\3\25\3\25")
        buf.write("\3\25\3\25\3\25\3\25\3\25\3\25\3\26\3\26\3\26\3\26\3\27")
        buf.write("\3\27\3\27\3\27\3\30\3\30\3\30\3\31\3\31\3\31\3\32\3\32")
        buf.write("\3\32\3\32\3\32\3\32\3\33\3\33\3\33\3\33\3\33\3\34\3\34")
        buf.write("\3\34\3\35\3\35\3\35\3\35\3\35\3\36\3\36\3\36\3\36\3\37")
        buf.write("\3\37\3\37\3 \3 \3 \3 \3!\3!\3\"\3\"\3\"\3#\3#\3$\3$\3")
        buf.write("$\3%\3%\3%\3&\3&\3&\3\'\3\'\3\'\3(\3(\3(\5(\u013a\n(\3")
        buf.write("(\3(\5(\u013e\n(\3(\5(\u0141\n(\5(\u0143\n(\3(\3(\3)\3")
        buf.write(")\7)\u0149\n)\f)\16)\u014c\13)\3*\3*\7*\u0150\n*\f*\16")
        buf.write("*\u0153\13*\3*\3*\3+\3+\5+\u0159\n+\3,\3,\7,\u015d\n,")
        buf.write("\f,\16,\u0160\13,\3,\6,\u0163\n,\r,\16,\u0164\5,\u0167")
        buf.write("\n,\3-\3-\5-\u016b\n-\3.\3.\3/\3/\3\60\3\60\3\61\3\61")
        buf.write("\3\61\3\62\3\62\3\62\3\63\3\63\3\63\3\64\3\64\3\64\3\65")
        buf.write("\3\65\3\65\5\65\u0182\n\65\3\65\3\65\3\66\3\66\3\67\3")
        buf.write("\67\38\58\u018b\n8\38\38\38\38\58\u0191\n8\39\39\59\u0195")
        buf.write("\n9\39\39\3:\6:\u019a\n:\r:\16:\u019b\3;\3;\6;\u01a0\n")
        buf.write(";\r;\16;\u01a1\3<\3<\5<\u01a6\n<\3<\6<\u01a9\n<\r<\16")
        buf.write("<\u01aa\3=\6=\u01ae\n=\r=\16=\u01af\3>\3>\7>\u01b4\n>")
        buf.write("\f>\16>\u01b7\13>\3?\3?\5?\u01bb\n?\3?\5?\u01be\n?\3?")
        buf.write("\3?\5?\u01c2\n?\3@\5@\u01c5\n@\3A\3A\5A\u01c9\nA\2\2B")
        buf.write("\3\3\5\4\7\5\t\6\13\7\r\b\17\t\21\n\23\13\25\f\27\r\31")
        buf.write("\16\33\17\35\20\37\21!\22#\23%\24\'\25)\26+\27-\30/\31")
        buf.write("\61\32\63\33\65\34\67\359\36;\37= ?!A\"C#E$G%I&K\'M(O")
        buf.write(")Q*S+U,W-Y.[/]\60_\61a\62c\63e\64g\65i\66k\2m\2o\2q\2")
        buf.write("s\2u\2w\2y\2{\2}\2\177\2\u0081\2\3\2\13\6\2\f\f\16\17")
        buf.write("))^^\3\2\63;\3\2\62;\4\2GGgg\4\2--//\4\2\13\13\"\"\4\2")
        buf.write("\f\f\16\17\u0129\2C\\aac|\u00ac\u00ac\u00b7\u00b7\u00bc")
        buf.write("\u00bc\u00c2\u00d8\u00da\u00f8\u00fa\u0243\u0252\u02c3")
        buf.write("\u02c8\u02d3\u02e2\u02e6\u02f0\u02f0\u037c\u037c\u0388")
        buf.write("\u0388\u038a\u038c\u038e\u038e\u0390\u03a3\u03a5\u03d0")
        buf.write("\u03d2\u03f7\u03f9\u0483\u048c\u04d0\u04d2\u04fb\u0502")
        buf.write("\u0511\u0533\u0558\u055b\u055b\u0563\u0589\u05d2\u05ec")
        buf.write("\u05f2\u05f4\u0623\u063c\u0642\u064c\u0670\u0671\u0673")
        buf.write("\u06d5\u06d7\u06d7\u06e7\u06e8\u06f0\u06f1\u06fc\u06fe")
        buf.write("\u0701\u0701\u0712\u0712\u0714\u0731\u074f\u076f\u0782")
        buf.write("\u07a7\u07b3\u07b3\u0906\u093b\u093f\u093f\u0952\u0952")
        buf.write("\u095a\u0963\u097f\u097f\u0987\u098e\u0991\u0992\u0995")
        buf.write("\u09aa\u09ac\u09b2\u09b4\u09b4\u09b8\u09bb\u09bf\u09bf")
        buf.write("\u09d0\u09d0\u09de\u09df\u09e1\u09e3\u09f2\u09f3\u0a07")
        buf.write("\u0a0c\u0a11\u0a12\u0a15\u0a2a\u0a2c\u0a32\u0a34\u0a35")
        buf.write("\u0a37\u0a38\u0a3a\u0a3b\u0a5b\u0a5e\u0a60\u0a60\u0a74")
        buf.write("\u0a76\u0a87\u0a8f\u0a91\u0a93\u0a95\u0aaa\u0aac\u0ab2")
        buf.write("\u0ab4\u0ab5\u0ab7\u0abb\u0abf\u0abf\u0ad2\u0ad2\u0ae2")
        buf.write("\u0ae3\u0b07\u0b0e\u0b11\u0b12\u0b15\u0b2a\u0b2c\u0b32")
        buf.write("\u0b34\u0b35\u0b37\u0b3b\u0b3f\u0b3f\u0b5e\u0b5f\u0b61")
        buf.write("\u0b63\u0b73\u0b73\u0b85\u0b85\u0b87\u0b8c\u0b90\u0b92")
        buf.write("\u0b94\u0b97\u0b9b\u0b9c\u0b9e\u0b9e\u0ba0\u0ba1\u0ba5")
        buf.write("\u0ba6\u0baa\u0bac\u0bb0\u0bbb\u0c07\u0c0e\u0c10\u0c12")
        buf.write("\u0c14\u0c2a\u0c2c\u0c35\u0c37\u0c3b\u0c62\u0c63\u0c87")
        buf.write("\u0c8e\u0c90\u0c92\u0c94\u0caa\u0cac\u0cb5\u0cb7\u0cbb")
        buf.write("\u0cbf\u0cbf\u0ce0\u0ce0\u0ce2\u0ce3\u0d07\u0d0e\u0d10")
        buf.write("\u0d12\u0d14\u0d2a\u0d2c\u0d3b\u0d62\u0d63\u0d87\u0d98")
        buf.write("\u0d9c\u0db3\u0db5\u0dbd\u0dbf\u0dbf\u0dc2\u0dc8\u0e03")
        buf.write("\u0e32\u0e34\u0e35\u0e42\u0e48\u0e83\u0e84\u0e86\u0e86")
        buf.write("\u0e89\u0e8a\u0e8c\u0e8c\u0e8f\u0e8f\u0e96\u0e99\u0e9b")
        buf.write("\u0ea1\u0ea3\u0ea5\u0ea7\u0ea7\u0ea9\u0ea9\u0eac\u0ead")
        buf.write("\u0eaf\u0eb2\u0eb4\u0eb5\u0ebf\u0ebf\u0ec2\u0ec6\u0ec8")
        buf.write("\u0ec8\u0ede\u0edf\u0f02\u0f02\u0f42\u0f49\u0f4b\u0f6c")
        buf.write("\u0f8a\u0f8d\u1002\u1023\u1025\u1029\u102b\u102c\u1052")
        buf.write("\u1057\u10a2\u10c7\u10d2\u10fc\u10fe\u10fe\u1102\u115b")
        buf.write("\u1161\u11a4\u11aa\u11fb\u1202\u124a\u124c\u124f\u1252")
        buf.write("\u1258\u125a\u125a\u125c\u125f\u1262\u128a\u128c\u128f")
        buf.write("\u1292\u12b2\u12b4\u12b7\u12ba\u12c0\u12c2\u12c2\u12c4")
        buf.write("\u12c7\u12ca\u12d8\u12da\u1312\u1314\u1317\u131a\u135c")
        buf.write("\u1382\u1391\u13a2\u13f6\u1403\u166e\u1671\u1678\u1683")
        buf.write("\u169c\u16a2\u16ec\u16f0\u16f2\u1702\u170e\u1710\u1713")
        buf.write("\u1722\u1733\u1742\u1753\u1762\u176e\u1770\u1772\u1782")
        buf.write("\u17b5\u17d9\u17d9\u17de\u17de\u1822\u1879\u1882\u18aa")
        buf.write("\u1902\u191e\u1952\u196f\u1972\u1976\u1982\u19ab\u19c3")
        buf.write("\u19c9\u1a02\u1a18\u1d02\u1dc1\u1e02\u1e9d\u1ea2\u1efb")
        buf.write("\u1f02\u1f17\u1f1a\u1f1f\u1f22\u1f47\u1f4a\u1f4f\u1f52")
        buf.write("\u1f59\u1f5b\u1f5b\u1f5d\u1f5d\u1f5f\u1f5f\u1f61\u1f7f")
        buf.write("\u1f82\u1fb6\u1fb8\u1fbe\u1fc0\u1fc0\u1fc4\u1fc6\u1fc8")
        buf.write("\u1fce\u1fd2\u1fd5\u1fd8\u1fdd\u1fe2\u1fee\u1ff4\u1ff6")
        buf.write("\u1ff8\u1ffe\u2073\u2073\u2081\u2081\u2092\u2096\u2104")
        buf.write("\u2104\u2109\u2109\u210c\u2115\u2117\u2117\u211a\u211f")
        buf.write("\u2126\u2126\u2128\u2128\u212a\u212a\u212c\u2133\u2135")
        buf.write("\u213b\u213e\u2141\u2147\u214b\u2162\u2185\u2c02\u2c30")
        buf.write("\u2c32\u2c60\u2c82\u2ce6\u2d02\u2d27\u2d32\u2d67\u2d71")
        buf.write("\u2d71\u2d82\u2d98\u2da2\u2da8\u2daa\u2db0\u2db2\u2db8")
        buf.write("\u2dba\u2dc0\u2dc2\u2dc8\u2dca\u2dd0\u2dd2\u2dd8\u2dda")
        buf.write("\u2de0\u3007\u3009\u3023\u302b\u3033\u3037\u303a\u303e")
        buf.write("\u3043\u3098\u309d\u30a1\u30a3\u30fc\u30fe\u3101\u3107")
        buf.write("\u312e\u3133\u3190\u31a2\u31b9\u31f2\u3201\u3402\u4db7")
        buf.write("\u4e02\u9fbd\ua002\ua48e\ua802\ua803\ua805\ua807\ua809")
        buf.write("\ua80c\ua80e\ua824\uac02\ud7a5\uf902\ufa2f\ufa32\ufa6c")
        buf.write("\ufa72\ufadb\ufb02\ufb08\ufb15\ufb19\ufb1f\ufb1f\ufb21")
        buf.write("\ufb2a\ufb2c\ufb38\ufb3a\ufb3e\ufb40\ufb40\ufb42\ufb43")
        buf.write("\ufb45\ufb46\ufb48\ufbb3\ufbd5\ufd3f\ufd52\ufd91\ufd94")
        buf.write("\ufdc9\ufdf2\ufdfd\ufe72\ufe76\ufe78\ufefe\uff23\uff3c")
        buf.write("\uff43\uff5c\uff68\uffc0\uffc4\uffc9\uffcc\uffd1\uffd4")
        buf.write("\uffd9\uffdc\uffde\u0096\2\62;\u0302\u0371\u0485\u0488")
        buf.write("\u0593\u05bb\u05bd\u05bf\u05c1\u05c1\u05c3\u05c4\u05c6")
        buf.write("\u05c7\u05c9\u05c9\u0612\u0617\u064d\u0660\u0662\u066b")
        buf.write("\u0672\u0672\u06d8\u06de\u06e1\u06e6\u06e9\u06ea\u06ec")
        buf.write("\u06ef\u06f2\u06fb\u0713\u0713\u0732\u074c\u07a8\u07b2")
        buf.write("\u0903\u0905\u093e\u093e\u0940\u094f\u0953\u0956\u0964")
        buf.write("\u0965\u0968\u0971\u0983\u0985\u09be\u09be\u09c0\u09c6")
        buf.write("\u09c9\u09ca\u09cd\u09cf\u09d9\u09d9\u09e4\u09e5\u09e8")
        buf.write("\u09f1\u0a03\u0a05\u0a3e\u0a3e\u0a40\u0a44\u0a49\u0a4a")
        buf.write("\u0a4d\u0a4f\u0a68\u0a73\u0a83\u0a85\u0abe\u0abe\u0ac0")
        buf.write("\u0ac7\u0ac9\u0acb\u0acd\u0acf\u0ae4\u0ae5\u0ae8\u0af1")
        buf.write("\u0b03\u0b05\u0b3e\u0b3e\u0b40\u0b45\u0b49\u0b4a\u0b4d")
        buf.write("\u0b4f\u0b58\u0b59\u0b68\u0b71\u0b84\u0b84\u0bc0\u0bc4")
        buf.write("\u0bc8\u0bca\u0bcc\u0bcf\u0bd9\u0bd9\u0be8\u0bf1\u0c03")
        buf.write("\u0c05\u0c40\u0c46\u0c48\u0c4a\u0c4c\u0c4f\u0c57\u0c58")
        buf.write("\u0c68\u0c71\u0c84\u0c85\u0cbe\u0cbe\u0cc0\u0cc6\u0cc8")
        buf.write("\u0cca\u0ccc\u0ccf\u0cd7\u0cd8\u0ce8\u0cf1\u0d04\u0d05")
        buf.write("\u0d40\u0d45\u0d48\u0d4a\u0d4c\u0d4f\u0d59\u0d59\u0d68")
        buf.write("\u0d71\u0d84\u0d85\u0dcc\u0dcc\u0dd1\u0dd6\u0dd8\u0dd8")
        buf.write("\u0dda\u0de1\u0df4\u0df5\u0e33\u0e33\u0e36\u0e3c\u0e49")
        buf.write("\u0e50\u0e52\u0e5b\u0eb3\u0eb3\u0eb6\u0ebb\u0ebd\u0ebe")
        buf.write("\u0eca\u0ecf\u0ed2\u0edb\u0f1a\u0f1b\u0f22\u0f2b\u0f37")
        buf.write("\u0f37\u0f39\u0f39\u0f3b\u0f3b\u0f40\u0f41\u0f73\u0f86")
        buf.write("\u0f88\u0f89\u0f92\u0f99\u0f9b\u0fbe\u0fc8\u0fc8\u102e")
        buf.write("\u1034\u1038\u103b\u1042\u104b\u1058\u105b\u1361\u1361")
        buf.write("\u136b\u1373\u1714\u1716\u1734\u1736\u1754\u1755\u1774")
        buf.write("\u1775\u17b8\u17d5\u17df\u17df\u17e2\u17eb\u180d\u180f")
        buf.write("\u1812\u181b\u18ab\u18ab\u1922\u192d\u1932\u193d\u1948")
        buf.write("\u1951\u19b2\u19c2\u19ca\u19cb\u19d2\u19db\u1a19\u1a1d")
        buf.write("\u1dc2\u1dc5\u2041\u2042\u2056\u2056\u20d2\u20de\u20e3")
        buf.write("\u20e3\u20e7\u20ed\u302c\u3031\u309b\u309c\ua804\ua804")
        buf.write("\ua808\ua808\ua80d\ua80d\ua825\ua829\ufb20\ufb20\ufe02")
        buf.write("\ufe11\ufe22\ufe25\ufe35\ufe36\ufe4f\ufe51\uff12\uff1b")
        buf.write("\uff41\uff41\2\u01d7\2\3\3\2\2\2\2\5\3\2\2\2\2\7\3\2\2")
        buf.write("\2\2\t\3\2\2\2\2\13\3\2\2\2\2\r\3\2\2\2\2\17\3\2\2\2\2")
        buf.write("\21\3\2\2\2\2\23\3\2\2\2\2\25\3\2\2\2\2\27\3\2\2\2\2\31")
        buf.write("\3\2\2\2\2\33\3\2\2\2\2\35\3\2\2\2\2\37\3\2\2\2\2!\3\2")
        buf.write("\2\2\2#\3\2\2\2\2%\3\2\2\2\2\'\3\2\2\2\2)\3\2\2\2\2+\3")
        buf.write("\2\2\2\2-\3\2\2\2\2/\3\2\2\2\2\61\3\2\2\2\2\63\3\2\2\2")
        buf.write("\2\65\3\2\2\2\2\67\3\2\2\2\29\3\2\2\2\2;\3\2\2\2\2=\3")
        buf.write("\2\2\2\2?\3\2\2\2\2A\3\2\2\2\2C\3\2\2\2\2E\3\2\2\2\2G")
        buf.write("\3\2\2\2\2I\3\2\2\2\2K\3\2\2\2\2M\3\2\2\2\2O\3\2\2\2\2")
        buf.write("Q\3\2\2\2\2S\3\2\2\2\2U\3\2\2\2\2W\3\2\2\2\2Y\3\2\2\2")
        buf.write("\2[\3\2\2\2\2]\3\2\2\2\2_\3\2\2\2\2a\3\2\2\2\2c\3\2\2")
        buf.write("\2\2e\3\2\2\2\2g\3\2\2\2\2i\3\2\2\2\3\u0083\3\2\2\2\5")
        buf.write("\u0085\3\2\2\2\7\u0087\3\2\2\2\t\u0089\3\2\2\2\13\u008b")
        buf.write("\3\2\2\2\r\u008d\3\2\2\2\17\u008f\3\2\2\2\21\u0092\3\2")
        buf.write("\2\2\23\u0094\3\2\2\2\25\u009c\3\2\2\2\27\u00a7\3\2\2")
        buf.write("\2\31\u00b2\3\2\2\2\33\u00bf\3\2\2\2\35\u00c8\3\2\2\2")
        buf.write("\37\u00d0\3\2\2\2!\u00d8\3\2\2\2#\u00df\3\2\2\2%\u00e6")
        buf.write("\3\2\2\2\'\u00ea\3\2\2\2)\u00ed\3\2\2\2+\u00f7\3\2\2\2")
        buf.write("-\u00fb\3\2\2\2/\u00ff\3\2\2\2\61\u0102\3\2\2\2\63\u0105")
        buf.write("\3\2\2\2\65\u010b\3\2\2\2\67\u0110\3\2\2\29\u0113\3\2")
        buf.write("\2\2;\u0118\3\2\2\2=\u011c\3\2\2\2?\u011f\3\2\2\2A\u0123")
        buf.write("\3\2\2\2C\u0125\3\2\2\2E\u0128\3\2\2\2G\u012a\3\2\2\2")
        buf.write("I\u012d\3\2\2\2K\u0130\3\2\2\2M\u0133\3\2\2\2O\u0142\3")
        buf.write("\2\2\2Q\u0146\3\2\2\2S\u014d\3\2\2\2U\u0158\3\2\2\2W\u0166")
        buf.write("\3\2\2\2Y\u016a\3\2\2\2[\u016c\3\2\2\2]\u016e\3\2\2\2")
        buf.write("_\u0170\3\2\2\2a\u0172\3\2\2\2c\u0175\3\2\2\2e\u0178\3")
        buf.write("\2\2\2g\u017b\3\2\2\2i\u0181\3\2\2\2k\u0185\3\2\2\2m\u0187")
        buf.write("\3\2\2\2o\u0190\3\2\2\2q\u0194\3\2\2\2s\u0199\3\2\2\2")
        buf.write("u\u019d\3\2\2\2w\u01a3\3\2\2\2y\u01ad\3\2\2\2{\u01b1\3")
        buf.write("\2\2\2}\u01b8\3\2\2\2\177\u01c4\3\2\2\2\u0081\u01c8\3")
        buf.write("\2\2\2\u0083\u0084\7?\2\2\u0084\4\3\2\2\2\u0085\u0086")
        buf.write("\7.\2\2\u0086\6\3\2\2\2\u0087\u0088\7-\2\2\u0088\b\3\2")
        buf.write("\2\2\u0089\u008a\7/\2\2\u008a\n\3\2\2\2\u008b\u008c\7")
        buf.write("\61\2\2\u008c\f\3\2\2\2\u008d\u008e\7\'\2\2\u008e\16\3")
        buf.write("\2\2\2\u008f\u0090\7\'\2\2\u0090\u0091\7\'\2\2\u0091\20")
        buf.write("\3\2\2\2\u0092\u0093\7~\2\2\u0093\22\3\2\2\2\u0094\u0095")
        buf.write("\7k\2\2\u0095\u0096\7p\2\2\u0096\u0097\7e\2\2\u0097\u0098")
        buf.write("\7n\2\2\u0098\u0099\7w\2\2\u0099\u009a\7f\2\2\u009a\u009b")
        buf.write("\7g\2\2\u009b\24\3\2\2\2\u009c\u009d\7r\2\2\u009d\u009e")
        buf.write("\7c\2\2\u009e\u009f\7t\2\2\u009f\u00a0\7c\2\2\u00a0\u00a1")
        buf.write("\7o\2\2\u00a1\u00a2\7g\2\2\u00a2\u00a3\7v\2\2\u00a3\u00a4")
        buf.write("\7g\2\2\u00a4\u00a5\7t\2\2\u00a5\u00a6\7u\2\2\u00a6\26")
        buf.write("\3\2\2\2\u00a7\u00a8\7c\2\2\u00a8\u00a9\7v\2\2\u00a9\u00aa")
        buf.write("\7v\2\2\u00aa\u00ab\7t\2\2\u00ab\u00ac\7k\2\2\u00ac\u00ad")
        buf.write("\7d\2\2\u00ad\u00ae\7w\2\2\u00ae\u00af\7v\2\2\u00af\u00b0")
        buf.write("\7g\2\2\u00b0\u00b1\7u\2\2\u00b1\30\3\2\2\2\u00b2\u00b3")
        buf.write("\7r\2\2\u00b3\u00b4\7t\2\2\u00b4\u00b5\7q\2\2\u00b5\u00b6")
        buf.write("\7i\2\2\u00b6\u00b7\7t\2\2\u00b7\u00b8\7g\2\2\u00b8\u00b9")
        buf.write("\7u\2\2\u00b9\u00ba\7u\2\2\u00ba\u00bb\7k\2\2\u00bb\u00bc")
        buf.write("\7q\2\2\u00bc\u00bd\7p\2\2\u00bd\u00be\7u\2\2\u00be\32")
        buf.write("\3\2\2\2\u00bf\u00c0\7h\2\2\u00c0\u00c1\7q\2\2\u00c1\u00c2")
        buf.write("\7t\2\2\u00c2\u00c3\7o\2\2\u00c3\u00c4\7w\2\2\u00c4\u00c5")
        buf.write("\7n\2\2\u00c5\u00c6\7c\2\2\u00c6\u00c7\7u\2\2\u00c7\34")
        buf.write("\3\2\2\2\u00c8\u00c9\7t\2\2\u00c9\u00ca\7g\2\2\u00ca\u00cb")
        buf.write("\7u\2\2\u00cb\u00cc\7w\2\2\u00cc\u00cd\7n\2\2\u00cd\u00ce")
        buf.write("\7v\2\2\u00ce\u00cf\7u\2\2\u00cf\36\3\2\2\2\u00d0\u00d1")
        buf.write("\7e\2\2\u00d1\u00d2\7j\2\2\u00d2\u00d3\7c\2\2\u00d3\u00d4")
        buf.write("\7p\2\2\u00d4\u00d5\7i\2\2\u00d5\u00d6\7g\2\2\u00d6\u00d7")
        buf.write("\7u\2\2\u00d7 \3\2\2\2\u00d8\u00d9\7x\2\2\u00d9\u00da")
        buf.write("\7c\2\2\u00da\u00db\7n\2\2\u00db\u00dc\7w\2\2\u00dc\u00dd")
        buf.write("\7g\2\2\u00dd\u00de\7u\2\2\u00de\"\3\2\2\2\u00df\u00e0")
        buf.write("\7u\2\2\u00e0\u00e1\7j\2\2\u00e1\u00e2\7c\2\2\u00e2\u00e3")
        buf.write("\7t\2\2\u00e3\u00e4\7g\2\2\u00e4\u00e5\7u\2\2\u00e5$\3")
        buf.write("\2\2\2\u00e6\u00e7\7h\2\2\u00e7\u00e8\7q\2\2\u00e8\u00e9")
        buf.write("\7t\2\2\u00e9&\3\2\2\2\u00ea\u00eb\7k\2\2\u00eb\u00ec")
        buf.write("\7p\2\2\u00ec(\3\2\2\2\u00ed\u00ee\7q\2\2\u00ee\u00ef")
        buf.write("\7v\2\2\u00ef\u00f0\7j\2\2\u00f0\u00f1\7g\2\2\u00f1\u00f2")
        buf.write("\7t\2\2\u00f2\u00f3\7y\2\2\u00f3\u00f4\7k\2\2\u00f4\u00f5")
        buf.write("\7u\2\2\u00f5\u00f6\7g\2\2\u00f6*\3\2\2\2\u00f7\u00f8")
        buf.write("\7x\2\2\u00f8\u00f9\7c\2\2\u00f9\u00fa\7t\2\2\u00fa,\3")
        buf.write("\2\2\2\u00fb\u00fc\7u\2\2\u00fc\u00fd\7g\2\2\u00fd\u00fe")
        buf.write("\7v\2\2\u00fe.\3\2\2\2\u00ff\u0100\7c\2\2\u0100\u0101")
        buf.write("\7u\2\2\u0101\60\3\2\2\2\u0102\u0103\7d\2\2\u0103\u0104")
        buf.write("\7{\2\2\u0104\62\3\2\2\2\u0105\u0106\7c\2\2\u0106\u0107")
        buf.write("\7h\2\2\u0107\u0108\7v\2\2\u0108\u0109\7g\2\2\u0109\u010a")
        buf.write("\7t\2\2\u010a\64\3\2\2\2\u010b\u010c\7y\2\2\u010c\u010d")
        buf.write("\7k\2\2\u010d\u010e\7v\2\2\u010e\u010f\7j\2\2\u010f\66")
        buf.write("\3\2\2\2\u0110\u0111\7k\2\2\u0111\u0112\7h\2\2\u01128")
        buf.write("\3\2\2\2\u0113\u0114\7g\2\2\u0114\u0115\7n\2\2\u0115\u0116")
        buf.write("\7u\2\2\u0116\u0117\7g\2\2\u0117:\3\2\2\2\u0118\u0119")
        buf.write("\7c\2\2\u0119\u011a\7p\2\2\u011a\u011b\7f\2\2\u011b<\3")
        buf.write("\2\2\2\u011c\u011d\7q\2\2\u011d\u011e\7t\2\2\u011e>\3")
        buf.write("\2\2\2\u011f\u0120\7p\2\2\u0120\u0121\7q\2\2\u0121\u0122")
        buf.write("\7v\2\2\u0122@\3\2\2\2\u0123\u0124\7>\2\2\u0124B\3\2\2")
        buf.write("\2\u0125\u0126\7>\2\2\u0126\u0127\7?\2\2\u0127D\3\2\2")
        buf.write("\2\u0128\u0129\7@\2\2\u0129F\3\2\2\2\u012a\u012b\7@\2")
        buf.write("\2\u012b\u012c\7?\2\2\u012cH\3\2\2\2\u012d\u012e\7#\2")
        buf.write("\2\u012e\u012f\7?\2\2\u012fJ\3\2\2\2\u0130\u0131\7G\2")
        buf.write("\2\u0131\u0132\7S\2\2\u0132L\3\2\2\2\u0133\u0134\7\60")
        buf.write("\2\2\u0134\u0135\7\60\2\2\u0135N\3\2\2\2\u0136\u0137\6")
        buf.write("(\2\2\u0137\u0143\5y=\2\u0138\u013a\7\17\2\2\u0139\u0138")
        buf.write("\3\2\2\2\u0139\u013a\3\2\2\2\u013a\u013b\3\2\2\2\u013b")
        buf.write("\u013e\7\f\2\2\u013c\u013e\4\16\17\2\u013d\u0139\3\2\2")
        buf.write("\2\u013d\u013c\3\2\2\2\u013e\u0140\3\2\2\2\u013f\u0141")
        buf.write("\5y=\2\u0140\u013f\3\2\2\2\u0140\u0141\3\2\2\2\u0141\u0143")
        buf.write("\3\2\2\2\u0142\u0136\3\2\2\2\u0142\u013d\3\2\2\2\u0143")
        buf.write("\u0144\3\2\2\2\u0144\u0145\b(\2\2\u0145P\3\2\2\2\u0146")
        buf.write("\u014a\5\177@\2\u0147\u0149\5\u0081A\2\u0148\u0147\3\2")
        buf.write("\2\2\u0149\u014c\3\2\2\2\u014a\u0148\3\2\2\2\u014a\u014b")
        buf.write("\3\2\2\2\u014bR\3\2\2\2\u014c\u014a\3\2\2\2\u014d\u0151")
        buf.write("\7)\2\2\u014e\u0150\n\2\2\2\u014f\u014e\3\2\2\2\u0150")
        buf.write("\u0153\3\2\2\2\u0151\u014f\3\2\2\2\u0151\u0152\3\2\2\2")
        buf.write("\u0152\u0154\3\2\2\2\u0153\u0151\3\2\2\2\u0154\u0155\7")
        buf.write(")\2\2\u0155T\3\2\2\2\u0156\u0159\5W,\2\u0157\u0159\5Y")
        buf.write("-\2\u0158\u0156\3\2\2\2\u0158\u0157\3\2\2\2\u0159V\3\2")
        buf.write("\2\2\u015a\u015e\5k\66\2\u015b\u015d\5m\67\2\u015c\u015b")
        buf.write("\3\2\2\2\u015d\u0160\3\2\2\2\u015e\u015c\3\2\2\2\u015e")
        buf.write("\u015f\3\2\2\2\u015f\u0167\3\2\2\2\u0160\u015e\3\2\2\2")
        buf.write("\u0161\u0163\7\62\2\2\u0162\u0161\3\2\2\2\u0163\u0164")
        buf.write("\3\2\2\2\u0164\u0162\3\2\2\2\u0164\u0165\3\2\2\2\u0165")
        buf.write("\u0167\3\2\2\2\u0166\u015a\3\2\2\2\u0166\u0162\3\2\2\2")
        buf.write("\u0167X\3\2\2\2\u0168\u016b\5o8\2\u0169\u016b\5q9\2\u016a")
        buf.write("\u0168\3\2\2\2\u016a\u0169\3\2\2\2\u016bZ\3\2\2\2\u016c")
        buf.write("\u016d\7\60\2\2\u016d\\\3\2\2\2\u016e\u016f\7,\2\2\u016f")
        buf.write("^\3\2\2\2\u0170\u0171\7<\2\2\u0171`\3\2\2\2\u0172\u0173")
        buf.write("\7*\2\2\u0173\u0174\b\61\3\2\u0174b\3\2\2\2\u0175\u0176")
        buf.write("\7+\2\2\u0176\u0177\b\62\4\2\u0177d\3\2\2\2\u0178\u0179")
        buf.write("\7]\2\2\u0179\u017a\b\63\5\2\u017af\3\2\2\2\u017b\u017c")
        buf.write("\7_\2\2\u017c\u017d\b\64\6\2\u017dh\3\2\2\2\u017e\u0182")
        buf.write("\5y=\2\u017f\u0182\5{>\2\u0180\u0182\5}?\2\u0181\u017e")
        buf.write("\3\2\2\2\u0181\u017f\3\2\2\2\u0181\u0180\3\2\2\2\u0182")
        buf.write("\u0183\3\2\2\2\u0183\u0184\b\65\7\2\u0184j\3\2\2\2\u0185")
        buf.write("\u0186\t\3\2\2\u0186l\3\2\2\2\u0187\u0188\t\4\2\2\u0188")
        buf.write("n\3\2\2\2\u0189\u018b\5s:\2\u018a\u0189\3\2\2\2\u018a")
        buf.write("\u018b\3\2\2\2\u018b\u018c\3\2\2\2\u018c\u0191\5u;\2\u018d")
        buf.write("\u018e\5s:\2\u018e\u018f\7\60\2\2\u018f\u0191\3\2\2\2")
        buf.write("\u0190\u018a\3\2\2\2\u0190\u018d\3\2\2\2\u0191p\3\2\2")
        buf.write("\2\u0192\u0195\5s:\2\u0193\u0195\5o8\2\u0194\u0192\3\2")
        buf.write("\2\2\u0194\u0193\3\2\2\2\u0195\u0196\3\2\2\2\u0196\u0197")
        buf.write("\5w<\2\u0197r\3\2\2\2\u0198\u019a\5m\67\2\u0199\u0198")
        buf.write("\3\2\2\2\u019a\u019b\3\2\2\2\u019b\u0199\3\2\2\2\u019b")
        buf.write("\u019c\3\2\2\2\u019ct\3\2\2\2\u019d\u019f\7\60\2\2\u019e")
        buf.write("\u01a0\5m\67\2\u019f\u019e\3\2\2\2\u01a0\u01a1\3\2\2\2")
        buf.write("\u01a1\u019f\3\2\2\2\u01a1\u01a2\3\2\2\2\u01a2v\3\2\2")
        buf.write("\2\u01a3\u01a5\t\5\2\2\u01a4\u01a6\t\6\2\2\u01a5\u01a4")
        buf.write("\3\2\2\2\u01a5\u01a6\3\2\2\2\u01a6\u01a8\3\2\2\2\u01a7")
        buf.write("\u01a9\5m\67\2\u01a8\u01a7\3\2\2\2\u01a9\u01aa\3\2\2\2")
        buf.write("\u01aa\u01a8\3\2\2\2\u01aa\u01ab\3\2\2\2\u01abx\3\2\2")
        buf.write("\2\u01ac\u01ae\t\7\2\2\u01ad\u01ac\3\2\2\2\u01ae\u01af")
        buf.write("\3\2\2\2\u01af\u01ad\3\2\2\2\u01af\u01b0\3\2\2\2\u01b0")
        buf.write("z\3\2\2\2\u01b1\u01b5\7%\2\2\u01b2\u01b4\n\b\2\2\u01b3")
        buf.write("\u01b2\3\2\2\2\u01b4\u01b7\3\2\2\2\u01b5\u01b3\3\2\2\2")
        buf.write("\u01b5\u01b6\3\2\2\2\u01b6|\3\2\2\2\u01b7\u01b5\3\2\2")
        buf.write("\2\u01b8\u01ba\7^\2\2\u01b9\u01bb\5y=\2\u01ba\u01b9\3")
        buf.write("\2\2\2\u01ba\u01bb\3\2\2\2\u01bb\u01c1\3\2\2\2\u01bc\u01be")
        buf.write("\7\17\2\2\u01bd\u01bc\3\2\2\2\u01bd\u01be\3\2\2\2\u01be")
        buf.write("\u01bf\3\2\2\2\u01bf\u01c2\7\f\2\2\u01c0\u01c2\4\16\17")
        buf.write("\2\u01c1\u01bd\3\2\2\2\u01c1\u01c0\3\2\2\2\u01c2~\3\2")
        buf.write("\2\2\u01c3\u01c5\t\t\2\2\u01c4\u01c3\3\2\2\2\u01c5\u0080")
        buf.write("\3\2\2\2\u01c6\u01c9\5\177@\2\u01c7\u01c9\t\n\2\2\u01c8")
        buf.write("\u01c6\3\2\2\2\u01c8\u01c7\3\2\2\2\u01c9\u0082\3\2\2\2")
        buf.write("\35\2\u0139\u013d\u0140\u0142\u014a\u0151\u0158\u015e")
        buf.write("\u0164\u0166\u016a\u0181\u018a\u0190\u0194\u019b\u01a1")
        buf.write("\u01a5\u01aa\u01af\u01b5\u01ba\u01bd\u01c1\u01c4\u01c8")
        buf.write("\b\3(\2\3\61\3\3\62\4\3\63\5\3\64\6\b\2\2")
        return buf.getvalue()


class DynamodLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    INCLUDE = 9
    PARAMETERS = 10
    ATTRIBUTES = 11
    PROGRESSION = 12
    FORMULAS = 13
    RESULTS = 14
    CHANGES = 15
    VALUES = 16
    SHARES = 17
    FOR = 18
    IN = 19
    OTHERWISE = 20
    VAR = 21
    SET = 22
    AS = 23
    BY = 24
    AFTER = 25
    WITH = 26
    IF = 27
    ELSE = 28
    AND = 29
    OR = 30
    NOT = 31
    LT = 32
    LE = 33
    GT = 34
    GE = 35
    NE = 36
    EQ = 37
    DOTDOT = 38
    NEWLINE = 39
    NAME = 40
    PATH = 41
    NUMBER = 42
    INTEGER = 43
    FLOAT_NUMBER = 44
    DOT = 45
    STAR = 46
    COLON = 47
    OPEN_PAREN = 48
    CLOSE_PAREN = 49
    OPEN_BRACK = 50
    CLOSE_BRACK = 51
    SKIP_ = 52

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'='", "','", "'+'", "'-'", "'/'", "'%'", "'%%'", "'|'", "'include'", 
            "'parameters'", "'attributes'", "'progressions'", "'formulas'", 
            "'results'", "'changes'", "'values'", "'shares'", "'for'", "'in'", 
            "'otherwise'", "'var'", "'set'", "'as'", "'by'", "'after'", 
            "'with'", "'if'", "'else'", "'and'", "'or'", "'not'", "'<'", 
            "'<='", "'>'", "'>='", "'!='", "'EQ'", "'..'", "'.'", "'*'", 
            "':'", "'('", "')'", "'['", "']'" ]

    symbolicNames = [ "<INVALID>",
            "INCLUDE", "PARAMETERS", "ATTRIBUTES", "PROGRESSION", "FORMULAS", 
            "RESULTS", "CHANGES", "VALUES", "SHARES", "FOR", "IN", "OTHERWISE", 
            "VAR", "SET", "AS", "BY", "AFTER", "WITH", "IF", "ELSE", "AND", 
            "OR", "NOT", "LT", "LE", "GT", "GE", "NE", "EQ", "DOTDOT", "NEWLINE", 
            "NAME", "PATH", "NUMBER", "INTEGER", "FLOAT_NUMBER", "DOT", 
            "STAR", "COLON", "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACK", 
            "CLOSE_BRACK", "SKIP_" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "INCLUDE", "PARAMETERS", "ATTRIBUTES", "PROGRESSION", 
                  "FORMULAS", "RESULTS", "CHANGES", "VALUES", "SHARES", 
                  "FOR", "IN", "OTHERWISE", "VAR", "SET", "AS", "BY", "AFTER", 
                  "WITH", "IF", "ELSE", "AND", "OR", "NOT", "LT", "LE", 
                  "GT", "GE", "NE", "EQ", "DOTDOT", "NEWLINE", "NAME", "PATH", 
                  "NUMBER", "INTEGER", "FLOAT_NUMBER", "DOT", "STAR", "COLON", 
                  "OPEN_PAREN", "CLOSE_PAREN", "OPEN_BRACK", "CLOSE_BRACK", 
                  "SKIP_", "NON_ZERO_DIGIT", "DIGIT", "POINT_FLOAT", "EXPONENT_FLOAT", 
                  "INT_PART", "FRACTION", "EXPONENT", "SPACES", "COMMENT", 
                  "LINE_JOINING", "ID_START", "ID_CONTINUE" ]

    grammarFileName = "Dynamod.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


    @property
    def tokens(self):
        try:
            return self._tokens
        except AttributeError:
            self._tokens = []
            return self._tokens
    @property
    def indents(self):
        try:
            return self._indents
        except AttributeError:
            self._indents = []
            return self._indents
    @property
    def opened(self):
        try:
            return self._opened
        except AttributeError:
            self._opened = 0
            return self._opened
    @opened.setter
    def opened(self, value):
        self._opened = value
    @property
    def lastToken(self):
        try:
            return self._lastToken
        except AttributeError:
            self._lastToken = None
            return self._lastToken
    @lastToken.setter
    def lastToken(self, value):
        self._lastToken = value
    def reset(self):
        super().reset()
        self.tokens = []
        self.indents = []
        self.opened = 0
        self.lastToken = None
    def emitToken(self, t):
        super().emitToken(t)
        self.tokens.append(t)
    def nextToken(self):
        if self._input.LA(1) == Token.EOF and self.indents:
            for i in range(len(self.tokens)-1,-1,-1):
                if self.tokens[i].type == Token.EOF:
                    self.tokens.pop(i)
            self.emitToken(self.commonToken(LanguageParser.NEWLINE, '\n'))
            while self.indents:
                self.emitToken(self.createDedent())
                self.indents.pop()
            self.emitToken(self.commonToken(LanguageParser.EOF, "<EOF>"))
        next = super().nextToken()
        if next.channel == Token.DEFAULT_CHANNEL:
            self.lastToken = next
        return next if not self.tokens else self.tokens.pop(0)
    def createDedent(self):
        dedent = self.commonToken(LanguageParser.DEDENT, "")
        dedent.line = self.lastToken.line
        return dedent
    def commonToken(self, type, text, indent=0):
        stop = self.getCharIndex()-1-indent
        start = (stop - len(text) + 1) if text else stop
        return CommonToken(self._tokenFactorySourcePair, type, super().DEFAULT_TOKEN_CHANNEL, start, stop)
    @staticmethod
    def getIndentationCount(spaces):
        count = 0
        for ch in spaces:
            if ch == '\t':
                count += 8 - (count % 8)
            else:
                count += 1
        return count
    def atStartOfInput(self):
        return Lexer.column.fget(self) == 0 and Lexer.line.fget(self) == 1


    def action(self, localctx:RuleContext, ruleIndex:int, actionIndex:int):
        if self._actions is None:
            actions = dict()
            actions[38] = self.NEWLINE_action 
            actions[47] = self.OPEN_PAREN_action 
            actions[48] = self.CLOSE_PAREN_action 
            actions[49] = self.OPEN_BRACK_action 
            actions[50] = self.CLOSE_BRACK_action 
            self._actions = actions
        action = self._actions.get(ruleIndex, None)
        if action is not None:
            action(localctx, actionIndex)
        else:
            raise Exception("No registered action for:" + str(ruleIndex))


    def NEWLINE_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 0:

            tempt = Lexer.text.fget(self)
            newLine = re.sub("[^\r\n\f]+", "", tempt)
            spaces = re.sub("[\r\n\f]+", "", tempt)
            la_char = ""
            try:
                la = self._input.LA(1)
                la_char = chr(la)       # Python does not compare char to ints directly
            except ValueError:          # End of file
                pass
            # Strip newlines inside open clauses except if we are near EOF. We keep NEWLINEs near EOF to
            # satisfy the final newline needed by the single_put rule used by the REPL.
            try:
                nextnext_la = self._input.LA(2)
                nextnext_la_char = chr(nextnext_la)
            except ValueError:
                nextnext_eof = True
            else:
                nextnext_eof = False
            if self.opened > 0 or nextnext_eof is False and (la_char == '\r' or la_char == '\n' or la_char == '\f' or la_char == '#'):
                self.skip()
            else:
                indent = self.getIndentationCount(spaces)
                previous = self.indents[-1] if self.indents else 0
                self.emitToken(self.commonToken(self.NEWLINE, newLine, indent=indent))      # NEWLINE is actually the '\n' char
                if indent == previous:
                    self.skip()
                elif indent > previous:
                    self.indents.append(indent)
                    self.emitToken(self.commonToken(LanguageParser.INDENT, spaces))
                else:
                    while self.indents and self.indents[-1] > indent:
                        self.emitToken(self.createDedent())
                        self.indents.pop()
                
     

    def OPEN_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 1:
            self.opened += 1
     

    def CLOSE_PAREN_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 2:
            self.opened -= 1
     

    def OPEN_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 3:
            self.opened += 1
     

    def CLOSE_BRACK_action(self, localctx:RuleContext , actionIndex:int):
        if actionIndex == 4:
            self.opened -= 1
     

    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates is None:
            preds = dict()
            preds[38] = self.NEWLINE_sempred
            self._predicates = preds
        pred = self._predicates.get(ruleIndex, None)
        if pred is not None:
            return pred(localctx, predIndex)
        else:
            raise Exception("No registered predicate for:" + str(ruleIndex))

    def NEWLINE_sempred(self, localctx:RuleContext, predIndex:int):
            if predIndex == 0:
                return self.atStartOfInput()
         


