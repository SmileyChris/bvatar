===========================
Bvatar - Random Art Avatars
===========================

Bvatar creates a unique 8x8 graphical representation of a string.


Setup
=====

Install from PYPI
-----------------

Install with the following pip command::

    pip install bvatar

If you want to be able to create bitmap images, use this as the final
installation command instead::

    pip install bvatar[bitmap]


Install development version
---------------------------

Download from github and install the development version with these commands::

    git clone https://github.com/smileychris/bvatar
    cd bvatar
    pip install -e .[bitmap]


Usage
=====

Import the bvatar class and use it like so:

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
    ``--no-color``
        use greyscale rather than coloring the image
    ``--px-size=<int>``
        actual size for each pixel [default: 16]
    ``--hash=<sha1_hash>``
        rather than passing the text and having it SHA1ed, you can pass a hex
        encoded SHA1 hash explicitly
    ``--ascii``
        output ascii rather than generating a bitmap image
    ``--spaced``
        a "lighter" ascii art alternative
    ``--no-border``
        don't add a border around the ascii art
