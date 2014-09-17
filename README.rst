===========================
Bvatar - Random Art Avatars
===========================

Bvatar creates a unique 8x8 graphical representation of a string.


Setup
=====

Install from PYPI
-----------------

For a full install (to be able to create bitmap images), use the following pip
command::

    pip install bvatar[bitmap]

Or, if for some reason you only want to output ascii bvatars, just use:
``pip install bvatar``


Install development version
---------------------------

Download from github and install the development version with these commands::

    git clone https://github.com/smileychris/bvatar
    cd bvatar
    pip install -e .[bitmap]


Usage
=====

Import the bvatar class and use it like so:

.. code:: python

    from bvatar import Bvatar
    bvtr = Bvatar('text')
    img = bvtr.image()
    img.save('some_file.png', 'PNG')


Command-line Script
===================

Generate a Bvatar (an 8x8 randomart avatar).

Usage::

    bvatar [--mirror] [--no-color] [--px-size=<int>] ([TEXT] | [--hash=<sha1_hash>])
    bvatar --ascii [--mirror] [--spaced] [--no-border] ([TEXT] | [--hash=<sha1_hash>])

The first format is for generating bitmap images. By default, the image is
only displayed and not stored. To save the image, pipe to a file::

    bvatar > some_file.png

Arguments:

``TEXT``
    bvatar source text (otherwise a random bvatar is generated)

Options:

``--mirror``
    generate a horizontally mirrored bvatar
``--ascii``
    output ascii rather than generating a bitmap image
``--hash=<sha1_hash>``
    rather than passing the text and having it SHA1ed, you can pass a hex
    encoded SHA1 hash explicitly

Extra options when generating an image (i.e. not using``--ascii``):

``--saturation``
    color saturation (use 0 for greyscale image) [default: 0.75]
``--fill``
    fill background with lightest saturation of the bvatar's color
``--px-size=<int>``
    actual size for each pixel [default: 16]

Extra options when using ``--ascii``:

``--spaced``
    a "lighter" ascii art alternative
``--no-border``
    don't add a border around the ascii art
