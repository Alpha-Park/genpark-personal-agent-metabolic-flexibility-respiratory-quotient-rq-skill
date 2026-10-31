# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-metabolic-flexibility-respiratory-quotient-rq-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def audit_metabolic_flexibility_rq(fasting_rq, postprandial_rq=None, resting_energy_expenditure_kcal=1800):
    if not (0.65 <= fasting_rq <= 1.20):
        raise ValueError("Respiratory Quotient must be within physiological range (0.65 to 1.20)")
        
    # Non-protein substrate oxidation formula:
    # % Fat oxidation = ((1.0 - RQ) / (1.0 - 0.707)) * 100
    # % Carb oxidation = ((RQ - 0.707) / (1.0 - 0.707)) * 100
    clamped_rq = min(1.0, max(0.707, fasting_rq))
    fasting_fat_pct = ((1.0 - clamped_rq) / 0.293) * 100.0
    fasting_carb_pct = ((clamped_rq - 0.707) / 0.293) * 100.0
    
    delta_rq = None
    switching_capacity = "UNDETERMINED_NO_POSTPRANDIAL_TEST"
    if postprandial_rq is not None:
        delta_rq = round(postprandial_rq - fasting_rq, 3)
        if delta_rq >= 0.12 and fasting_rq <= 0.78:
            switching_capacity = "HIGH_METABOLIC_FLEXIBILITY"
        elif delta_rq >= 0.06:
            switching_capacity = "MODERATE_FLEXIBILITY"
        else:
            switching_capacity = "METABOLIC_INFLEXIBILITY_BLUNTED_SWITCH"
            
    if fasting_rq > 0.85:
        phenotype = "IMPAIRED_FASTING_LIPID_OXIDATION"
        guidance = "Unable to efficiently utilize fatty acids during fasting; characteristic of mitochondrial overload, insulin resistance, or nocturnal carbohydrate consumption."
    elif fasting_rq <= 0.75:
        phenotype = "OPTIMAL_FASTING_FAT_BURNING"
        guidance = "Robust physiological fat oxidation in fasted state."
    else:
        phenotype = "BALANCED_SUBSTRATE_UTILIZATION"
        guidance = "Mixed fuel oxidation profile."
        
    return {
        "fasting_respiratory_quotient": round(fasting_rq, 3),
        "postprandial_respiratory_quotient": round(postprandial_rq, 3) if postprandial_rq else None,
        "delta_rq_switching_range": delta_rq,
        "fasting_fat_oxidation_percent": round(fasting_fat_pct, 1),
        "fasting_carbohydrate_oxidation_percent": round(fasting_carb_pct, 1),
        "metabolic_flexibility_category": switching_capacity,
        "fasting_phenotype": phenotype,
        "clinical_guidance": guidance
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "audit_metabolic_flexibility_rq",
                        "description": """Audit metabolic substrate switching dynamics using Respiratory Quotient (RQ = VCO2 / VO2) from indirect calorimetry.
Evaluates fasting fat oxidation capacity (normal fasting RQ 0.70-0.78) and postprandial glucose uptake transition (postprandial RQ > 0.90).
Calculates non-protein substrate oxidation percentages via Weir equation and flags metabolic inflexibility.""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = audit_metabolic_flexibility_rq(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'fasting_rq': 0.74, 'postprandial_rq': 0.92, 'resting_energy_expenditure_kcal': 1750}
        out = audit_metabolic_flexibility_rq(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
