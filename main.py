import json
from datetime import datetime
from pathlib import Path

from database import (
    consultar_registros_oracle,
    salvar_registro_oracle,
)


STATUS_PERDA = (
    "BAIXO",
    "ATENCAO",
    "CRITICO",
)

DIRETORIO_RAIZ = Path(__file__).resolve().parent
DIRETORIO_DADOS = DIRETORIO_RAIZ / "data"
DIRETORIO_RELATORIOS = DIRETORIO_RAIZ / "reports"

ARQUIVO_JSON = DIRETORIO_DADOS / "colheitas.json"
ARQUIVO_RELATORIO = (
    DIRETORIO_RELATORIOS
    / "relatorio_colheitas.txt"
)

registros_colheita = []


def exibir_titulo(titulo):
    print()
    print("=" * 60)
    print(titulo)
    print("=" * 60)


def pausar():
    input("\nPressione Enter para continuar...")


def ler_texto_obrigatorio(mensagem):
    while True:
        valor = input(mensagem).strip()

        if valor:
            return valor

        print(
            "Entrada invalida. "
            "Informe um texto nao vazio."
        )


def ler_numero_positivo(mensagem, permite_zero=False):
    while True:
        valor = input(mensagem).strip().replace(",", ".")

        try:
            numero = float(valor)

            if permite_zero and numero >= 0:
                return numero

            if not permite_zero and numero > 0:
                return numero

            print("Informe um valor maior que zero.")

        except ValueError:
            print(
                "Entrada invalida. "
                "Digite somente um numero."
            )


def calcular_dados_colheita(
    area_hectares,
    produtividade_estimada,
    producao_colhida,
    valor_tonelada,
):
    producao_esperada = (
        area_hectares * produtividade_estimada
    )

    perda_toneladas = max(
        0,
        producao_esperada - producao_colhida,
    )

    percentual_perda = (
        (perda_toneladas / producao_esperada) * 100
        if producao_esperada > 0
        else 0
    )

    prejuizo_estimado = (
        perda_toneladas * valor_tonelada
    )

    return (
        producao_esperada,
        perda_toneladas,
        percentual_perda,
        prejuizo_estimado,
    )


def classificar_perda(percentual_perda):
    if percentual_perda <= 5:
        return STATUS_PERDA[0]

    if percentual_perda <= 10:
        return STATUS_PERDA[1]

    return STATUS_PERDA[2]


def obter_proximo_id():
    if not registros_colheita:
        return 1

    maior_id = max(
        registro["id"]
        for registro in registros_colheita
    )

    return maior_id + 1


def cadastrar_colheita():
    exibir_titulo("CADASTRO DE COLHEITA")

    talhao = ler_texto_obrigatorio(
        "Identificacao do talhao: "
    )

    area_hectares = ler_numero_positivo(
        "Area do talhao em hectares: "
    )

    produtividade_estimada = ler_numero_positivo(
        "Produtividade estimada em toneladas/hectare: "
    )

    producao_colhida = ler_numero_positivo(
        "Producao efetivamente colhida em toneladas: ",
        permite_zero=True,
    )

    valor_tonelada = ler_numero_positivo(
        "Valor da tonelada de cana em R$: "
    )

    (
        producao_esperada,
        perda_toneladas,
        percentual_perda,
        prejuizo_estimado,
    ) = calcular_dados_colheita(
        area_hectares,
        produtividade_estimada,
        producao_colhida,
        valor_tonelada,
    )

    status = classificar_perda(
        percentual_perda
    )

    registro = {
        "id": obter_proximo_id(),
        "talhao": talhao.upper(),
        "area_hectares": area_hectares,
        "produtividade_estimada_t_ha": produtividade_estimada,
        "producao_colhida_t": producao_colhida,
        "valor_tonelada": valor_tonelada,
        "producao_esperada_t": producao_esperada,
        "perda_t": perda_toneladas,
        "percentual_perda": percentual_perda,
        "prejuizo_estimado": prejuizo_estimado,
        "status": status,
        "data_registro": datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        ),
    }

    registros_colheita.append(registro)

    print()
    print("Registro cadastrado com sucesso.")
    exibir_resumo_registro(registro)


def exibir_resumo_registro(registro):
    print(f"ID: {registro['id']}")
    print(f"Talhao: {registro['talhao']}")
    print(
        "Producao esperada: "
        f"{registro['producao_esperada_t']:.2f} t"
    )
    print(
        "Producao colhida: "
        f"{registro['producao_colhida_t']:.2f} t"
    )
    print(
        "Perda estimada: "
        f"{registro['perda_t']:.2f} t"
    )
    print(
        "Percentual de perda: "
        f"{registro['percentual_perda']:.2f}%"
    )
    print(
        "Prejuizo estimado: "
        f"R$ {registro['prejuizo_estimado']:.2f}"
    )
    print(f"Classificacao: {registro['status']}")
    print(
        "Data do registro: "
        f"{registro['data_registro']}"
    )


