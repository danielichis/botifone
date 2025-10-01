# ...existing code...
import base64
import datetime
from zoneinfo import ZoneInfo

s = 'MjAyNS0wOS0yNyAwMToyNjo0Mg'
print(base64.b64decode(s + '==').decode())  # -> '2025-09-27 01:26:42'

unix = 1759012002
print(datetime.datetime.utcfromtimestamp(unix))   # UTC
print(datetime.datetime.fromtimestamp(unix))      # hora local del sistema

# Mostrar en hora de Lima (America/Lima, UTC-5)
lima = ZoneInfo("America/Lima")
print(datetime.datetime.fromtimestamp(unix, tz=lima))  # hora en Lima

# Si la cadena decodificada es UTC y quieres convertirla a Lima:
dt = datetime.datetime.strptime(base64.b64decode(s + '==').decode(), "%Y-%m-%d %H:%M:%S")
dt_utc = dt.replace(tzinfo=datetime.timezone.utc)
print(dt_utc.astimezone(lima))  # misma marca en hora de Lima
# ...existing code...