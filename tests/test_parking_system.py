import unittest

from parking_system import MedianFilter, ParkingState, ParkingController, simulate


class ParkingSystemTests(unittest.TestCase):
    def test_filter_rejects_one_ultrasonic_spike(self):
        states = simulate([20, 20, 60, 20, 20], sample_count=5)
        self.assertEqual(states[-1], ParkingState.EMPTY)

    def test_car_needs_two_confirmations_to_become_occupied(self):
        states = simulate([20, 6, 6], sample_count=1)
        self.assertEqual(states[1], ParkingState.EMPTY)
        self.assertEqual(states[-1], ParkingState.OCCUPIED)

    def test_hysteresis_prevents_boundary_flapping(self):
        states = simulate([6, 6, 10, 10, 11, 13, 13], sample_count=1)
        self.assertEqual(states[3], ParkingState.OCCUPIED)
        self.assertEqual(states[-1], ParkingState.EMPTY)

    def test_invalid_filter_size_is_rejected(self):
        with self.assertRaises(ValueError):
            MedianFilter(4)


if __name__ == "__main__":
    unittest.main()

