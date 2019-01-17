from __future__ import absolute_import, unicode_literals

__version__ = '1.0.0'

import misaka
from flask import Markup
from copy import copy

# import constants for compatibility
from misaka import (EXT_AUTOLINK, EXT_FENCED_CODE,  # pyflakes.ignore
                    EXT_NO_INTRA_EMPHASIS, EXT_SPACE_HEADERS, EXT_STRIKETHROUGH,
                    EXT_SUPERSCRIPT, EXT_TABLES, HTML_ESCAPE, HTML_HARD_WRAP, HTML_SKIP_HTML,
                    HTML_USE_XHTML, TABLE_ALIGNMASK, TABLE_HEADER, TABLE_ALIGN_CENTER, TABLE_ALIGN_LEFT,
                    TABLE_ALIGN_RIGHT, EXT_MATH, EXT_FOOTNOTES, EXT_UNDERLINE, EXT_MATH_EXPLICIT,
                    EXT_DISABLE_INDENTED_CODE, EXT_HIGHLIGHT, EXT_QUOTE)

ALIAS_EXT = {
    'autolink': EXT_AUTOLINK,
    'fenced_code': EXT_FENCED_CODE,
    'no_intra_emphasis': EXT_NO_INTRA_EMPHASIS,
    'space_headers': EXT_SPACE_HEADERS,
    'strikethrough': EXT_STRIKETHROUGH,
    'superscript': EXT_SUPERSCRIPT,
    'tables': EXT_TABLES,
    'math': EXT_MATH,
    'footnotes': EXT_FOOTNOTES,
    'underline': EXT_UNDERLINE,
    'math_explicit': EXT_MATH_EXPLICIT,
    'disable_indented_code': EXT_DISABLE_INDENTED_CODE,
    'no_indented_code': EXT_DISABLE_INDENTED_CODE,
    'highlight': EXT_HIGHLIGHT,
    'quote': EXT_QUOTE
}

ALIAS_RENDER = {
    'escape': HTML_ESCAPE,
    'hard_wrap': HTML_HARD_WRAP,
    'wrap': HTML_HARD_WRAP,
    'skip_html': HTML_SKIP_HTML,
    'no_html': HTML_SKIP_HTML,
    'use_xhtml': HTML_USE_XHTML,
    'xhtml': HTML_USE_XHTML,
}


def make_flags(**options):
    ext = 0
    for name, val in ALIAS_EXT.items():
        if options.get(name):
            ext = ext | val
        if name.startswith("no_"):
            if options.get(name[3:]) is False:
                ext = ext | val

    rndr = 0
    for name, val in ALIAS_RENDER.items():
        if options.get(name):
            rndr = rndr | val
        if name.startswith("no_"):
            if options.get(name[3:]) is False:
                rndr = rndr | val

    return ext, rndr


def markdown(text, renderer=None, **options):
    """
    Parses the provided Markdown-formatted text into valid HTML, and returns
    it as a :class:`flask.Markup` instance.

    :param text: Markdown-formatted text to be rendered into HTML
    :param renderer: A custom misaka renderer to be used instead of the default one
    :param options: Additional options for customizing the default renderer
    :return: A :class:`flask.Markup` instance representing the rendered text
    """
    ext, rndr = make_flags(**options)
    if renderer:
        md = misaka.Markdown(renderer,ext)
        result = md(text)
    else:
        result = misaka.html(text, extensions=ext, render_flags=rndr)
    if options.get("smartypants"):
        result = misaka.smartypants(result)
    return Markup(result)


class Misaka(object):
    def __init__(self, app=None, renderer=None, **defaults):
        """
        Set the default options for the :meth:`render` method. If you want
        the ``markdown`` template filter to use options, set them here.

        A custom misaka renderer can be specified to be used instead of the
        default one.
        """
        self.renderer = renderer
        self.defaults = defaults
        if app:
            self.init_app(app)

    def init_app(self, app):
        """
        Registers the rendering method as template filter.

        :param app: a :class:`flask.Flask` instance.
        """
        app.jinja_env.filters.setdefault('markdown', self.render)

    def render(self, text, **overrides):
        """
        It delegates to the :func:`markdown` function, passing any default
        options or renderer set in the :meth:`__init__` method.

        The ``markdown`` template filter calls this method.

        :param text: Markdown-formatted text to be rendered to HTML
        :param overrides: Additional options which may override the defaults
        :return: A :class:`flask.Markup` instance representing the rendered text
        """
        options = self.defaults
        if overrides:
            options = copy(options)
            options.update(overrides)
        return markdown(text, self.renderer, **options)