def listar_colheitas():
    exibir_titulo("REGISTROS DE COLHEITA")

    if not registros_colheita:
        print("Nenhum registro cadastrado.")
        return

    print(
        f"{'ID':<4}"
        f"{'TALHAO':<15}"
        f"{'PERDA (%)':<12}"
        f"{'PREJUIZO (R$)':<18}"
        f"{'STATUS':<12}"
    )

    print("-" * 61)

    for registro in registros_colheita:
        print(
            f"{registro['id']:<4}"
            f"{registro['talhao']:<15}"
            f"{registro['percentual_perda']:<12.2f}"
            f"{registro['prejuizo_estimado']:<18.2f}"
            f"{registro['status']:<12}"
        )


def buscar_por_talhao():
    exibir_titulo("CONSULTAR TALHAO")

    if not registros_colheita:
        print("Nenhum registro cadastrado.")
        return

    talhao = ler_texto_obrigatorio(
        "Informe o talhao: "
    ).upper()

    encontrados = [
        registro
        for registro in registros_colheita
        if registro["talhao"] == talhao
    ]

    if not encontrados:
        print("Nenhum registro encontrado.")
        return

    for registro in encontrados:
        print()
        exibir_resumo_registro(registro)


def listar_registros_criticos():
    exibir_titulo("REGISTROS CRITICOS")

    criticos = [
        registro
        for registro in registros_colheita
        if registro["status"] == STATUS_PERDA[2]
    ]

    if not criticos:
        print("Nenhum registro critico identificado.")
        return

    for registro in criticos:
        print()
        exibir_resumo_registro(registro)


def salvar_json():
    exibir_titulo("SALVAR DADOS EM JSON")

    if not registros_colheita:
        print("Nao existem registros para salvar.")
        return

    try:
        DIRETORIO_DADOS.mkdir(
            parents=True,
            exist_ok=True,
        )

        with ARQUIVO_JSON.open(
            "w",
            encoding="utf-8",
        ) as arquivo:
            json.dump(
                registros_colheita,
                arquivo,
                ensure_ascii=False,
                indent=4,
            )

        print("Dados salvos com sucesso em:")
        print(ARQUIVO_JSON)

    except OSError as erro:
        print("Erro ao salvar o arquivo JSON:")
        print(erro)


def carregar_json():
    global registros_colheita

    exibir_titulo("CARREGAR DADOS DO JSON")

    if not ARQUIVO_JSON.exists():
        print("Arquivo JSON nao encontrado.")
        print(ARQUIVO_JSON)
        return

    try:
        with ARQUIVO_JSON.open(
            "r",
            encoding="utf-8",
        ) as arquivo:
            dados = json.load(arquivo)

        if not isinstance(dados, list):
            print(
                "Arquivo JSON invalido: "
                "a estrutura esperada e uma lista."
            )
            return

        registros_colheita = dados

        print(
            f"{len(registros_colheita)} "
            "registro(s) carregado(s) com sucesso."
        )

    except json.JSONDecodeError:
        print(
            "Erro: o arquivo JSON possui "
            "formato invalido."
        )

    except OSError as erro:
        print("Erro ao ler o arquivo JSON:")
        print(erro)


def montar_conteudo_relatorio():
    linhas = []

    linhas.append("=" * 70)
    linhas.append(
        "CANAGUARD - RELATORIO DE PERDAS NA COLHEITA"
    )
    linhas.append("=" * 70)
    linhas.append(
        "Data de geracao: "
        f"{datetime.now().strftime('%d/%m/%Y %H:%M')}"
    )
    linhas.append(
        f"Total de registros: {len(registros_colheita)}"
    )
    linhas.append("")

    if not registros_colheita:
        linhas.append("Nenhum registro cadastrado.")
        return "\n".join(linhas)

    total_perda = sum(
        registro["perda_t"]
        for registro in registros_colheita
    )

    total_prejuizo = sum(
        registro["prejuizo_estimado"]
        for registro in registros_colheita
    )

    total_criticos = sum(
        1
        for registro in registros_colheita
        if registro["status"] == STATUS_PERDA[2]
    )

    linhas.append("RESUMO GERAL")
    linhas.append("-" * 70)
    linhas.append(
        f"Perda total estimada: {total_perda:.2f} t"
    )
    linhas.append(
        "Prejuizo total estimado: "
        f"R$ {total_prejuizo:.2f}"
    )
    linhas.append(
        f"Registros criticos: {total_criticos}"
    )
    linhas.append("")

    linhas.append("DETALHAMENTO DOS REGISTROS")
    linhas.append("-" * 70)

    for registro in registros_colheita:
        linhas.append(
            f"ID {registro['id']} - "
            f"Talhao: {registro['talhao']}"
        )
        linhas.append(
            "Producao esperada: "
            f"{registro['producao_esperada_t']:.2f} t"
        )
        linhas.append(
            "Producao colhida: "
            f"{registro['producao_colhida_t']:.2f} t"
        )
        linhas.append(
            f"Perda: {registro['perda_t']:.2f} t"
        )
        linhas.append(
            "Percentual de perda: "
            f"{registro['percentual_perda']:.2f}%"
        )
        linhas.append(
            "Prejuizo estimado: "
            f"R$ {registro['prejuizo_estimado']:.2f}"
        )
        linhas.append(
            f"Status: {registro['status']}"
        )
        linhas.append("-" * 70)

    return "\n".join(linhas)


