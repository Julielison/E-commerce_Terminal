import threading
import time

# Cria um semáforo com um contador inicial de 2 (duas threads podem acessar simultaneamente)
sem = threading.Semaphore(1)

def tarefa(numero):
    print(f"Thread {numero} esperando para acessar o recurso.")
    
    # Adquire o semáforo, decrementando o contador
    with sem:
        print(f"Thread {numero} acessou o recurso.")
        time.sleep(2)  # Simula uma tarefa que leva tempo
        print(f"Thread {numero} liberou o recurso.")

# Cria múltiplas threads
threads = []
for i in range(5):
    t = threading.Thread(target=tarefa, args=(i,))
    threads.append(t)
    t.start()

# Aguarda todas as threads terminarem
for t in threads:
    t.join()

print("Todas as threads terminaram.")
