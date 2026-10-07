"""Example usage for AgenticCartAbandonmentRecoveryOrchestrator."""
import sys
import json
from client import AgenticCartAbandonmentRecoveryOrchestrator

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Agentic Commerce Cart Abandonment Win-Back Orchestrator Demo ===")
    orchestrator = AgenticCartAbandonmentRecoveryOrchestrator()

    abandoned_session = {
        "cart_id": "CART-MUSE-89410",
        "customer_name": "Sarah Connor",
        "cart_total_usd": 150.00,
        "shipping_cost_usd": 30.00,
        "exit_step": "SHIPPING",
        "dwell_time_seconds": 75.0,
        "items": ["Smart Noise-Canceling Earbuds", "Protective Leather Case"]
    }

    # 1. Diagnose abandonment friction cause
    print("\n--- 1. Diagnosing Drop-off Friction ---")
    diagnosis = orchestrator.diagnose_abandonment_friction(abandoned_session)
    print(f"Friction Code: {diagnosis['friction_code']}")
    print(f"Recommended Strategy: {diagnosis['recommended_strategy']}")

    # 2. Synthesize profit-margin preserving win-back voucher
    print("\n--- 2. Synthesizing Dynamic Incentive Voucher ---")
    offer = orchestrator.synthesize_winback_offer(abandoned_session, profit_margin_pct=45.0)
    print(f"Voucher Code: {offer['voucher_code']} (Discount: {offer['discount_percentage']}%, Free Shipping: {offer['free_shipping_granted']})")
    print(f"Total Customer Savings: ${offer['customer_savings_usd']:.2f}")

    # 3. Generate WhatsApp and WeChat Work recovery message copy
    print("\n--- 3. Generating Channel-Native Outreach Copy ---")
    wa_msg = orchestrator.generate_recovery_message(abandoned_session, channel="WHATSAPP", offer=offer)
    print(f"[WhatsApp]:\n{wa_msg['recovery_message_text']}")

if __name__ == "__main__":
    main()
