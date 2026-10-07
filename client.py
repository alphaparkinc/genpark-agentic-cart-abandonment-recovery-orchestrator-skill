"""
Agentic Cart Abandonment Recovery Orchestrator (Zero External Dependencies)
Diagnoses checkout abandonment root cause, computes dynamic margin-safe incentives, and crafts win-back copy.
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional

class AgenticCartAbandonmentRecoveryOrchestrator:
    def __init__(self, max_discount_pct: float = 15.0):
        self.max_discount = max_discount_pct

    def diagnose_abandonment_friction(self, cart_session: Dict[str, Any]) -> Dict[str, Any]:
        """Diagnoses probable reason for user abandoning checkout."""
        exit_step = str(cart_session.get("exit_step", "CART")).upper()
        shipping = float(cart_session.get("shipping_cost_usd", 0.0))
        total = float(cart_session.get("cart_total_usd", 50.0))
        dwell_time = float(cart_session.get("dwell_time_seconds", 30.0))

        if exit_step == "SHIPPING" and shipping > 0.15 * total:
            friction_code = "SHIPPING_FEE_STICKER_SHOCK"
            recommended_strategy = "WAIVE_SHIPPING_FEE"
        elif exit_step == "PAYMENT":
            friction_code = "PAYMENT_METHOD_OR_TRUST_HESITATION"
            recommended_strategy = "ASSURE_BUYER_PROTECTION_AND_PAYMENT_OPTIONS"
        elif dwell_time > 180:
            friction_code = "PRODUCT_SPECIFICATION_OR_FIT_UNCERTAINTY"
            recommended_strategy = "OFFER_AI_FIT_ASSISTANT_AND_EASY_RETURNS"
        else:
            friction_code = "PRICE_SENSITIVITY_OR_WINDOW_SHOPPING"
            recommended_strategy = "MODERATE_TIME_LIMITED_DISCOUNT"

        return {
            "cart_id": cart_session.get("cart_id", "CART-DEFAULT"),
            "cart_total_usd": total,
            "friction_code": friction_code,
            "recommended_strategy": recommended_strategy
        }

    def synthesize_winback_offer(
        self,
        cart_session: Dict[str, Any],
        profit_margin_pct: float = 40.0
    ) -> Dict[str, Any]:
        """Computes margin-preserving recovery incentive voucher."""
        diag = self.diagnose_abandonment_friction(cart_session)
        strat = diag["recommended_strategy"]
        total = diag["cart_total_usd"]

        discount_pct = 0.0
        free_shipping = False

        if strat == "WAIVE_SHIPPING_FEE":
            free_shipping = True
            discount_pct = 0.0
        elif strat == "MODERATE_TIME_LIMITED_DISCOUNT":
            # Grant max 10% or half of profit margin
            discount_pct = min(self.max_discount, round(profit_margin_pct * 0.25, 1))
        elif strat == "OFFER_AI_FIT_ASSISTANT_AND_EASY_RETURNS":
            discount_pct = 5.0
            free_shipping = True
        else:
            discount_pct = 5.0

        savings_usd = round(total * (discount_pct / 100.0) + (float(cart_session.get("shipping_cost_usd", 0.0)) if free_shipping else 0.0), 2)
        voucher_code = "WINBACK-" + hashlib.md5(f"{diag['cart_id']}:{discount_pct}".encode("utf-8")).hexdigest()[:6].upper()

        return {
            "cart_id": diag["cart_id"],
            "friction_diagnosis": diag,
            "voucher_code": voucher_code,
            "discount_percentage": discount_pct,
            "free_shipping_granted": free_shipping,
            "customer_savings_usd": savings_usd,
            "voucher_validity_hours": 24
        }

    def generate_recovery_message(
        self,
        cart_session: Dict[str, Any],
        channel: str = "WHATSAPP",
        offer: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Synthesizes high-conversion recovery copy tailored for target communication channel."""
        winback = offer or self.synthesize_winback_offer(cart_session)
        customer_name = cart_session.get("customer_name", "Valued Customer")
        items = cart_session.get("items", ["Selected Products"])
        item_str = ", ".join(items[:2])
        channel_norm = channel.upper()

        if channel_norm == "WHATSAPP":
            body = (
                f"Hi {customer_name}! 👋 Your items ({item_str}) are reserved in your cart. "
                f"To help you complete your order today, we unlocked a special perk: Use code *{winback['voucher_code']}* "
                f"for {winback['discount_percentage']}% off" + (" + Free Shipping!" if winback['free_shipping_granted'] else "!") + " "
                f"Complete checkout here: https://shop.example.com/cart/{winback['cart_id']} (Expires in 24h)"
            )
        elif channel_norm == "WECHAT_WORK":
            body = (
                f"【购物车待办提醒】{customer_name}，您关注的商品（{item_str}）已为您锁定库存。\n"
                f"专享优惠码: `{winback['voucher_code']}`（抵扣 ${winback['customer_savings_usd']}）\n"
                f"有效期: 24小时内有效。点击一键恢复订单并结算。"
            )
        else: # EMAIL
            body = (
                f"Subject: Don't miss out on {item_str} - Exclusive offer inside!\n\n"
                f"Hi {customer_name},\n\nWe noticed you left something behind in your shopping cart. "
                f"As a gesture, here is your personal promo code: {winback['voucher_code']}.\n"
                f"Enjoy a discount of ${winback['customer_savings_usd']:.2f} on your purchase today.\n\n"
                f"Best regards,\nMeta Muse Autonomous Commerce Team"
            )

        return {
            "channel": channel_norm,
            "cart_id": winback["cart_id"],
            "voucher_code": winback["voucher_code"],
            "recovery_message_text": body
        }
