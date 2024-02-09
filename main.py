from fastapi import FastAPI
import psutil
import subprocess
import docker

app = FastAPI()

def get_ram_usage():
    total_memory = round(psutil.virtual_memory().total / (1024.0 ** 3), 2)
    used_memory = round(psutil.virtual_memory().used / (1024.0 ** 3), 2)
    return f'{used_memory} of {total_memory} Gb'

def get_cpu_usage():
    percent: float = round(psutil.cpu_percent(interval=1) , 2) 
    return f'{percent} %'

def get_network_usage():
    kb_sent: float = round(psutil.net_io_counters().bytes_sent / 1024, 2) 
    kb_recv: float = round(psutil.net_io_counters().bytes_recv / 1024, 2) 
    return kb_sent, kb_recv

def get_ip_address():
    try:
        ip = subprocess.check_output(['hostname', '-I']).decode().strip()
        return ip
    except subprocess.CalledProcessError:
        return "No se pudo obtener la dirección IP"

def get_docker_containers():
    try:
        client = docker.from_env()
        containers = client.containers.list()
        container_info = []
        for container in containers:
            container_info.append({
                "Nombre": container.name,
                "ID": container.short_id,
                "Estado": container.status
            })
        return container_info
    except:
        return { }
    
@app.get('/info')
def get_server_info() -> dict:
    info = {
        "uso_ram": get_ram_usage(),
        "uso_cpu": get_cpu_usage(),
        "uso_red": {
            "kb_enviados": get_network_usage()[0],
            "kb_recibidos": get_network_usage()[1]
        },
        "ip": get_ip_address(),
        "estado_docker_contenedores": get_docker_containers()
    }
    return info

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
