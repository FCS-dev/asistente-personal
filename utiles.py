import datetime as dt


def valida_fecha(fecha):
    if not fecha:
        return False
    try:
        _ = dt.datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        return False
    return True


def fecha_a_bd(fecha):
    if not fecha:
        return ""
    try:
        fecha_dt = dt.datetime.strptime(fecha, "%d/%m/%Y")
        fecha_bd = fecha_dt.strftime("%Y-%m-%d")  # formato para BD
    except ValueError:
        return ""
    return fecha_bd


def bd_a_fecha(fecha):
    if not fecha:
        return ""
    try:
        fecha_dt = dt.datetime.strptime(fecha, "%Y-%m-%d")  # formato BD
        return fecha_dt.strftime("%d/%m/%Y")  # formato app
    except ValueError:
        return ""
