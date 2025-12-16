# transformer_engine.py
def design_transformer(kva: float, v1: float, v2: float, f: float = 50.0):
    """Basic transformer design for oil-filled distribution units"""
    # Core design (volts per turn)
    Et = 0.45 * (kva ** 0.25)  # Empirical constant for 50 Hz
    B = 1.6  # Flux density in Tesla (CRGO)
    A_core = (Et * 1e6) / (4.44 * f * B)  # Core area in mm²
    D_core = (4 * A_core / 3.1416) ** 0.5  # Equivalent core diameter

    # Currents
    I1 = (kva * 1000) / (1.732 * v1)
    I2 = (kva * 1000) / (1.732 * v2)

    # Conductor area (J = 2.8 A/mm²)
    A_cu_hv = I1 / 2.8
    A_cu_lv = I2 / 2.8

    # Turns
    N1 = v1 / Et
    N2 = v2 / Et

    # Weights (approx)
    core_weight_kg = kva * 12
    copper_weight_kg = kva * 8

    # Losses
    no_load_loss = 1.2 * core_weight_kg  # W
    load_loss = 0.8 * kva  # W (approx)

    # Impedance (%)
    impedance = 4.5 if kva <= 500 else 5.0

    return {
        "kva": kva,
        "v1": v1,
        "v2": v2,
        "core_diameter_mm": round(D_core, 1),
        "hv_turns": round(N1),
        "lv_turns": round(N2),
        "core_weight_kg": round(core_weight_kg),
        "copper_weight_kg": round(copper_weight_kg),
        "no_load_loss_w": round(no_load_loss),
        "load_loss_w": round(load_loss),
        "impedance_percent": impedance
    }