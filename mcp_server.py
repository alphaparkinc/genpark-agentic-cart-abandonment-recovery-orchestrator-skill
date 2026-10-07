"""MCP Server for Agentic Cart Abandonment Recovery Orchestrator."""
import sys
import json
import time
from client import AgenticCartAbandonmentRecoveryOrchestrator

orchestrator = AgenticCartAbandonmentRecoveryOrchestrator()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "orchestrate_cart_recovery":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "synthesize_winback_offer")
    cart = args.get("cart_session", {})
    channel = args.get("channel", "WHATSAPP")

    if action == "diagnose_abandonment_friction":
        return orchestrator.diagnose_abandonment_friction(cart)
    elif action == "synthesize_winback_offer":
        return orchestrator.synthesize_winback_offer(cart)
    elif action == "generate_recovery_message":
        return orchestrator.generate_recovery_message(cart, channel=channel)
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        cart = {
            "cart_id": "CART-TEST-12",
            "cart_total_usd": 120.0,
            "shipping_cost_usd": 25.0,
            "exit_step": "SHIPPING",
            "items": ["Ergonomic Mechanical Keyboard"]
        }
        diag = orchestrator.diagnose_abandonment_friction(cart)
        assert diag["friction_code"] == "SHIPPING_FEE_STICKER_SHOCK"
        wb = orchestrator.synthesize_winback_offer(cart)
        assert wb["free_shipping_granted"] is True
        msg = orchestrator.generate_recovery_message(cart, "WHATSAPP", wb)
        assert wb["voucher_code"] in msg["recovery_message_text"]
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "AgenticCartAbandonmentRecoveryOrchestrator", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "orchestrate_cart_recovery",
                            "description": "Diagnose cart abandonment friction, synthesize dynamic win-back voucher incentives within profit margin bounds, and generate recovery message drafts.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["diagnose_abandonment_friction", "synthesize_winback_offer", "generate_recovery_message"]},
                                    "cart_session": {"type": "object"},
                                    "channel": {"type": "string"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
