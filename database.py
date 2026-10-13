import oracledb

from config import (
    ORACLE_DSN,
    ORACLE_PASSWORD,
    ORACLE_USER,
)


def conectar_oracle():
    """
    Cria e retorna uma conexao com Oracle.
    """

    return oracledb.connect(
        user=ORACLE_USER,
        password=ORACLE_PASSWORD,
        dsn=ORACLE_DSN,
    )


def salvar_registro_oracle(registro):
    """
    Insere um registro de colheita na tabela COLHEITA_CANA.
    """

    comando_sql = """
        INSERT INTO COLHEITA_CANA (
            TALHAO,
            AREA_HECTARES,
            PRODUTIVIDADE_ESTIMADA,
            PRODUCAO_COLHIDA,
            VALOR_TONELADA,
            PRODUCAO_ESPERADA,
            PERDA_TONELADAS,
            PERCENTUAL_PERDA,
            PREJUIZO_ESTIMADO,
            STATUS_PERDA,
            DATA_REGISTRO
        ) VALUES (
            :talhao,
            :area_hectares,
            :produtividade_estimada,
            :producao_colhida,
            :valor_tonelada,
            :producao_esperada,
            :perda_toneladas,
            :percentual_perda,
            :prejuizo_estimado,
            :status_perda,
            :data_registro
        )
    """

    parametros = {
        "talhao": registro["talhao"],
        "area_hectares": registro["area_hectares"],
        "produtividade_estimada": (
            registro["produtividade_estimada_t_ha"]
        ),
        "producao_colhida": (
            registro["producao_colhida_t"]
        ),
        "valor_tonelada": registro["valor_tonelada"],
        "producao_esperada": (
            registro["producao_esperada_t"]
        ),
        "perda_toneladas": registro["perda_t"],
        "percentual_perda": (
            registro["percentual_perda"]
        ),
        "prejuizo_estimado": (
            registro["prejuizo_estimado"]
        ),
        "status_perda": registro["status"],
        "data_registro": registro["data_registro"],
    }

    conexao = None
    cursor = None

    try:
        conexao = conectar_oracle()
        cursor = conexao.cursor()

        cursor.execute(
            comando_sql,
            parametros,
        )

        conexao.commit()

        return True, "Registro gravado no Oracle com sucesso."

    except oracledb.Error as erro:
        return False, (
            "Erro ao gravar registro no Oracle: "
            f"{erro}"
        )

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()


def consultar_registros_oracle():
    """
    Retorna registros da tabela COLHEITA_CANA.
    """

    comando_sql = """
        SELECT
            ID,
            TALHAO,
            AREA_HECTARES,
            PRODUTIVIDADE_ESTIMADA,
            PRODUCAO_COLHIDA,
            PRODUCAO_ESPERADA,
            PERDA_TONELADAS,
            PERCENTUAL_PERDA,
            PREJUIZO_ESTIMADO,
            STATUS_PERDA,
            DATA_REGISTRO
        FROM COLHEITA_CANA
        ORDER BY ID DESC
    """

    conexao = None
    cursor = None

    try:
        conexao = conectar_oracle()
        cursor = conexao.cursor()

        cursor.execute(comando_sql)

        registros = cursor.fetchall()

        return True, registros

    except oracledb.Error as erro:
        return False, (
            "Erro ao consultar registros no Oracle: "
            f"{erro}"
        )

    finally:
        if cursor:
            cursor.close()

        if conexao:
            conexao.close()