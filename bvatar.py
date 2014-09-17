import base64
import colorsys
import hashlib
import itertools
import uuid
import sys

from bitarray import bitarray


class Bvatar(object):

    def __init__(self, source, mirror=False, is_hash=False, bits=3):
        if is_hash:
            self.bytes = base64.b16decode(source)
        else:
            self.bytes = hashlib.sha1(source).digest()
        self.mirror = mirror
        #: Number of bits per side (default is 3, so an 8x8 bvatar)
        self.size = bits
        self.walk()

    def _get_start_pos(self, bits):
        pos_bits = self.size * 2
        if self.mirror:
            pos_bits -= 1

        pos = 0
        for _ in range(pos_bits):
            pos <<= 1
            pos += bits.next()
        return pos

    def walk(self):
        """
        Walk the atrium.

        Bishop Peter finds himself in the middle of an ambient atrium. There
        are walls on all four sides and apparently there is no exit. The floor
        is paved with square tiles, strictly alternating between black and
        white. His head heavily aching probably from too much wine he had
        before he starts wandering around randomly, Well, to be exact, he
        usually makes diagonal steps just like a bishop on a chess board. When
        he hits a wall, he moves to the side. And after each move, he places a
        coin on the floor, to remember that he has been there before. Just
        when no coins are left, Peter suddenly wakes up. What a strange dream!
        """
        # Reset the atrium.
        wall_length = 2 ** self.size
        atrium_size = wall_length ** 2
        if self.mirror:
            atrium_size //= 2
        self.atrium = [0] * atrium_size
        if not self.mirror:
            self.atrium *= 2
        # Create a bitarray from the source's SHA.
        steps = bitarray(endian='big')
        steps.frombytes(self.bytes)

        king_tendancy = steps.copy()
        king_tendancy.reverse()
        king_tendancy = itertools.cycle(king_tendancy)
        steps = itertools.cycle(steps)

        # Mark the starting position.
        pos = start_pos = self._get_start_pos(steps)
        self.atrium[pos] += 1

        do_x, do_y = True, True
        for i in range(atrium_size * 2):
            x, y = steps.next(), steps.next()
            # As long as the Bishop didn't already walk like a king last step,
            # there's a 50% chance he will now.
            if do_x and do_y and king_tendancy.next():
                do_y = king_tendancy.next()
                do_x = not do_y
            else:
                do_x, do_y = True, True
            if do_x or not do_y:
                if x:
                    pos += wall_length if pos < atrium_size-wall_length else 0
                else:
                    pos -= wall_length if pos >= wall_length else 0
            if do_y or not do_x:
                if y:
                    pos += (1 if (pos+1) % wall_length else 0)
                else:
                    pos -= (1 if pos % wall_length else 0)
            # Leave a coin.
            self.atrium[pos] += 1

            if i == atrium_size - 1:
                # Pick a new starting position.
                pos = self._get_start_pos(steps)

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

    def _get_hue_and_sat(self):
        color_bits = bitarray(endian='big')
        color_bits.frombytes(hashlib.sha1(self.bytes).digest())
        hue = int(color_bits[:8].to01(), 2) / 255.0
        sat = int(color_bits[8:12].to01(), 2) / 15.0 * .8 + 0.2
        return hue, sat

    def color(self, lightness=0.5, hue_offset=0):
        hue, sat = self._get_hue_and_sat()
        return colorsys.hls_to_rgb(hue+hue_offset, lightness, sat)

    def image(self, color=0.75, pxsize=1, fill=False):
        from PIL import Image

        min_lightness = 0.1
        if color:
            hue, sat = self._get_hue_and_sat()
            sat *= color
            max_lightness = 0.75
        else:
            hue = 1
            sat = 0
            max_lightness = 1

        wall_length = 2 ** self.size
        if fill:
            bgcolor = tuple(int(255*p) for p in self.color(max_lightness))
        else:
            bgcolor = 'white'
        img = Image.new('RGB', (wall_length, wall_length), bgcolor)
        max_weight = float(max(self.atrium))
        light_weight = max_lightness-min_lightness
        for point, weight in enumerate(self.atrium):
            if not weight:
                continue
            x, y = point // wall_length, point % wall_length
            hls = (
                hue,
                min_lightness + (1-weight/max_weight)*light_weight,
                sat,
            )
            pxcolor = tuple(int(255*p) for p in colorsys.hls_to_rgb(*hls))
            img.putpixel((x, y), pxcolor)
            if self.mirror:
                img.putpixel((wall_length-1-x, y), pxcolor)

        if pxsize > 1:
            img = img.resize((wall_length*pxsize,)*2)

        return img


def main():
    """
    Generate a Bvatar (an 8x8 randomart avatar).

    Usage:
        bvatar [--mirror] [--saturation=<float>] [--fill] [--px-size=<int>] ([TEXT] | [--hash=<sha1_hash>])
        bvatar --ascii [--mirror] [--spaced] [--no-border] ([TEXT] | [--hash=<sha1_hash>])

    Arguments:
        TEXT  bvatar source text (otherwise a random bvatar is generated)

    Options:
        --mirror              generate a horizontally mirrored bvatar
        --saturation=<float>  color saturation (use 0 for greyscale image)
                              [default: 0.75]
        --fill                fill background with lightest saturation of the
                              bvatar's color
        --px-size=<int>       actual size for each pixel [default: 16]
        --hash=<sha1_hash>    rather than passing the text and having it
                              SHA1ed, you can pass a hex encoded SHA1 hash
                              explicitly
        --ascii               output ascii rather than generating a bitmap
                              image
        --spaced              a "lighter" ascii art alternative
        --no-border           don't add a border around the ascii art
    """
    from docopt import docopt
    arguments = docopt(main.__doc__)

    is_hash = arguments['--hash']
    source = arguments['TEXT'] or is_hash or uuid.uuid4().bytes
    bvatar = Bvatar(source, mirror=arguments['--mirror'], is_hash=is_hash)

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
        kwargs = {}
        img = bvatar.image(
            pxsize=int(arguments['--px-size']),
            color=float(arguments['--saturation']),
            fill=arguments['--fill']
        )
        if sys.stdout.isatty():
            img.show()
        else:
            img.save(sys.stdout, 'PNG')


if __name__ == '__main__':
    main()
