from django import template
from django.template import Node, NodeList, Variable, Context
from django.template import TemplateSyntaxError, VariableDoesNotExist

register = template.Library()

class IsMusiphileCreatorNode(Node):
    def __init__(self, musiphile, playlist, nodelist_true, nodelist_false):
        self.musiphile, self.playlist = Variable(musiphile), Variable(playlist)
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false

    def __repr__(self):
        return '<IsMusphileCreatorNode>'

    def render(self,context):
        musiphile,playlist = None,None
        try:
            musiphile = self.musiphile.resolve(context)
        except VariableDoesNotExist:
            pass

        try:
            playlist = self.playlist.resolve(context)
        except VariableDoesNotExist:
            pass

        if not musiphile or not playlist:
            return self.nodelist_false.render(context)

        return self.nodelist_true.render(context) if musiphile==playlist.creator else self.nodelist_false.render(context)

def do_is_musiphile_creator(parser, token):
    bits = list(token.split_contents())
    if len(bits) != 3:
        raise TemplateSyntaxError, '%r takes two arguments' % bits[0]
    end_tag = 'end' + bits[0]

    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    return IsMusiphileCreatorNode(bits[1],bits[2],nodelist_true,nodelist_false)
register.tag('ifmusiphileiscreator', do_is_musiphile_creator)
