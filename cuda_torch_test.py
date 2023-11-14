#import cudf
#print(cudf.Series([1, 2, 3]))

import torch
import time

# Verifica si CUDA está disponible
cuda_available = torch.cuda.is_available()

# Configura el dispositivo (CPU o GPU)
device = torch.device("cuda" if cuda_available else "cpu")

# Ajusta el tamaño de los tensores para aumentar la carga de trabajo
size = 10000
x = torch.rand(size, size).to(device)
y = torch.rand(size, size).to(device)

# Realiza una operación más compleja con los tensores y mide el tiempo
start_time = time.time()
z = torch.matmul(x, y)
end_time = time.time()

# Imprime el tiempo de ejecución y el dispositivo
print(f"Tiempo de ejecución: {end_time - start_time} segundos en {device}")
print(f"Dispositivo de z: {z.device}")

# Si CUDA está disponible, también realiza la operación en la CPU para comparar
if cuda_available:
    # Ajusta el tamaño de los tensores en la CPU
    x_cpu = torch.rand(size, size).cpu()
    y_cpu = torch.rand(size, size).cpu()

    # Realiza la operación en la CPU y mide el tiempo
    start_time_cpu = time.time()
    z_cpu = torch.matmul(x_cpu, y_cpu)
    end_time_cpu = time.time()

    # Imprime el tiempo de ejecución en la CPU
    print(f"Tiempo de ejecución en CPU: {end_time_cpu - start_time_cpu} segundos")
