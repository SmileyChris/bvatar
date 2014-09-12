#!/usr/bin/env python
from PIL import Image
from bvatar import Bvatar

letters, numbers = 'abcdef', '123456'


def main():
    """
    Generate a grid of example bvatars.

    Usage: example.py [--mirror] [--no-king] [--multiplier=<num>]

    Options:
        --mirror            create mirrored avatars
        --no-king           don't use the new king algorithm
        --multiplier=<num>  Pixel multiplier [default: 8]
    """
    from docopt import docopt
    arguments = docopt(main.__doc__)

    multiplier = int(arguments['--multiplier'])
    border = int(multiplier * 1.5)
    offset = border + 8*multiplier

    grid = Image.new(
        'RGB',
        (offset * len(letters) + border,) * 2,
        '#333')

    for x, letter in enumerate(letters):
        for y, number in enumerate(numbers):
            name = letter+number
            bvtr = Bvatar(
                name, king=not arguments['--no-king'],
                mirror=arguments['--mirror'])
            grid.paste(
                bvtr.image(pxsize=multiplier),
                (x*offset + border, y*offset + border)
            )
    grid.show()


if __name__ == '__main__':
    main()
