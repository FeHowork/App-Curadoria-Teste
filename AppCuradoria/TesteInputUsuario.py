from itertools import product
from datetime import datetime, timedelta

# Lista de 35 bandas de rock conhecidas
bandas = [
    "Led Zeppelin", "Pink Floyd", "The Beatles", "Queen", "Rolling Stones",
    "AC/DC", "Metallica", "Guns N' Roses", "Nirvana", "U2",
    "The Who", "Black Sabbath", "Deep Purple", "Radiohead", "Red Hot Chili Peppers",
    "Foo Fighters", "The Doors", "Aerosmith", "Iron Maiden", "Pearl Jam",
    "Rush", "Kiss", "Dire Straits", "The Clash", "Ramones",
    "The Cure", "Green Day", "Linkin Park", "System of a Down", "Rage Against the Machine",
    "Soundgarden", "Alice in Chains", "Tool", "Lynyrd Skynyrd", "Santana"
]

# Definição das casas de show
casas = ["Turatti Varjota", "Turatti Papicu", "Turatti Kenedy", "Turatti Cambeba"]

# Dias da semana
dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

# Horários específicos para cada casa
horarios_por_casa = {
    "Turatti Varjota": {
        "Segunda": ["18:45", "21:30"],
        "Terça": ["18:45", "21:30"],
        "Quarta": ["18:45", "21:30"],
        "Quinta": ["17:00", "18:45", "21:30"],
        "Sexta": ["17:00", "18:45", "21:30"],
        "Sábado": ["17:00", "19:45", "22:30"],
        "Domingo": ["17:00", "18:45", "21:30"]
    },
    "Turatti Papicu": {
        "Segunda": ["19:30"],
        "Terça": ["19:30"],
        "Quarta": ["19:30"],
        "Quinta": ["19:30"],
        "Sexta": ["20:00"],
        "Sábado": ["20:00"],
        "Domingo": ["19:30"]
    },
    "Turatti Kenedy": {
        "Segunda": ["18:00"],
        "Terça": ["18:00"],
        "Quarta": ["18:00"],
        "Quinta": ["18:00"],
        "Sexta": ["16:30", "19:00"],
        "Sábado": ["16:30", "19:00"],
        "Domingo": ["18:00"]
    },
    "Turatti Cambeba": {
        "Segunda": [],
        "Terça": [],
        "Quarta": [],
        "Quinta": [],
        "Sexta": ["20:00"],
        "Sábado": ["20:00"],
        "Domingo": []
    }
}

# Função para coletar a data inicial e final
def coletar_datas():
    while True:
        try:
            data_inicial = input("Digite a data inicial (DD/MM/AAAA): ")
            data_final = input("Digite a data final (DD/MM/AAAA): ")
            
            # Converter para objetos datetime
            data_inicial = datetime.strptime(data_inicial, "%d/%m/%Y")
            data_final = datetime.strptime(data_final, "%d/%m/%Y")
            
            if data_inicial > data_final:
                print("A data inicial deve ser anterior à data final. Tente novamente.")
            else:
                return data_inicial, data_final
        except ValueError:
            print("Formato de data inválido. Use o formato DD/MM/AAAA.")

# Função para gerar a lista de dias no intervalo
def gerar_dias_no_intervalo(data_inicial, data_final):
    dias = []
    delta = data_final - data_inicial
    for i in range(delta.days + 1):
        dia = data_inicial + timedelta(days=i)
        dias.append(dia)
    return dias

# Função para coletar as notas e disponibilidades das bandas
def coletar_dados_bandas():
    dados_bandas = {}
    for banda in bandas:
        print(f"\n💿 Dados para a banda: {banda} 💿")
        
        # Coletar a nota da banda
        while True:
            try:
                nota = int(input(f"  - Nota (0 a 10): "))
                if 0 <= nota <= 10:
                    break
                else:
                    print("Por favor, insira um valor entre 0 e 10.")
            except ValueError:
                print("Por favor, insira um número válido.")
        
        # Coletar a disponibilidade da banda para cada dia
        disponibilidade = {}
        for dia in dias_semana:
            while True:
                disponivel = input(f"  - Disponível na {dia}? (s/n): ").strip().lower()
                if disponivel in ["s", "n", "n"]:
                    disponibilidade[dia] = disponivel == "s"
                    break
                else:
                    print("Por favor, insira 's' ou 'n'.")
        
        # Armazenar os dados da banda
        dados_bandas[banda] = {
            "nota": nota,
            "disponibilidade": disponibilidade
        }
    
    return dados_bandas



# Coletar os dados das bandas
print("="*40)
print(" INSIRA OS DADOS DAS BANDAS ")
print("="*40)
dados_bandas = coletar_dados_bandas()

# Coletar as datas inicial e final
print("\n" + "="*40)
print(" INSIRA AS DATAS INICIAL E FINAL ")
print("="*40)
data_inicial, data_final = coletar_datas()

