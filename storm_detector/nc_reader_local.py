import netCDF4 as nc
from netCDF4 import Dataset
import xarray as xr
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import s3fs
from tqdm import tqdm

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

# Ruta  LOCAL al archivo NetCDF
ruta_archivo = "/home/juampamanzano/ml-ideas/data/WRFDETAR_01H_20230101_00_000.nc"

# Abrir el archivo LOCAL NetCDF en modo de solo lectura
archivo_netcdf = nc.Dataset(ruta_archivo, "r")

# Configurar el sistema de archivos S3
s3 = s3fs.S3FileSystem(anon=True) 

# Listar las variables disponibles en el archivo
print("Variables disponibles:", archivo_netcdf.variables.keys())

# Leer una variable específica
variable = archivo_netcdf.variables["time"]

# Obtener los datos como un array de NumPy
datos = variable[:]
print("Datos:", datos)

# Cerrar el archivo NetCDF
archivo_netcdf.close()


# Cargar el conjunto de datos NetCDF usando xarray
ds = xr.open_dataset(ruta_archivo)
print(ds['time'])

# Seleccionar la variable que deseas visualizar (por ejemplo, 'PP')
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
plt.title('Visualización de la variable PP en el tiempo 0')

# Mostrar el mapa
plt.savefig('mapa_variable_local.png')
