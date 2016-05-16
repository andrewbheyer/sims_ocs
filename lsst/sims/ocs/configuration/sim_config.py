import os

import lsst.pex.config as pexConfig

from lsst.sims.ocs.configuration import load_config, Observatory, ObservingSite, ScienceProposals, Survey

__all__ = ["SimulationConfig"]

class SimulationConfig(pexConfig.Config):
    """Configuration for the survey simulation.

    This class gathers all of the configuration objects into one place.
    """
    survey = pexConfig.ConfigField("The LSST survey configuration.", Survey)
    science = pexConfig.ConfigField("The science proposal configuration.", ScienceProposals)
    observing_site = pexConfig.ConfigField("The observing site configuration.", ObservingSite)
    observatory = pexConfig.ConfigField("The LSST observatory configuration.", Observatory)

    def setDefaults(self):
        """Set defaults for the survey simulation.
        """
        pass

    def load(self, ifiles):
        """Load and apply configuration override files.

        This function loads the specified configuration files and applies them to the configuration
        objects. If input is a directory, it is assumed that all files in that directory are override
        files.

        Parameters
        ----------
        ifiles : list[str]
            A list of files or directories containing configuration overrides.
        """
        if ifiles is None:
            return
        config_files = []
        for ifile in ifiles:
            if os.path.isdir(ifile):
                dfiles = os.listdir(ifile)
                for dfile in dfiles:
                    full_dfile = os.path.join(ifile, dfile)
                    if os.path.isfile(full_dfile):
                        config_files.append(full_dfile)
            else:
                config_files.append(ifile)

        if len(config_files):
            load_config(self.survey, config_files)
            self.science.load(config_files)
            load_config(self.observing_site, config_files)
            self.observatory.load(config_files)

    def load_proposals(self):
        """Tell the science proposals to load their configuration.
        """
        self.science.load_proposals()

    def save(self, save_dir=''):
        """Save the configuration objects to separate files.

        Parameters
        ----------
        save_dir : str
            The directory in which to save the configuration files.
        """
        self.survey.save(os.path.join(save_dir, "survey.py"))
        self.science.save_as(save_dir)
        self.observing_site.save(os.path.join(save_dir, "observing_site.py"))
        self.observatory.save_as(save_dir)