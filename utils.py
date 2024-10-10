def decimal_a_gms(grados_decimales):
    grados = int(grados_decimales)
    minutos_decimales = abs(grados_decimales - grados) * 60
    minutos = int(minutos_decimales)
    segundos = (minutos_decimales - minutos) * 60
    return f"{grados}° {minutos}' {segundos:.2f}\""