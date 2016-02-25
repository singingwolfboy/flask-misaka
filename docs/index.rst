Flask-Misaka
============

.. module:: flask_misaka

Flask-Misaka provides a pleasant interface between the `Flask`_ web framework
and the `Misaka`_ `Markdown`_ parser. [#technically]_

Installation
------------

Install the extension with:

.. code-block:: sh

  $ pip install Flask-Misaka

Usage
----------
Just import the :func:`markdown` function and use it!

.. code-block:: python

  >>> from flask.ext.misaka import markdown
  >>> markdown("A *simple* example.")
  Markup(u'<p>A <em>simple</em> example.</p>\n')

To use Markdown in your templates, you just need to import the :class:`Misaka`
class and wrap your Flask instance with it:

.. code-block:: python

  from flask import Flask
  from flask.ext.misaka import Misaka

  app = Flask(__name__)
  Misaka(app)

or use the :ref:`application factory pattern <flask:app-factories>`:

.. code-block:: python

  md = Misaka()
  app = Flask(__name__)
  md.init_app(app)

And then the ``markdown`` filter will be available in your `Jinja2`_ templates.
You can pass variables in your template through it:

.. code-block:: jinja

  {{ text|markdown }}

Or, you can use the ``filter`` tag to write your template directly in Markdown
and have Jinja dynamically interpret it for you!

.. code-block:: jinja

  {% filter markdown %}
  I'm writing my templates in *Markdown!*
  {% endfilter %}


API
---
.. autofunction:: markdown

.. autoclass:: Misaka
   :members: __init__, init_app, render

Options
-------
Misaka is very customizable, and `supports many Markdown extensions
<http://misaka.61924.nl/#extensions>`_. Flask-Misaka provides a nicer API for these
extensions. All functions in the public API (except :py:meth:`Misaka.init_app`)
accept the following boolean arguments, all of which default to False:

.. list-table:: Flask-Misaka options
    :header-rows: 1

    * - Option Name
      - Description

    * - ``autolink``
      - Parse links even when they are not enclosed in ``<>`` characters.
        Autolinks for the http, https and ftp protocols will be automatically
        detected. Email addresses are also handled, and http links without
        protocol, but starting with ``www``.

    * - ``fenced_code``
      - Blocks delimited with 3 or more ``~`` or backticks will be considered
        as code, without the need to be indented. An optional language name
        may be added at the end of the opening fence for the code block.

    * - ``underline``
      - Treat text surrounded by underscores (like ``_this_``) as underlined,
        rather than emphasized.

    * - ``highlight``
      - Treat text surrounded by double equal signs (like ``==this==``)
        as highlighted.

    * - ``quote``
      - Parse inline quotes (like ``"this"``). This allows the renderer to
        control how they are rendered.

    * - ``math``
      - Parse inline LaTeX-style math blocks (like ``$$this$$``).

    * - ``math_explicit``
      - Parse inline LaTeX-style math blocks with a single dollar, e.g.
        ``$x + y = 3$``

    * - ``disable_indented_code`` or ``no_indented_code``
      - Ignore indented code blocks

    * - ``no_intra_emphasis``
      - Do not parse emphasis inside of words. Strings such as ``foo_bar_baz``
        will not generate ``<em>`` tags.

    * - ``space_headers``
      - A space is always required between the hash at the beginning of
        a header and its name, e.g. ``#this is my header`` would not be
        a valid header.

    * - ``strikethrough``
      - Two ``~`` characters mark the start of a strikethrough, e.g.
        ``this is ~~good~~ bad``.

    * - ``superscript``
      - Parse superscripts after the ``^`` character; contiguous superscripts
        are nested together, and complex values can be enclosed in parenthesis,
        e.g. ``this is the 2^(nd) time``.

    * - ``tables``
      - Parse `PHP-Markdown tables`_.

    * - ``hard_wrap`` *or* ``wrap``
      - Insert HTML ``<br>`` tags inside on paragraphs where the origin
        Markdown document had newlines (by default, Markdown
        ignores these newlines).

    * - ``footnotes``
      - Parse Markdown footnotes.

    * - ``escape``
      - Escape all HTML tags, regardless of what they are.

    * - ``skip_html`` *or* ``no_html``
      - Do not allow any user-inputted HTML in the output.

    * - ``use_xhtml`` *or* ``xhtml``
      - Output XHTML-conformant tags.

    * - ``smartypants``
      - Post-process rendered markdown text with `SmartyPants`_.


Any option that starts with ``no_`` can also be passed as its inverse set to
False. For example, ``no_html=True`` and ``html=False`` have exactly the same
effect, just as ``no_intra_emphasis=True`` and ``intra_emphasis=False`` have
exactly the same effect.

.. note::
    To override an option, you must use exactly the same option name as you used
    to originally set the option. If you set ``html=False`` as a default, you
    must override it with ``html=True``: using ``no_html=False`` or
    ``skip_html=False`` will not work, even though they all refer to the same
    thing.

.. _Flask: http://flask.pocoo.org/
.. _Jinja2: http://jinja.pocoo.org/
.. _Misaka: http://misaka.61924.nl/
.. _Markdown: http://en.wikipedia.org/wiki/Markdown
.. _Hoedown: https://github.com/hoedown/hoedown
.. _PHP-Markdown tables: http://michelf.com/projects/php-markdown/extra/#table
.. _SmartyPants: http://daringfireball.net/projects/smartypants/
.. _inline LaTex-style math: https://github.com/bhollis/maruku/blob/master/docs/math.md

.. rubric:: Footnotes
.. [#technically]
  (Technically, `Misaka`_ is just a Python binding to the `Hoedown`_ library,
  which is written in C.)
