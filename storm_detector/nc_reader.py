import requests
from netCDF4 import Dataset
import os
from tqdm import tqdm
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs

'''
PP (Precipitación): Podría representar la cantidad de precipitación en milímetros.

T2 (Temperatura a 2 metros): La temperatura del aire a una altura de 2 metros sobre la superficie.

PSFC (Presión a nivel del suelo): La presión atmosférica al nivel del suelo.

TSLB (Temperatura del suelo): La temperatura del suelo a una cierta profundidad.

SMOIS (Contenido de humedad del suelo): La humedad del suelo, indicando cuánta agua hay en el suelo.

ACLWDNB (Albedo de las nubes): El albedo asociado con la radiación de las nubes.

ACLWUPB (Albedo hacia arriba de las nubes): Similar al albedo de las nubes, pero relacionado con la radiación reflejada hacia arriba.

ACSWDNB (Radiación solar directa de onda corta hacia abajo): La cantidad de radiación solar directa que llega a la superficie desde el sol.

HR2 (Humedad relativa a 2 metros): La humedad relativa del aire a 2 metros sobre la superficie.

dirViento10 (Dirección del viento a 10 metros): La dirección desde la cual sopla el viento a una altura de 10 metros.

magViento10 (Velocidad del viento a 10 metros): La velocidad del viento a una altura de 10 metros.
'''

# URL del archivo NetCDF en S3
url = "https://smn-ar-wrf.s3.amazonaws.com/DATA/WRF/DET/2022/01/01/00/WRFDETAR_01H_20220101_00_000.nc"
temp_file_path = "temp_file.nc"

# Descargar el archivo con barra de progreso
response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))
block_size = 1024  # 1 Kibibyte
progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)

with open(temp_file_path, 'wb') as f:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        f.write(data)

progress_bar.close()

# Abrir el archivo con xarray
ds = xr.open_dataset(temp_file_path)

# Listar las variables disponibles en el archivo
print("Variables disponibles:", ds.variables.keys())

# Seleccionar la variable que deseas visualizar (por ejemplo, 'HR2')
variable_a_visualizar = ds['HR2']

# Obtener las coordenadas de latitud y longitud
lat = ds['lat']
lon = ds['lon']

# Crear una figura y ejes usando cartopy
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})

# Crear un mapa de contorno de la variable seleccionada
contorno = ax.contourf(lon, lat, variable_a_visualizar.isel(time=0), transform=ccrs.PlateCarree(), cmap='viridis', levels=50)

# Agregar barra de color
barra_color = plt.colorbar(contorno, ax=ax, shrink=0.6, orientation='vertical', label='Unidades de la variable')

# Agregar límites de la costa
ax.coastlines()

# Agregar etiquetas y título
ax.set_xlabel('Longitud')
ax.set_ylabel('Latitud')
plt.title('Visualización de la variable HR2 en el tiempo 0')

# Mostrar el mapa
plt.savefig('mapa_variable.png')

# Cerrar el conjunto de datos xarray
ds.close()

# Eliminar el archivo temporal
os.remove(temp_file_path)
