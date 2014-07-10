from django import template
import re
import pygments
import pygments.lexers
import pygments.formatters

register = template.Library()

@register.filter
def stat_kep(value):
    csere=value.replace("__GAL_KEPEM:","<img src='/static/upl/").replace(":__", "'>")
    return csere

@register.filter
def hide_tag(value):
    return re.sub(r'__[A-Z]+\:[A-Z]+__', '', value)

@register.filter
def highlight_syntaxy(value):
    kezdesek=[(x.start(), x.end()) for x in re.finditer(r"__HL_(PY|HTML|RU):START__", value)]
    vegek=[(x.start(), x.end()) for x in re.finditer(r"__HL\:END__", value)]
    if len(kezdesek)==0 or len(kezdesek)!=len(vegek):
        return value
    last_end=0
    curr=""
    for k,v in zip(kezdesek, vegek):
        if value[k[0]:].startswith("__HL_HTML"):
            lexer=pygments.lexers.HtmlDjangoLexer()
        if value[k[0]:].startswith("__HL_PY"):
            lexer=pygments.lexers.PythonLexer()
        if value[k[0]:].startswith("__HL_RU"):
            lexer=pygments.lexers.RubyLexer()
        curr+=value[last_end:k[0]]
        formazando=value[k[1]:v[0]]
        curr+=pygments.highlight(formazando, lexer, pygments.formatters.HtmlFormatter())
        last_end=v[1]
    if last_end!=len(value):
        curr+=value[last_end:len(value)]
    return curr