# Gerar a lista de dias no intervalo
dias_no_intervalo = gerar_dias_no_intervalo(data_inicial, data_final)

# Criando lista de todos os slots possíveis (dia, horário, casa)
slots_disponiveis = []
for dia in dias_no_intervalo:
    dia_semana = dias_semana[dia.weekday()]  # Obter o dia da semana
    for casa in casas:
        for horario in horarios_por_casa[casa][dia_semana]:
            slots_disponiveis.append((casa, dia, dia_semana, horario))

# Função para calcular a pontuação de uma banda para um slot específico
def calcular_pontuacao(banda, dia_semana):
    """Calcula a pontuação de uma banda para um slot específico."""
    if not dados_bandas[banda]["disponibilidade"][dia_semana]:
        return -1  # Banda não está disponível nesse dia
    return dados_bandas[banda]["nota"]

# Lista final de alocações
alocacoes = []
bandas_usadas = {banda: 0 for banda in bandas}  # Contador de quantas vezes cada banda foi escalada
bandas_dias_usados = {banda: set() for banda in bandas}  # Dias em que cada banda já foi alocada

def dia_seguinte(dia_semana):
    """Retorna o dia seguinte ao dia fornecido."""
    index = dias_semana.index(dia_semana)
    return dias_semana[(index + 1) % len(dias_semana)]

def dia_anterior(dia_semana):
    """Retorna o dia anterior ao dia fornecido."""
    index = dias_semana.index(dia_semana)
    return dias_semana[(index - 1) % len(dias_semana)]

# Garantir que todas as casas tenham shows nos horários corretos
for casa, dia, dia_semana, horario in slots_disponiveis:
    melhor_banda = None
    melhor_pontuacao = -1

    # Verificar bandas disponíveis para o dia e horário
    bandas_disponiveis = [
        b for b in bandas
        if bandas_usadas[b] < 3  # Limite de 3 shows por banda
        and dia_semana not in bandas_dias_usados[b]  # Não tocar no mesmo dia
        and dia_anterior(dia_semana) not in bandas_dias_usados[b]  # Não tocar no dia anterior
        and dia_seguinte(dia_semana) not in bandas_dias_usados[b]  # Não tocar no dia seguinte
        and dados_bandas[b]["disponibilidade"][dia_semana]  # Banda está disponível no dia
    ]

    if not bandas_disponiveis:
        # Se não houver bandas disponíveis, escolher qualquer banda que não viole as restrições de dias consecutivos
        bandas_disponiveis = [
            b for b in bandas
            if dia_semana not in bandas_dias_usados[b]
            and dia_anterior(dia_semana) not in bandas_dias_usados[b]
            and dia_seguinte(dia_semana) not in bandas_dias_usados[b]
            and dados_bandas[b]["disponibilidade"][dia_semana]
        ]

    if not bandas_disponiveis:
        # Se ainda não houver bandas disponíveis, relaxar a restrição de dias consecutivos
        bandas_disponiveis = [
            b for b in bandas
            if dia_semana not in bandas_dias_usados[b]
            and dados_bandas[b]["disponibilidade"][dia_semana]
        ]

    if not bandas_disponiveis:
        # Se ainda não houver bandas disponíveis, escolher qualquer banda disponível no dia
        bandas_disponiveis = [b for b in bandas if dados_bandas[b]["disponibilidade"][dia_semana]]

    # Escolher a banda com a maior pontuação
    for banda in bandas_disponiveis:
        score = calcular_pontuacao(banda, dia_semana)
        if score > melhor_pontuacao:
            melhor_pontuacao = score
            melhor_banda = banda

    # Alocar a banda escolhida
    if melhor_banda:
        alocacoes.append((casa, dia.strftime("%d/%m/%Y"), dia_semana, horario, melhor_banda))
        bandas_usadas[melhor_banda] += 1
        bandas_dias_usados[melhor_banda].add(dia_semana)  # Registrar que a banda foi alocada nesse dia

# Organizando as alocações por casa, dia e horário
alocacoes.sort()

# Exibindo o resultado formatado
print("\n" + "="*40)
print(" PROGRAMAÇÃO DAS CASAS DE SHOW ")
print("="*40 + "\n")

# Criando estrutura para agrupar por casa
casas_dict = {casa: [] for casa in casas}

for casa, data, dia_semana, horario, banda in alocacoes:
    casas_dict[casa].append((data, dia_semana, horario, banda))

# Imprimindo os resultados organizados
for casa, eventos in casas_dict.items():
    print(f"\n🎵 {casa.upper()} 🎵\n" + "-"*40)
    
    # Ordenar dentro da casa por data e horário
    eventos.sort(key=lambda x: (datetime.strptime(x[0], "%d/%m/%Y"), x[2]))
    
    for data, dia_semana, horario, banda in eventos:
        print(f"{data} | {dia_semana:>8} | {horario} | {banda}")

print("\n" + "="*40)
print(" FIM DA PROGRAMAÇÃO ")
print("="*40 + "\n")