from __future__ import absolute_import, unicode_literals

import misaka
from flask import Markup
from copy import copy

# import constants for compatibility
from misaka import (EXT_AUTOLINK, EXT_FENCED_CODE,  # pyflakes.ignore
    EXT_LAX_HTML_BLOCKS, EXT_NO_INTRA_EMPHASIS, EXT_SPACE_HEADERS,
    EXT_STRIKETHROUGH, EXT_SUPERSCRIPT, EXT_TABLES, HTML_ESCAPE,
    HTML_EXPAND_TABS, HTML_HARD_WRAP, HTML_SAFELINK, HTML_SKIP_HTML,
    HTML_SKIP_IMAGES, HTML_SKIP_LINKS, HTML_SKIP_STYLE, HTML_SMARTYPANTS,
    HTML_TOC, HTML_TOC_TREE, HTML_USE_XHTML, TABLE_ALIGNMASK, TABLE_ALIGN_C,
    TABLE_ALIGN_L, TABLE_ALIGN_R, TABLE_HEADER)

ALIAS_EXT = {
    'autolink': EXT_AUTOLINK,
    'fenced_code': EXT_FENCED_CODE,
    'lax_html': EXT_LAX_HTML_BLOCKS,
    'lax_html_blocks': EXT_LAX_HTML_BLOCKS,
    'no_intra_emphasis': EXT_NO_INTRA_EMPHASIS,
    'space_headers': EXT_SPACE_HEADERS,
    'strikethrough': EXT_STRIKETHROUGH,
    'superscript': EXT_SUPERSCRIPT,
    'tables': EXT_TABLES,
}

ALIAS_RENDER = {
    'escape': HTML_ESCAPE,
    'hard_wrap': HTML_HARD_WRAP,
    'wrap': HTML_HARD_WRAP,
    'safelink': HTML_SAFELINK,
    'skip_html': HTML_SKIP_HTML,
    'no_html': HTML_SKIP_HTML,
    'skip_images': HTML_SKIP_IMAGES,
    'no_images': HTML_SKIP_IMAGES,
    'skip_links': HTML_SKIP_LINKS,
    'no_links': HTML_SKIP_LINKS,
    'skip_style': HTML_SKIP_STYLE,
    'no_style': HTML_SKIP_STYLE,
    'smartypants': HTML_SMARTYPANTS,
    'toc': HTML_TOC,
    'toc_tree': HTML_TOC_TREE,
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


def markdown(text, **options):
    """
    Parses the provided Markdown-formatted text into valid HTML, and returns
    it as a :class:`flask.Markup` instance.
    """
    ext, rndr = make_flags(**options)
    return Markup(misaka.html(text, extensions=ext, render_flags=rndr))


class Misaka(object):
    def __init__(self, app=None, **defaults):
        """
        Set the default options for the :meth:`render` method. If you want
        the ``markdown`` template filter to use options, set them here.
        """
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
        Proxies to the :func:`markdown` function, automatically passing any
        defaults set in the :meth:`__init__` method (or overriding them).

        The ``markdown`` template filter calls this method.
        """
        options = self.defaults
        if overrides:
            options = copy(options)
            options.update(overrides)
        return markdown(text, **options)
