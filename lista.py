import random
from datetime import datetime, timedelta

# Listas fornecidas
viloes = [
    'Coringa', 'Pinguim', 'Arlequina', 'Charada', 'Espantalho', 
    'Duas-Caras', 'Bane', 'Hera Venenosa', 'Senhor Frio', 'Chapeleiro Louco'
]

crimes = [
    'Assassinato', 'Roubo', 'Ameaça', 'Sequestro', 'Explosão',
    'Extorsão', 'Invasão', 'Sabotagem', 'Envenenamento', 'Assalto',
    'Atentado', 'Terrorismo', 'Suborno', 'Massacre', 'Fraude',
    'Corrupção', 'Agressão', 'Perturbação', 'Tráfico', 
    'Tentativa de Homicídio', 'Rebelião'
]

vizinhanças = [
    'Arkham', 'Gotham Heights', 'The Narrows', 'Diamond District',
    'Otisburg', 'Gotham Central', 'Burnley', 'Old Gotham', 'Bristol'
]

# Função para gerar data aleatória entre 2020-01-01 e 2025-09-01
def gerar_data_aleatoria():
    inicio = datetime(2020, 1, 1)
    fim = datetime(2025, 9, 1)
    delta = fim - inicio
    dias_aleatorios = random.randint(0, delta.days)
    return (inicio + timedelta(days=dias_aleatorios)).strftime('%Y-%m-%d')

# Gerar 150 inserts
novas_linhas = []
for _ in range(150):
    vilao = random.choice(viloes)
    crime = random.choice(crimes)
    bairro = random.choice(vizinhanças)
    data = gerar_data_aleatoria()
    novas_linhas.append(f"('{vilao}', '{crime}', '{bairro}', '{data}')")

# Montar o SQL final
comando_sql = "INSERT INTO crime_stats (villain, crimes, neighborhood, date) VALUES \n"
comando_sql += ",\n".join(novas_linhas) + ";"

# Salvar ou imprimir
print(comando_sql)
