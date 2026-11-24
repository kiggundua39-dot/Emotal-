from agents.market_analyst import analyse_market
from agents.risk.risk_manager import RiskManager


class TradingSupervisor:

    def __init__(self):
        self.analyst_ready = True
        self.risk_manager = RiskManager()
        self.execution_enabled = False

    def evaluate(
        self,
        closes,
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
        # Stage 1: Analyse the market
        analysis = analyse_market(closes)

        result = {
            "signal": analysis.signal,
            "reason": analysis.reason,
            "approved": False,
            "volume": 0.0,
            "execution_enabled": False
        }

        # Stage 2: Reject HOLD signals
        if analysis.signal == "HOLD":
            result["decision"] = "REJECTED"
            result["risk_reason"] = "No trading signal"
            return result

        # Stage 3: Check capital protection
        approved, volume, reason = (
            self.risk_manager.check_trade(
                equity=equity,
                daily_loss=daily_loss,
                open_positions=open_positions,
                stop_loss_points=stop_loss_points,
                tick_value=tick_value,
                tick_size=tick_size,
                point_size=point_size,
                volume_min=volume_min,
                volume_max=volume_max,
                volume_step=volume_step
            )
        )

        result["approved"] = approved
        result["volume"] = volume
        result["risk_reason"] = reason

        if approved:
            result["decision"] = "APPROVED_FOR_TESTING"
        else:
            result["decision"] = "REJECTED"

        # No orders can be sent by this supervisor
        result["execution_enabled"] = False

        return result


if __name__ == "__main__":
    supervisor = TradingSupervisor()

    print("AI Trading Supervisor initialized")
    print("Market Analyst: READY")
    print("Risk Manager: READY")
    print("Trade execution: DISABLED")
  
