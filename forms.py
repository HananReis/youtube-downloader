"""Arquivo de referência para formulários relacionados a posts.
Não dependemos de Flask-WTF aqui (Flask puro), então este arquivo serve como documentação
/ estrutura para uma possível migração futura. A exigência foi que o campo de conteúdo
seja um HiddenField chamado "content" (o HTML do editor Quill será enviado para esse campo).
"""
from dataclasses import dataclass

@dataclass
class PostForm:
    title: str = ''
    # Conteúdo HTML do post (enviado via campo hidden 'content')
    content: str = ''
    # published é booleano (True/False)
    published: bool = False

    # Observação: o projeto atual usa formulários HTML puros nas templates; este dataclass
    # apenas documenta a forma esperada dos dados e pode ser usado para validações simples.
