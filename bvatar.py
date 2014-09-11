import base64
import colorsys
import hashlib
import uuid
import sys

from bitarray import bitarray


class Bvatar(object):

    def __init__(self, source, mirror=False, is_hash=False):
        if is_hash:
            self.bytes = base64.b16decode(source)
        else:
            self.bytes = hashlib.sha1(source).digest()
        self.mirror = mirror
        self.walk()

    def walk(self):
        """
        Walk the atrium.

        Bishop Peter finds himself in the middle of an ambient atrium. There
        are walls on all four sides and apparently there is no exit. The floor
        is paved with square tiles, strictly alternating between black and
        white. His head heavily aching probably from too much wine he had
        before he starts wandering around randomly, Well, to be exact, he only
        makes diagonal steps just like a bishop on a chess board. When he hits
        a wall, he moves to the side, which takes him from the black tiles to
        the white tiles (or vice versa). And after each move, he places a coin
        on the floor, to remember that he has been there before. Just when no
        coins are left, Peter suddenly wakes up. What a strange dream!
        """
        # Reset the atrium.
        atrium_size = 32 if self.mirror else 64
        self.atrium = [0] * atrium_size
        if not self.mirror:
            self.atrium *= 2
        # Create a bitarray from the source's SHA.
        steps = bitarray(endian='big')
        steps.frombytes(self.bytes)

        # First bits are the position, the rest are the steps.
        pos_bits = 5 if self.mirror else 6
        pos, steps = int(steps[:pos_bits].to01(), 2), steps[pos_bits:]

        # Mark the starting position.
        self.atrium[pos] += 1
        while True:
            try:
                x, y = steps.pop(), steps.pop()
            except IndexError:
                # No more steps to consume.
                break
            if x:
                pos += 8 if pos < atrium_size-8 else 0
            else:
                pos -= 8 if pos >= 8 else 0
            if y:
                pos += (1 if (pos+1) % 8 else 0)
            else:
                pos -= (1 if pos % 8 else 0)
            # Leave a coin.
            self.atrium[pos] += 1


    def ascii(self, stdout=None, spaced=False, border=True):
        if spaced:
            # Custom single
            values=' .,:;oix%08X&#@'
        else:
            # Use SSL keyart characters
            values = ' .o+=*BOX@%&#/^'
            # values = '.^:li?(fxXZ#MW&8%@'  # keyart values
        stdout = stdout or sys.stdout
        max_weight = float(max(self.atrium))
        max_value = len(values) - 1
        if self.mirror:
            x_range = range(4) + range(3, -1, -1)
        else:
            x_range = range(8)
        if border:
            stdout.write('+' + '-'*16)
            if spaced:
                stdout.write('-')
            stdout.write('+\n')
        for y in range(8):
            if border:
                stdout.write('|')
            for x in x_range:
                weight = self.atrium[y+x*8] / max_weight
                value = values[int(max_value * weight)]
                if spaced:
                    value = ' ' + value
                else:
                    value *= 2
                stdout.write(value)
            if border:
                if spaced:
                    stdout.write(' ')
                stdout.write('|')
            stdout.write('\n')
        if border:
            stdout.write('+' + '-'*16)
            if spaced:
                stdout.write('-')
            stdout.write('+\n')

    def _get_color_bits(self):
        color_bits = bitarray(endian='big')
        color_bits.frombytes(hashlib.sha1(self.bytes).digest())
        return color_bits

    def image(self, color=True, pxsize=1):
        from PIL import Image

        if color:
            color_bits = self._get_color_bits()
            hue = int(color_bits[:4].to01(), 2) / 16.0
            sat = int(color_bits[4:6].to01(), 2) / 4.0 * 0.5 + 0.2
            max_lightness = 0.75
        else:
            hue = 1
            sat = 0
            max_lightness = 1

        img = Image.new('RGB', (8, 8), 'white')
        max_weight = float(max(self.atrium))
        for point, weight in enumerate(self.atrium):
            if not weight:
                continue
            x, y = point // 8, point % 8
            hls = (hue, weight / max_weight * max_lightness, sat)
            color = tuple(
                200 - int(200 * p) for p in colorsys.hls_to_rgb(*hls))
            img.putpixel((x, y), color)
            if self.mirror:
                img.putpixel((7-x, y), color)

        if pxsize > 1:
            img = img.resize((8*pxsize,)*2)
        return img


def main():
    """
    Generate a Bvatar (an 8x8 randomart avatar).

    Usage:
        bvatar [--mirror] [--no-color] [--px-size=<int>] ([TEXT] | [--hash=<sha1_hash>])
        bvatar --ascii [--mirror] [--spaced] [--no-border] ([TEXT] | [--hash=<sha1_hash>])

    Arguments:
        TEXT  bvatar source text (otherwise a random bvatar is generated)

    Options:
        --mirror            generate a horizontally mirrored bvatar
        --no-color          use greyscale rather than coloring the image
        --px-size=<int>     actual size for each pixel [default: 16]
        --hash=<sha1_hash>  rather than passing the text and having it SHA1ed,
                            you can pass a hex encoded SHA1 hash explicitly
        --ascii             output ascii rather than generating a bitmap image
        --spaced            a "lighter" ascii art alternative
        --no-border         don't add a border around the ascii art
    """
    from docopt import docopt
    arguments = docopt(main.__doc__)

    source = arguments['TEXT'] or arguments['--hash'] or uuid.uuid4().bytes
    bvatar = Bvatar(source, mirror=arguments['--mirror'])

    use_ascii = arguments['--ascii']
    if not use_ascii and sys.stdout.isatty():
        try:
            from PIL import Image
        except ImportError:
            import warnings
            warnings.warn('PIL is not installed, falling back to ASCII')
            use_ascii = True

    if use_ascii:
        bvatar.ascii(
            spaced=arguments['--spaced'], border=not arguments['--no-border'])
    else:
        img = bvatar.image(
            pxsize=int(arguments['--px-size']),
            color=not arguments['--no-color']
        )
        if sys.stdout.isatty():
            img.show()
        else:
            img.save(sys.stdout, 'PNG')


if __name__ == '__main__':
    main()
