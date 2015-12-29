import math

class Field(object):
    """Class for handling field information.

    This is the class for handling the field information on the sky. The values contained
    within the class are all kept in degrees. Properties are exposed that present those
    values in radians.
    """

    def __init__(self, fid, fov, ra, dec, gl, gb, el, eb):
        """Initialize the class.

        NOTE: All angular values are expected to be in degrees!

        Args:
            fid (int): The field's ID.
            fov (float): The field's field-of-view.
            ra (float): The field's right ascension.
            dec (float): The field's declination.
            gl (float): The field's galactic latitude.
            gb (float): The field's galactic longitude.
            el (float): The field's ecliptic latitude.
            eb (float): The field's ecliptic longitude.
        """
        self.fid = fid
        self.fov = fov
        self.ra = ra
        self.dec = dec
        self.gl = gl
        self.gb = gb
        self.el = el
        self.eb = eb

    @classmethod
    def from_topic(cls, topic):
        """Alternate initializer.

        Args:
            topic (SALPY_scheduler.fieldC): The field topic instance.

        Returns:
            field.Field
        """
        return cls(topic.ID, topic.fov, topic.ra, topic.dec, topic.gl, topic.gb, topic.el, topic.eb)

    @property
    def fov_rads(self):
        """Field-of-view in radians.
        """
        return math.radians(self.fov)

    @property
    def ra_rads(self):
        """Right ascension in radians.
        """
        return math.radians(self.ra)

    @property
    def dec_rads(self):
        """Declination in radians.
        """
        return math.radians(self.dec)

    @property
    def gl_rads(self):
        """Galactic latitude in radians.
        """
        return math.radians(self.gl)

    @property
    def gb_rads(self):
        """Galactic longitude in radians.
        """
        return math.radians(self.gb)

    @property
    def el_rads(self):
        """Ecliptic latitude in radians.
        """
        return math.radians(self.el)

    @property
    def eb_rads(self):
        """Ecliptic longitude in radians.
        """
        return math.radians(self.eb)