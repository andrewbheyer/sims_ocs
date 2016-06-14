import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration.proposal import AreaDistribution, BandFilter, Selection
from lsst.sims.ocs.configuration.proposal import area_dist_prop_reg, SELECTION_LIMIT_TYPES

__all__ = ["GalacticPlane"]

@pexConfig.registerConfig("GalacticPlane", area_dist_prop_reg, AreaDistribution)
class GalacticPlane(AreaDistribution):
    """This class sets the parameters for specifying the Galactic Plane proposal.
    """

    def setDefaults(self):
        """Setup all the proposal information.
        """
        self.name = "GalacticPlane"

        # -------------------------
        # Sky Region specifications
        # -------------------------

        # Galactic Plane
        gal_plane = Selection()
        gal_plane.limit_type = SELECTION_LIMIT_TYPES[6]
        gal_plane.minimum_limit = 0.0
        gal_plane.maximum_limit = 10.0
        gal_plane.bounds_limit = 90.0

        self.sky_region.selections = {0: gal_plane}

        # -----------------------------
        # Sky Exclusion specifications
        # -----------------------------

        self.sky_exclusion.dec_window = 90.0

        # ---------------------------------
        # Sky Nightly Bounds specifications
        # ---------------------------------

        self.sky_nightly_bounds.twilight_boundary = -12.0
        self.sky_nightly_bounds.delta_lst = 60.0

        # ------------------------------
        # Sky Constraints specifications
        # ------------------------------

        self.sky_constraints.max_airmass = 2.5

        # ----------------------
        # Scheduling information
        # ----------------------

        self.scheduling.max_num_targets = 100
        self.scheduling.accept_serendipity = False
        self.scheduling.accept_consecutive_visits = False

        # --------------------------
        # Band Filter specifications
        # --------------------------

        u_filter = BandFilter()
        u_filter.name = 'u'
        u_filter.num_visits = 30
        u_filter.bright_limit = 20.8
        u_filter.dark_limit = 30.0
        u_filter.max_seeing = 3.0
        u_filter.exposures = [15.0, 15.0]

        g_filter = BandFilter()
        g_filter.name = 'g'
        g_filter.num_visits = 30
        g_filter.bright_limit = 20.8
        g_filter.dark_limit = 30.0
        g_filter.max_seeing = 3.0
        g_filter.exposures = [15.0, 15.0]

        r_filter = BandFilter()
        r_filter.name = 'r'
        r_filter.num_visits = 30
        r_filter.bright_limit = 20.0
        r_filter.dark_limit = 30.0
        r_filter.max_seeing = 2.0
        r_filter.exposures = [15.0, 15.0]

        i_filter = BandFilter()
        i_filter.name = 'i'
        i_filter.num_visits = 30
        i_filter.bright_limit = 19.5
        i_filter.dark_limit = 30.0
        i_filter.max_seeing = 2.0
        i_filter.exposures = [15.0, 15.0]

        z_filter = BandFilter()
        z_filter.name = 'z'
        z_filter.num_visits = 30
        z_filter.bright_limit = 17.0
        z_filter.dark_limit = 21.4
        z_filter.max_seeing = 2.0
        z_filter.exposures = [15.0, 15.0]

        y_filter = BandFilter()
        y_filter.name = 'y'
        y_filter.num_visits = 30
        y_filter.bright_limit = 16.0
        y_filter.dark_limit = 21.4
        y_filter.max_seeing = 2.0
        y_filter.exposures = [15.0, 15.0]

        self.filters = {u_filter.name: u_filter,
                        g_filter.name: g_filter,
                        r_filter.name: r_filter,
                        i_filter.name: i_filter,
                        z_filter.name: z_filter,
                        y_filter.name: y_filter}
