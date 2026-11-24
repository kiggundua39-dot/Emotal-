import unittest

from agents.market_analyst import (
    calculate_ema,
    calculate_rsi,
    analyse_market
)
from agents.risk.risk_manager import RiskManager
from agents.trading_supervisor import TradingSupervisor


class TestMarketAnalyst(unittest.TestCase):

    def test_ema(self):
        result = calculate_ema(list(range(1, 22)), 9)
        self.assertGreater(result, 0)

    def test_rsi(self):
        result = calculate_rsi(list(range(1, 31)))
        self.assertGreaterEqual(result, 0)
        self.assertLessEqual(result, 100)

    def test_flat_market_returns_hold(self):
        result = analyse_market([100.0] * 30)
        self.assertEqual(result.signal, "HOLD")


class TestRiskManager(unittest.TestCase):

    def setUp(self):
        self.manager = RiskManager()

    def test_daily_loss_rejected(self):
        approved, volume, reason = self.manager.check_trade(
            equity=100,
            daily_loss=2,
            open_positions=0,
            stop_loss_points=100,
            tick_value=1,
            tick_size=0.01,
            point_size=0.01,
            volume_min=0.01,
            volume_max=10,
            volume_step=0.01
        )
        self.assertFalse(approved)

    def test_invalid_stop_loss_rejected(self):
        approved, _, _ = self.manager.check_trade(
            equity=100,
            daily_loss=0,
            open_positions=0,
            stop_loss_points=0,
            tick_value=1,
            tick_size=0.01,
            point_size=0.01,
            volume_min=0.01,
            volume_max=10,
            volume_step=0.01
        )
        self.assertFalse(approved)


class TestSupervisor(unittest.TestCase):

    def test_execution_remains_disabled(self):
        supervisor = TradingSupervisor()
        self.assertFalse(supervisor.execution_enabled)


if __name__ == "__main__":
    unittest.main()
  
