from datetime import datetime


STATUS_PERDA = (
    "BAIXO",
    "ATENCAO",
    "CRITICO",
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

        print("Entrada invalida. Informe um texto nao vazio.")


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
            print("Entrada invalida. Digite somente um numero.")


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
        "id": len(registros_colheita) + 1,
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

    encontrados = []

    for registro in registros_colheita:
        if registro["talhao"] == talhao:
            encontrados.append(registro)

    if not encontrados:
        print("Nenhum registro encontrado.")
        return

    for registro in encontrados:
        print()
        exibir_resumo_registro(registro)


def listar_registros_criticos():
    exibir_titulo("REGISTROS CRITICOS")

    criticos = []

    for registro in registros_colheita:
        if registro["status"] == STATUS_PERDA[2]:
            criticos.append(registro)

    if not criticos:
        print("Nenhum registro critico identificado.")
        return

    for registro in criticos:
        print()
        exibir_resumo_registro(registro)


def exibir_menu():
    exibir_titulo("CANAGUARD - CONTROLE DE PERDAS")

    print("1 - Cadastrar colheita")
    print("2 - Listar colheitas")
    print("3 - Consultar por talhao")
    print("4 - Exibir registros criticos")
    print("0 - Sair")


def ler_opcao_menu():
    opcoes_validas = ("0", "1", "2", "3", "4")

    while True:
        opcao = input("\nEscolha uma opcao: ").strip()

        if opcao in opcoes_validas:
            return opcao

        print("Opcao invalida. Escolha uma opcao do menu.")


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

        else:
            print("\nEncerrando o CanaGuard.")
            break


if __name__ == "__main__":
    main()