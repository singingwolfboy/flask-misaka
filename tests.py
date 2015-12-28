from __future__ import unicode_literals
from flask import Flask, render_template_string, Markup
from unittest import TestCase
import mock

import misaka
from misaka import (EXT_AUTOLINK, EXT_FENCED_CODE,  # pyflakes.ignore
                    EXT_NO_INTRA_EMPHASIS, EXT_SPACE_HEADERS, EXT_STRIKETHROUGH,
                    EXT_SUPERSCRIPT, EXT_TABLES, HTML_ESCAPE, HTML_HARD_WRAP, HTML_SKIP_HTML,
                    HTML_USE_XHTML, TABLE_ALIGNMASK, TABLE_HEADER, TABLE_ALIGN_CENTER, TABLE_ALIGN_LEFT,
                    TABLE_ALIGN_RIGHT, EXT_MATH, EXT_FOOTNOTES, EXT_UNDERLINE, EXT_MATH_EXPLICIT,
                    EXT_DISABLE_INDENTED_CODE, EXT_HIGHLIGHT, EXT_QUOTE)

from flask_misaka import Misaka, markdown

TEST_MD = "*This* ~~contains~~ ``some`` mark^(down) extensions: www.markdown.com foo_bar_baz it's"

app = Flask(__name__)
app.debug = True
Misaka(app)

# templating tests #


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

# markdown extensions in templates

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
        ext, flags = EXT_FENCED_CODE | EXT_AUTOLINK, 0

        result = markdown(TEST_MD, fenced_code=True, autolink=True)

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
        ext, flags = 0, HTML_HARD_WRAP | HTML_ESCAPE

        result = markdown(TEST_MD, wrap=True, escape=True)

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
        flags = HTML_HARD_WRAP | HTML_USE_XHTML

        result = markdown(TEST_MD, strikethrough=True, superscript=True,
            hard_wrap=True, use_xhtml=True)

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
        ext, flags = 0, HTML_SKIP_HTML

        result = markdown(TEST_MD, no_html=True)

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
        ext, flags = 0, HTML_HARD_WRAP

        result = markdown(TEST_MD, hard_wrap=True, stupid_hard_wrap=False)

        html.assert_called_with(TEST_MD, extensions=ext, render_flags=flags)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, misaka.html(TEST_MD,
            extensions=ext, render_flags=flags))

    def test_set_defaults(self, html):
        ext, flags = EXT_TABLES, HTML_HARD_WRAP

        md = Misaka(hard_wrap=True, tables=True)
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

    def test_custom_renderer(self, html):

        class CustomRenderer(misaka.HtmlRenderer):
            def image(self, link, title, alt_text):
                return '<div><img src="{0}" alt="{2}" title="{1}"><div>{1}</div></div>'.format(
                    link, title, alt_text)

        test_md = '![Alt text](/img.jpg "Title")'
        expected_result = '<p><div><img src="/img.jpg" alt="Alt text" title="Title"><div>Title</div></div></p>\n'

        md = Misaka(None, CustomRenderer())
        result = md.render(test_md)
        self.assertFalse(html.called)
        self.assertEqual(str(result), expected_result)

    def test_smartypants(self, html):
        text = "Don't call me Shirley"
        pantsed = "Don&rsquo;t call me Shirley"
        expected_result = "<p>Don&rsquo;t call me Shirley</p>\n"

        md = Misaka(smartypants=True)
        result = md.render(text)

        html.assert_called_with(pantsed, extensions=0, render_flags=0)
        self.assertIsInstance(result, Markup)
        self.assertEqual(result, expected_result)


class FactoryPatternTests(TestCase):
    def test_init(self):
        md = Misaka()
        app2 = Flask(__name__)
        md.init_app(app2)
        self.assertIn("markdown", app2.jinja_env.filters)
