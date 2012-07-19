# -*- coding: utf-8 -*-
import json
import urllib2

class SetCounter:
    u"""(項目, 数) の辞書を作成するクラス"""
    
    def __init__(self):
        self._dict = {}         # (項目,数).
        self._set = set()       # 重複チェック用.
        
    def add(self, item):
        u"""項目の追加をする"""
        
        if isinstance(item, unicode) or isinstance(item, int):
            item_str = unicode(item).strip()
            if len(item_str) > 0:
                if item_str in self._set:
                    self._dict[item_str] += 1
                else:
                    self._dict[item_str] = 1
                    self._set.add(item_str)
        #else:
        #    print type(item)
                    
    def getDict(self):
        return self._dict

def print_SetCounter(set_cnt):
    u"""class SetCounterをprintする"""
    
    for k, v in sorted(set_cnt.getDict().items(), key=lambda x:x[1], reverse=True):
        print u"%3s %s" % (str(v), k)

# アンケートQ1の文.
Q1_BODY = [
u'創造する楽しみ・喜びのために。',
u'書いた結果がすぐに動き出すのがおもしろい。',
u'パズルを解くような楽しみ、問題を解く喜びがあるから。',
u'人間相手が苦手なので(!?)',
u'必要に迫られて。',
u'稼ぐために。',
]



# -- ここからstart --

"""
# ファイル版.
f = open('surveys.json')
exam_json = json.loads(f.read())
f.close()
"""

# url版.
exam_json = []
try:
    responce = urllib2.urlopen('http://code-survey.herokuapp.com/surveys.json')
    if responce.code == 200:
        exam_json = json.loads(
            responce.read()
            )
    
except urllib2.URLError, e:
    print e
except ValueError, e:
    print e

# 集計.
why_cnt = SetCounter()
locale_cnt   = SetCounter()
how_year_cnt = SetCounter()
free_comment_cnt = SetCounter()

for exam_row in exam_json:
    #print exam_row['id']
    #print exam_row['created_at']
    #print exam_row['app_name']
    #print exam_row['languages']
    
    if isinstance(exam_row['why'], unicode):
        q1_answer = exam_row['why'].split(',')
        for idx, ans in enumerate(q1_answer):
            if ans.find('true') != -1:
                why_cnt.add(Q1_BODY[idx])
    
    locale_cnt.add(exam_row['locale'])
    how_year_cnt.add(exam_row['how_year'])
    free_comment_cnt.add(exam_row['free_comment'])

# 表示.
print u"\n-------------------------------"
print u" 数 何故あなたはコードを書くか"
print u"-------------------------------"
print_SetCounter(why_cnt)

print u"\n-------------------------------"
print u" 人 コード歴"
print u"-------------------------------"
print_SetCounter(how_year_cnt)

print u"\n-------------------------------"
print u" 人 活動拠点"
print u"-------------------------------"
print_SetCounter(locale_cnt)

print u"\n-------------------------------"
print u" 人 フリーコメント"
print u"-------------------------------"
print_SetCounter(free_comment_cnt)

