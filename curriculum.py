"""Curriculum evidence is separate from unverified reading recommendations."""
import json
from atlas import ROOT
EVIDENCE=json.loads((ROOT/'data/curriculum-evidence.json').read_text())
BOOKS={b['id']:b for b in EVIDENCE['books']}
LINKS={x['work_id']:{**x,'book':BOOKS[x['book_id']]}for x in EVIDENCE['links']}

def category(grammar):
    if '代词' in grammar:return '指代用法（待教材定类）'
    if any(k in grammar for k in ('连词','助词','介词','副词','语气','疑问')):return '虚词候选'
    if any(k in grammar for k in ('名词','动词','形容','数量','使动','活用','古今')):return '实词候选'
    return '待分类'

def enrich(d):
    for w in d['works']:
        w['curriculum']=LINKS.get(w['id'])
        w['material_status']='directory_checked' if w['curriculum'] else 'unverified'
    sentences={s['id']:s for s in d['sentences']};lexemes={l['id']:l for l in d['lexemes']}
    for sense in d['senses']:sense['word_class']=category(sense['grammar'])
    for o in d['occurrences']:
        sentence=sentences[o['sentence_id']];word=lexemes[o['lexeme_id']]['text']
        o['gloss_check']=next((g for g in EVIDENCE['gloss_checks'] if g['work_id']==sentence['work_id']and g['word']==word and g['anchor']in sentence['text']),None)
    return d
