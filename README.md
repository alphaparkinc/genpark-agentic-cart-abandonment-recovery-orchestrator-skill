# genpark-agentic-cart-abandonment-recovery-orchestrator-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Skill-blue.svg)](https://genpark.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/dependencies-0%20(Pure%20Stdlib)-brightgreen.svg)](requirements.txt)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-purple.svg)](mcp_server.py)

Autonomous Agentic Cart Abandonment Recovery Orchestrator. Monitors abandoned checkout sessions in Meta Muse, Shopify, and WhatsApp Commerce, diagnoses friction causes (shipping cost shock, size doubt, payment hesitation), crafts margin-preserving dynamic incentive vouchers, and synthesizes multi-channel win-back messages.

---

## 🌟 Key Features

- **100% Zero External Dependencies**: Runs entirely on the Python 3.9+ standard library.
- **Model Context Protocol (MCP) Standard**: Native support for JSON-RPC 2.0 `initialize`, `tools/list`, and `tools/call`.
- **Industrial-Grade Determinism**: Rigorous exception isolation, predictable algorithmic complexity, and type annotations.
- **Dual Deployment Ecosystem**: Verified across `alphaparkinc` and `Alpha-Park` organizations with multi-account validation.

---

## 🚀 Quick Start

### 1. Direct Python SDK Usage

```python
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

```

### 2. Run as Model Context Protocol (MCP) Server

Start standard JSON-RPC 2.0 server over `stdio`:

```bash
python mcp_server.py
```

Execute embedded test harness:

```bash
python mcp_server.py --test
```

---

## 🛠️ MCP Tool Specification

Inspect [`skill.json`](skill.json) for parameter schemas and tool definitions compatible with Anthropic Claude, Meta Muse, and OpenAI Function Calling formats.

---

## 📜 License

Licensed under the [MIT License](LICENSE). Copyright © 2026 GenPark AI.
