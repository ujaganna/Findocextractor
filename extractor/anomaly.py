def detect_anomalies(metrics: dict) -> list[dict]:
    """
    Apply financial anomaly rules to extracted metrics.
    Returns a list of dicts with keys: flag, severity, detail.
    """
    flags = []

    rev_cur = metrics.get("revenue_current")
    rev_pri = metrics.get("revenue_prior")
    if rev_cur is not None and rev_pri and rev_pri != 0:
        yoy = (rev_cur - rev_pri) / abs(rev_pri)
        if yoy < -0.20:
            flags.append({
                "flag": "Revenue Decline > 20%",
                "severity": "HIGH",
                "detail": f"Revenue dropped {yoy:.1%} YoY (${rev_cur}M vs ${rev_pri}M prior year)",
            })
        elif yoy < -0.05:
            flags.append({
                "flag": "Revenue Decline > 5%",
                "severity": "MEDIUM",
                "detail": f"Revenue declined {yoy:.1%} YoY (${rev_cur}M vs ${rev_pri}M prior year)",
            })

    debt = metrics.get("total_debt")
    equity = metrics.get("total_equity")
    if debt is not None and equity and equity > 0:
        de_ratio = debt / equity
        if de_ratio > 3.0:
            flags.append({
                "flag": "High Debt-to-Equity Ratio",
                "severity": "MEDIUM",
                "detail": f"D/E ratio is {de_ratio:.2f}x (threshold: 3.0x)",
            })

    ebitda = metrics.get("ebitda")
    if ebitda is not None and ebitda < 0:
        flags.append({
            "flag": "Negative EBITDA",
            "severity": "HIGH",
            "detail": f"EBITDA is ${ebitda}M — company is not operationally profitable",
        })

    ni_cur = metrics.get("net_income_current")
    ni_pri = metrics.get("net_income_prior")
    if ni_cur is not None and ni_pri is not None and ni_pri > 0 and ni_cur < 0:
        flags.append({
            "flag": "Swing to Net Loss",
            "severity": "HIGH",
            "detail": f"Net income flipped from ${ni_pri}M profit to ${ni_cur}M loss",
        })

    opinion = (metrics.get("audit_opinion") or "").lower()
    if opinion in ("qualified", "adverse", "going concern", "disclaimer"):
        flags.append({
            "flag": f"Audit Issue: {metrics.get('audit_opinion')}",
            "severity": "CRITICAL",
            "detail": f"Auditor ({metrics.get('auditor_name', 'unknown')}) issued a '{metrics.get('audit_opinion')}' opinion",
        })

    eps = metrics.get("eps_diluted")
    if eps is not None and eps < 0:
        flags.append({
            "flag": "Negative EPS",
            "severity": "MEDIUM",
            "detail": f"Diluted EPS is ${eps} — company is losing money per share",
        })

    return flags
