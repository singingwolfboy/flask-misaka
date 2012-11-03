from flask import Flask, render_template_string
from unittest import TestCase

from flask.ext.misaka import Misaka

app = Flask(__name__)
app.debug = True
Misaka(app)

### templating tests ###

@app.route('/a')
def view_render_inline():
    s = u"This is *markdown*"
    return render_template_string('{{s|markdown}}', s=s)

def test_render_inline():
    client = app.test_client()
    resp = client.open('/a')
    assert resp.data == u'<p>This is <em>markdown</em></p>\n'

@app.route('/b')
def view_render_var_block():
    s = u"This is a *markdown* block"
    tpl = u'''{% filter markdown %}{{s}}{% endfilter %}'''
    return render_template_string(tpl, s=s)

def test_render_var_block():
    client = app.test_client()
    resp = client.open('/b')
    assert resp.data == u'<p>This is a <em>markdown</em> block</p>\n'

@app.route('/c')
def view_render_in_block():
    tpl = u'''{% filter markdown %}This is a *markdown* block{% endfilter %}'''
    return render_template_string(tpl)

def test_render_in_block():
    client = app.test_client()
    resp = client.open('/c')
    assert resp.data == u'<p>This is a <em>markdown</em> block</p>\n'

class MarkdownExtensionTests(TestCase):
    def test_defaults(self):
        md = Misaka()
        result = md.render("This ~~contains~~ some mark^(down) extensions: "
            "www.markdown.com foo_bar_baz it's")
        expected = (u"<p>This ~~contains~~ some mark^(down) extensions: "
            "www.markdown.com foo<em>bar</em>baz it&#39;s</p>\n")
        self.assertEqual(result, expected)

    def test_strikethrough(self):
        md = Misaka(strikethrough=True)
        result = md.render("That's ~~wrong~~ right!")
        self.assertEqual(result, u"<p>That&#39;s <del>wrong</del> right!</p>\n")

    def test_emphasis(self):
        md = Misaka(strikethrough=True)
        result = md.render("That's *right!*")
        self.assertEqual(result, u"<p>That&#39;s <em>right!</em></p>\n")

    def test_no_intra_emphasis(self):
        md = Misaka(intra_emphasis=False)
        result = md.render("foo_bar_baz")
        self.assertEqual(result, u"<p>foo_bar_baz</p>\n")


