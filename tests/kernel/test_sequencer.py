import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from lsst.sims.ocs.kernel.sequencer import Sequencer
from lsst.sims.ocs.kernel.time_handler import TimeHandler
from lsst.sims.ocs.sal.sal_manager import SalManager

class SequencerTest(unittest.TestCase):

    def setUp(self):
        self.seq = Sequencer()

    def initialize_sequencer(self):
        self.sal = SalManager()
        self.sal.initialize()
        self.seq.initialize(self.sal)

    def create_objects(self):
        target = self.sal.set_subscribe_topic("targetTest")
        # Set some meaningful information
        target.targetId = 10
        target.fieldId = 300
        target.filter = "i"
        target.ra = 0.4244
        target.dec = -0.5314
        target.num_exposures = 2

        # Make it so initial timestamp is 0
        time_handler = TimeHandler("1970-01-01")

        return target, time_handler

    def test_basic_information_after_creation(self):
        self.assertEqual(self.seq.observations_made, 0)
        self.assertEqual(self.seq.targets_received, 0)
        self.assertIsNone(self.seq.observation)
        self.assertIsNotNone(self.seq.observatory_model)
        self.assertIsNone(self.seq.observatory_state)

    @mock.patch("lsst.sims.ocs.observatory.main_observatory.MainObservatory.configure")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_initialization(self, mock_sal_telemetry_pub, mock_main_observatory_configure):
        self.initialize_sequencer()
        self.assertIsNotNone(self.seq.observation)
        self.assertEqual(self.seq.observation.observationId, 0)
        self.assertEquals(mock_sal_telemetry_pub.call_count, 2)
        self.assertTrue(mock_main_observatory_configure.called)
        self.assertIsNotNone(self.seq.observatory_state)

    @mock.patch("logging.Logger.info")
    def test_finalization(self, mock_logger_info):
        self.seq.finalize()
        self.assertEqual(mock_logger_info.call_count, 2)

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_observe_target(self, mock_sal_telemetry_pub, mock_sal_telemetry_sub, mock_logger_log):
        self.initialize_sequencer()
        target, time_handler = self.create_objects()

        observation, slew, exposures = self.seq.observe_target(target, time_handler)

        self.assertEqual(observation.observation_start_time, time_handler.initial_timestamp + 140.0)
        self.assertEqual(observation.targetId, target.targetId)
        self.assertEqual(self.seq.targets_received, 1)
        self.assertEqual(self.seq.observations_made, 1)
        self.assertEqual(len(slew), 5)
        self.assertEqual(len(exposures), 2)

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_end_of_night(self, mock_sal_telemetry_pub, mock_sal_telemetry_sub, mock_logger_log):
        self.initialize_sequencer()
        target, time_handler = self.create_objects()

        # Don't care about outputs
        self.seq.observe_target(target, time_handler)
        self.seq.end_of_night()

        obs_current_state = self.seq.observatory_model.currentState

        self.assertEqual(obs_current_state.telalt, 86.5)
        self.assertEqual(obs_current_state.telaz, 0.0)
        self.assertEqual(obs_current_state.domalt, 90.0)
        self.assertEqual(obs_current_state.domaz, 0.0)
        self.assertEqual(obs_current_state.filter, 'r')

    @mock.patch("logging.Logger.log")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetrySub")
    @mock.patch("SALPY_scheduler.SAL_scheduler.salTelemetryPub")
    def test_get_observatory_state_after_initialization(self, mock_sal_telemetry_pub,
                                                        mock_sal_telemetry_sub, mock_logger_log):
        self.initialize_sequencer()
        _, time_handler = self.create_objects()
        observatory_state = self.seq.get_observatory_state(time_handler.current_timestamp)

        # Observatory state should be in the park position
        self.assertEqual(observatory_state.timestamp, 0.0)
        self.assertEqual(observatory_state.pointing_ra, 29.34160493523685)
        self.assertEqual(observatory_state.pointing_dec, -26.7444)
        self.assertEqual(observatory_state.pointing_altitude, 86.5)
        self.assertEqual(observatory_state.pointing_azimuth, 0.0)
        self.assertEqual(observatory_state.pointing_pa, -180.0)
        self.assertEqual(observatory_state.pointing_rot, 0.0)
        self.assertFalse(observatory_state.tracking)
        self.assertEqual(observatory_state.telescope_altitude, 86.5)
        self.assertEqual(observatory_state.telescope_azimuth, 0.0)
        self.assertEqual(observatory_state.dome_altitude, 90.0)
        self.assertEqual(observatory_state.dome_azimuth, 0.0)
        self.assertEqual(observatory_state.filter_position, 'r')
        self.assertEqual(observatory_state.filter_mounted, 'g,r,i,z,y')
        self.assertEqual(observatory_state.filter_unmounted, 'u')