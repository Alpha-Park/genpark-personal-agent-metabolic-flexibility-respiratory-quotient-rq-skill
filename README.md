# genpark-personal-agent-metabolic-flexibility-respiratory-quotient-rq-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

Indirect calorimetry Respiratory Quotient (RQ / RER) fasting substrate oxidation and insulin resistance auditor.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `audit_metabolic_flexibility_rq`
- **Category**: `personal_agent`

### Method Documentation
Audit metabolic substrate switching dynamics using Respiratory Quotient (RQ = VCO2 / VO2) from indirect calorimetry.
Evaluates fasting fat oxidation capacity (normal fasting RQ 0.70-0.78) and postprandial glucose uptake transition (postprandial RQ > 0.90).
Calculates non-protein substrate oxidation percentages via Weir equation and flags metabolic inflexibility.

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "audit_metabolic_flexibility_rq",
    "arguments": {
    "fasting_rq": 0.74,
    "postprandial_rq": 0.92,
    "resting_energy_expenditure_kcal": 1750
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
