import random
# import yaml
import os
import time
from datetime import datetime, timedelta

class CreadorDeLogs:

    def __init__(self, limite_menor=None , limite_mayor=None, opciones_dispositivo=None, opciones_estado_dispositivo=None, opciones_mision=None, intervalo=None, ciclos=None):
        self.limite_menor = limite_menor or 1
        self.limite_mayor = limite_mayor or 100
        self.intervalo = intervalo or 20
        self.ciclos = ciclos or 3
        self.opciones_dispositivo = opciones_dispositivo or ["Satelites", "Naves", "Trajes", "Vehiculos_espaciales"]
        self.opciones_estado_dispositivo = opciones_estado_dispositivo or ["excellent", "good", "warning", "faulty","killed","unknown"]
        self.opciones_mision = opciones_mision or ["OrbitOne", "ColonyMoon", "VacMars", "GalaxyTwo","UNKN"]

    def crear_numero(self):
        numero_aleatorio = random.randint(self.limite_menor, self.limite_mayor)
        return numero_aleatorio

    def generar_fecha(self):
        fecha = datetime.today()
        fecha_actual=fecha + timedelta(hours=-5)
        fecha_formateada = fecha_actual.strftime("%d%m%Y%H%M%S")
        return fecha_formateada

    def crear_carpeta(self, carpeta_de_salida = "devices"):
        os.makedirs(carpeta_de_salida, exist_ok=True)

    def nombre_archivo(self, mission,i):
        if mission == 'OrbitOne':
            return f"APLORBONE-0000{i}.log"
        if mission == 'ColonyMoon':
            return f"APLCLNM-0000{i}.log"
        if mission == 'VacMars':
            return f"APLTMRS-0000{i}.log"
        if mission == 'GalaxyTwo':
            return f"APLGALXONE-0000{i}.log"
        if mission == 'UNKN':
            return f"APLUNKN-0000{i}.log"

    def crear_mision(self):
        self.inf={}
        date=self.generar_fecha()
        self.inf["date"]=date
        mision_apolo_11 = random.choice(self.opciones_mision)
        self.inf["mission"]=mision_apolo_11
        if mision_apolo_11 == "UNKN":
          dispositivo_apolo_11="unknown"
          estado_dispositivo_apolo_11="unknown"
        else:
          dispositivo_apolo_11 = random.choice(self.opciones_dispositivo)
          estado_dispositivo_apolo_11 = random.choice(self.opciones_estado_dispositivo)
        self.inf["device_type"]=dispositivo_apolo_11
        self.inf["device_status"]=estado_dispositivo_apolo_11
        if mision_apolo_11 != "UNKN":
          hash=self.generar_hash(self.inf)
          self.inf["hash"]=hash
        return self.inf

    def crear_archivo(self, carpeta_de_salida="devices"):
        self.numero_aleatorio = self.crear_numero()
        self.crear_carpeta(carpeta_de_salida)
        for i in range(1, self.numero_aleatorio + 1):
            contenido_del_archivo = self.crear_mision()
            ruta_archivo = f"{carpeta_de_salida}/{self.nombre_archivo(contenido_del_archivo['mission'],i)}"
            while os.path.exists(ruta_archivo):
              i+=1
              e=1
              ruta_archivo = f"{carpeta_de_salida}/{self.nombre_archivo(contenido_del_archivo['mission'],i)}"
              nombre_archivo = f"{self.nombre_archivo(contenido_del_archivo['mission'], i)}"
            with open(ruta_archivo, "w") as archivo:
                yaml.dump(contenido_del_archivo, archivo)



    def generar_hash(self,inf):
        fecha_arc:str=inf["date"]
        mission_arc:str=inf["mission"]
        dispositivo_arc:str=inf["device_type"]
        estado_arc:str=inf["device_status"]
        contenido_hash:str=fecha_arc+mission_arc+dispositivo_arc+estado_arc
        return contenido_hash

    def ejecutar_ciclos(self):
        contador_ciclos = 0
        try:
            while contador_ciclos < self.ciclos:
                self.crear_archivo()
                contador_ciclos += 1
                print(f"Ciclo {contador_ciclos} completados. {self.numero_aleatorio} archivos generados")
                time.sleep(self.intervalo)
        except KeyboardInterrupt:
            print("Interrupción manual del usuario. Finalizando la ejecución.")

def eliminar_archivos_en_carpeta(ruta_carpeta):
    try:
        archivos = [archivo for archivo in os.listdir(ruta_carpeta) if os.path.isfile(os.path.join(ruta_carpeta, archivo))]
        for archivo in archivos:
            ruta_completa = os.path.join(ruta_carpeta, archivo)
            os.remove(ruta_completa)
        print(f'Todos los archivos en "{ruta_carpeta}" han sido eliminados.')
    except Exception as e:
        print(f'Ocurrió un error al eliminar archivos: {e}')

def contar_archivos(carpeta_de_salida="devices"):
    try:
        archivos = os.listdir(carpeta_de_salida)
        num_archivos = len(archivos)
        print(f"Número de archivos en la carpeta '{carpeta_de_salida}': {num_archivos}")

    except Exception as e:
        print(f"Error al contar archivos: {e}")
        return 0

ruta_carpeta_limpiar = 'ruta_carpeta'
eliminar_archivos_en_carpeta("devices")
creador_de_logs=CreadorDeLogs(limite_menor=1, limite_mayor=100, intervalo=5, ciclos=5)
creador_de_logs.ejecutar_ciclos()
contar_archivos()
