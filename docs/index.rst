Flask-Misaka
============

.. module:: flask.ext.misaka

Flask-Misaka provides a pleasant interface between the `Flask`_ web framework
and the `Misaka`_ `Markdown`_ parser. [#sundown]_

Installation
------------

Install the extension with:

.. code-block:: sh

  $ pip install Flask-Misaka

Usage
----------
Just import the :func:`markdown` function and use it!

  >>> from flaskext.misaka import markdown
  >>> markdown("A *simple* example.")
  Markup(u'<p>A <em>simple</em> example.</p>\n')

To use Markdown in your templates, you just need to import the :class:`Misaka`
class and wrap your Flask instance with it::

  from flask import Flask
  from flaskext.misaka import Misaka

  app = Flask(__name__)
  Misaka(app)

And then the ``markdown`` filter will be available in your `Jinja2`_ templates.
You can pass variables in your template through it:

.. code-block:: jinja

  {{ text|markdown }}

Or, you can use the ``filter`` tag to write your template directly in Markdown
and have Jinja dynamically interpret it for you! That&#39;s right!

.. code-block:: jinja

  {% filter markdown %}
  I'm writing my templates in *Markdown!*
  {% endfilter %}


API
===
.. autofunction:: markdown

Options
-------
Misaka is very customizable, and `supports many Markdown extensions
<http://misaka.61924.nl/api/>`_. Flask-Misaka provides a nicer API for these
extensions. Any function or method that accepts ``**options`` or ``**overrides``
accepts the following boolean arguments, all of which default to False:

+-----------------------+-------------------------------------------------------+
| Option Name           | Description                                           |
+=======================+=======================================================+
| ``no_intra_emphasis`` | Do not parse emphasis inside of words. Strings such   |
|                       | as ``foo_bar_baz`` will not generate ``<em>`` tags.   |
+-----------------------+-------------------------------------------------------+
| ``autolink``          | Parse links even when they are not enclosed in ``<>`` |
|                       | characters. Autolinks for the http, https and ftp     |
|                       | protocols will be automatically detected. Email       |
|                       | addresses are also handled, and http links without    |
|                       | protocol, but starting with ``www``.                  |
+-----------------------+-------------------------------------------------------+
| ``fenced_code``       | Blocks delimited with 3 or more ``~`` or backticks    |
|                       | will be considered as code, without the need to be    |
|                       | indented. An optional language name may be added at   |
|                       | the end of the opening fence for the code block.      |
+-----------------------+-------------------------------------------------------+
| ``lax_html`` *or*     | HTML blocks do not require to be surrounded by an     |
| ``lax_html_blocks``   | empty line as in the Markdown standard.               |
+-----------------------+-------------------------------------------------------+
| ``space_headers``     | A space is always required between the hash at the    |
|                       | beginning of a header and its name, e.g.              |
|                       | ``#this is my header`` would not be a valid header.   |
+-----------------------+-------------------------------------------------------+
| ``strikethrough``     | Two ``~`` characters mark the start of a              |
|                       | strikethrough, e.g. ``this is ~~good~~ bad``.         |
+-----------------------+-------------------------------------------------------+
| ``superscript``       | Parse superscripts after the ``^`` character;         |
|                       | contiguous superscripts are nested together, and      |
|                       | complex values can be enclosed in parenthesis, e.g.   |
|                       | ``this is the 2^(nd) time``.                          |
+-----------------------+-------------------------------------------------------+
| ``tables``            | Parse `PHP-Markdown tables`_.                         |
+-----------------------+-------------------------------------------------------+
| ``escape``            | Escape all HTML tags, regardless of what they are.    |
+-----------------------+-------------------------------------------------------+


.. _Flask: http://flask.pocoo.org/
.. _Jinja2: http://jinja.pocoo.org/
.. _Misaka: http://misaka.61924.nl/
.. _Markdown: http://en.wikipedia.org/wiki/Markdown
.. _Sundown: https://github.com/vmg/sundown
.. _PHP-Markdown tables: http://michelf.com/projects/php-markdown/extra/#table

.. rubric:: Footnotes
.. [#sundown]
  (Technically, `Misaka`_ is just a Python binding to the `Sundown`_ library,
  which is written in C.)
