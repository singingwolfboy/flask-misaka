from __future__ import unicode_literals
from flask import Flask, render_template_string, Markup
from unittest import TestCase
import mock

import misaka
from misaka import (EXT_AUTOLINK, EXT_FENCED_CODE,
    EXT_LAX_HTML_BLOCKS, EXT_NO_INTRA_EMPHASIS, EXT_SPACE_HEADERS,
    EXT_STRIKETHROUGH, EXT_SUPERSCRIPT, EXT_TABLES, HTML_ESCAPE,
    HTML_EXPAND_TABS, HTML_HARD_WRAP, HTML_SAFELINK, HTML_SKIP_HTML,
    HTML_SKIP_IMAGES, HTML_SKIP_LINKS, HTML_SKIP_STYLE, HTML_SMARTYPANTS,
    HTML_TOC, HTML_TOC_TREE, HTML_USE_XHTML, TABLE_ALIGNMASK, TABLE_ALIGN_C,
    TABLE_ALIGN_L, TABLE_ALIGN_R, TABLE_HEADER)
from flask.ext.misaka import Misaka, markdown

TEST_MD = "*This* ~~contains~~ ``some`` mark^(down) extensions: www.markdown.com foo_bar_baz it's"

app = Flask(__name__)
app.debug = True
Misaka(app)

### templating tests ###

@app.route('/a')
def view_render_inline():
    s = "This is ~~restructuredtext~~ *markdown*"
    return render_template_string('{{s|markdown}}', s=s)

def test_render_inline():
    client = app.test_client()
    resp = client.open('/a')
    assert resp.data == b'<p>This is ~~restructuredtext~~ <em>markdown</em></p>\n'

@app.route('/b')
def view_render_var_block():
    s = "This is a *markdown* block"
    tpl = '''{% filter markdown %}{{s}}{% endfilter %}'''
    return render_template_string(tpl, s=s)

def test_render_var_block():
    client = app.test_client()
    resp = client.open('/b')
    assert resp.data == b'<p>This is a <em>markdown</em> block</p>\n'

@app.route('/c')
def view_render_in_block():
    tpl = '''{% filter markdown %}This is a *markdown* block{% endfilter %}'''
    return render_template_string(tpl)

def test_render_in_block():
    client = app.test_client()
    resp = client.open('/c')
    assert resp.data == b'<p>This is a <em>markdown</em> block</p>\n'

### markdown extensions in templates

extapp = Flask(__name__)
extapp.debug = True
Misaka(extapp, strikethrough=True)

@extapp.route('/d')
def view_render_inline_ext():
    s = "This is ~~restructuredtext~~ *markdown*"
    return render_template_string('{{s|markdown}}', s=s)

def test_render_inline_ext():
    client = extapp.test_client()
    resp = client.open('/d')
    assert resp.data == b'<p>This is <del>restructuredtext</del> <em>markdown</em></p>\n'

# Note that the Markdown extension tests aren't actually testing that the
# Markdown is rendered correctly; that should be covered by the test suite of
# the misaka module. These tests should test that Flask-Misaka is calling
# the misaka module correctly, and returning the result unmodified
# (aside from being wrapped in a Markup class instance.)

@mock.patch("flask.ext.misaka.misaka.html", side_effect=misaka.html)
class MarkdownExtensionTests(TestCase):
    def test_defaults(self, html):
        ext, flags = 0, 0

        result = markdown(TEST_MD)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_one_ext(self, html):
        ext, flags = EXT_AUTOLINK, 0

        result = markdown(TEST_MD, autolink=True)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_two_ext(self, html):
        ext, flags = EXT_FENCED_CODE | EXT_LAX_HTML_BLOCKS, 0

        result = markdown(TEST_MD, fenced_code=True, lax_html=True)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_one_render(self, html):
        ext, flags = 0, HTML_ESCAPE

        result = markdown(TEST_MD, escape=True)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_two_render(self, html):
        ext, flags = 0, HTML_HARD_WRAP | HTML_SAFELINK

        result = markdown(TEST_MD, wrap=True, safelink=True)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_one_ext_one_render(self, html):
        ext, flags = EXT_NO_INTRA_EMPHASIS, HTML_SKIP_HTML

        result = markdown(TEST_MD, no_intra_emphasis=True, no_html=True)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_two_ext_two_render(self, html):
        ext = EXT_STRIKETHROUGH | EXT_SUPERSCRIPT
        flags = HTML_SKIP_LINKS | HTML_SKIP_STYLE

        result = markdown(TEST_MD, strikethrough=True, superscript=True,
            skip_links=True, no_style=True)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_inverse_ext(self, html):
        ext, flags = EXT_NO_INTRA_EMPHASIS, 0

        result = markdown(TEST_MD, intra_emphasis=False)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_inverse_render(self, html):
        ext, flags = 0, HTML_SKIP_STYLE

        result = markdown(TEST_MD, style=False)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_undefined_option(self, html):
        ext, flags = 0, 0

        result = markdown(TEST_MD, fireworks=True)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_defined_and_undefined_options(self, html):
        ext, flags = 0, HTML_SMARTYPANTS

        result = markdown(TEST_MD, smartypants=True, stupidpants=False)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_set_defaults(self, html):
        ext, flags = EXT_TABLES, HTML_SMARTYPANTS

        md = Misaka(smartypants=True, tables=True)
        result = md.render(TEST_MD)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_override_defaults(self, html):
        ext, flags = 0, 0

        md = Misaka(autolink=True)
        result = md.render(TEST_MD, autolink=False)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

class FactoryPatternTests(TestCase):
    def test_init(self):
        md = Misaka()
        app2 = Flask(__name__)
        md.init_app(app2)
        self.assertIn("markdown", app2.jinja_env.filters)