def gerar_relatorio_txt():
    exibir_titulo("GERAR RELATORIO TXT")

    try:
        DIRETORIO_RELATORIOS.mkdir(
            parents=True,
            exist_ok=True,
        )

        conteudo = montar_conteudo_relatorio()

        with ARQUIVO_RELATORIO.open(
            "w",
            encoding="utf-8",
        ) as arquivo:
            arquivo.write(conteudo)

        print("Relatorio gerado com sucesso em:")
        print(ARQUIVO_RELATORIO)

    except OSError as erro:
        print("Erro ao gerar o relatorio:")
        print(erro)


def salvar_ultimo_registro_oracle():
    exibir_titulo("GRAVAR ULTIMO REGISTRO NO ORACLE")

    if not registros_colheita:
        print("Nenhum registro cadastrado.")
        return

    ultimo_registro = registros_colheita[-1]

    sucesso, mensagem = salvar_registro_oracle(
        ultimo_registro
    )

    print(mensagem)


def listar_registros_oracle():
    exibir_titulo("CONSULTAR REGISTROS NO ORACLE")

    sucesso, resultado = consultar_registros_oracle()

    if not sucesso:
        print(resultado)
        return

    if not resultado:
        print("Nenhum registro encontrado no Oracle.")
        return

    print(
        f"{'ID':<5}"
        f"{'TALHAO':<15}"
        f"{'PERDA (%)':<12}"
        f"{'PREJUIZO (R$)':<18}"
        f"{'STATUS':<12}"
    )

    print("-" * 62)

    for registro in resultado:
        (
            identificador,
            talhao,
            _,
            _,
            _,
            _,
            _,
            percentual_perda,
            prejuizo_estimado,
            status,
            _,
        ) = registro

        print(
            f"{identificador:<5}"
            f"{talhao:<15}"
            f"{float(percentual_perda):<12.2f}"
            f"{float(prejuizo_estimado):<18.2f}"
            f"{status:<12}"
        )


def exibir_menu():
    exibir_titulo("CANAGUARD - CONTROLE DE PERDAS")

    print("1 - Cadastrar colheita")
    print("2 - Listar colheitas")
    print("3 - Consultar por talhao")
    print("4 - Exibir registros criticos")
    print("5 - Salvar dados em JSON")
    print("6 - Carregar dados do JSON")
    print("7 - Gerar relatorio em TXT")
    print("8 - Gravar ultimo registro no Oracle")
    print("9 - Consultar registros do Oracle")
    print("0 - Sair")


def ler_opcao_menu():
    opcoes_validas = (
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    )

    while True:
        opcao = input(
            "\nEscolha uma opcao: "
        ).strip()

        if opcao in opcoes_validas:
            return opcao

        print(
            "Opcao invalida. "
            "Escolha uma opcao do menu."
        )


def main():
    while True:
        exibir_menu()
        opcao = ler_opcao_menu()

        if opcao == "1":
            cadastrar_colheita()
            pausar()

        elif opcao == "2":
            listar_colheitas()
            pausar()

        elif opcao == "3":
            buscar_por_talhao()
            pausar()

        elif opcao == "4":
            listar_registros_criticos()
            pausar()

        elif opcao == "5":
            salvar_json()
            pausar()

        elif opcao == "6":
            carregar_json()
            pausar()

        elif opcao == "7":
            gerar_relatorio_txt()
            pausar()

        elif opcao == "8":
            salvar_ultimo_registro_oracle()
            pausar()

        elif opcao == "9":
            listar_registros_oracle()
            pausar()

        else:
            print("\nEncerrando o CanaGuard.")
            break


if __name__ == "__main__":
    main()