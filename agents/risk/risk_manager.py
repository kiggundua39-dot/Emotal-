from dataclasses import dataclass


@dataclass
class RiskConfig:
    risk_percent: float = 0.5
    daily_loss_limit_percent: float = 2.0
    max_positions: int = 1
    max_volume: float = 0.10


class RiskManager:

    def __init__(self, config=None):
        self.config = config or RiskConfig()

    def check_trade(
        self,
        equity,
        daily_loss,
        open_positions,
        stop_loss_points,
        tick_value,
        tick_size,
        point_size,
        volume_min,
        volume_max,
        volume_step
    ):
        if equity <= 0:
            return False, 0.0, "Invalid account equity"

        if stop_loss_points <= 0:
            return False, 0.0, "Invalid stop loss"

        if tick_value <= 0 or tick_size <= 0:
            return False, 0.0, "Invalid symbol tick data"

        if point_size <= 0 or volume_step <= 0:
            return False, 0.0, "Invalid broker settings"

        if volume_min <= 0 or volume_max < volume_min:
            return False, 0.0, "Invalid volume limits"

        if self.config.risk_percent <= 0:
            return False, 0.0, "Invalid risk percentage"

        if daily_loss < 0:
            return False, 0.0, "Invalid daily loss value"

        if daily_loss >= equity * (
            self.config.daily_loss_limit_percent / 100
        ):
            return False, 0.0, "Daily loss limit reached"

        if open_positions >= self.config.max_positions:
            return False, 0.0, "Maximum positions reached"

        risk_money = equity * (
            self.config.risk_percent / 100
        )

        stop_distance = stop_loss_points * point_size

        loss_per_lot = (
            stop_distance / tick_size
        ) * tick_value

        if loss_per_lot <= 0:
            return False, 0.0, "Invalid loss calculation"

        raw_volume = risk_money / loss_per_lot

        volume_cap = min(
            volume_max,
            self.config.max_volume
        )

        volume = (
            int(raw_volume / volume_step) * volume_step
        )

        if volume < volume_min:
            return False, 0.0, (
                "Minimum broker volume exceeds risk budget"
            )

        volume = min(volume, volume_cap)

        return True, round(volume, 8), "Risk checks passed"


if __name__ == "__main__":
    manager = RiskManager()

    print("Risk Manager initialized")
    print("Live trading: DISABLED")
  
