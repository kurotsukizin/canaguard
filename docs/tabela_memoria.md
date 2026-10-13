# Tabela de Memória — CanaGuard

A tabela abaixo representa o comportamento das principais variáveis durante o cadastro de uma colheita.

## Cenário utilizado

```text
Talhão: T-01
Área: 10 hectares
Produtividade estimada: 100 toneladas/hectare
Produção colhida: 850 toneladas
Valor da tonelada: R$ 145,00
```

## Tabela

| Variável | Tipo | Valor de exemplo | Finalidade |
|---|---|---:|---|
| `talhao` | `str` | `"T-01"` | Identifica a área agrícola monitorada |
| `area_hectares` | `float` | `10.0` | Armazena a área do talhão em hectares |
| `produtividade_estimada` | `float` | `100.0` | Representa a expectativa de produção em toneladas por hectare |
| `producao_colhida` | `float` | `850.0` | Armazena a produção efetivamente obtida |
| `valor_tonelada` | `float` | `145.0` | Representa o valor financeiro de uma tonelada de cana |
| `producao_esperada` | `float` | `1000.0` | Resultado de `area_hectares × produtividade_estimada` |
| `perda_toneladas` | `float` | `150.0` | Diferença entre produção esperada e produção colhida |
| `percentual_perda` | `float` | `15.0` | Percentual de perda sobre a produção esperada |
| `prejuizo_estimado` | `float` | `21750.0` | Estimativa financeira da perda |
| `status` | `str` | `"CRITICO"` | Classificação da perda calculada pelo sistema |
| `registro` | `dict` | Dicionário da colheita | Agrupa todos os dados de uma colheita |
| `registros_colheita` | `list` | `[registro]` | Mantém todos os registros em memória |
| `STATUS_PERDA` | `tuple` | `("BAIXO", "ATENCAO", "CRITICO")` | Mantém classificações fixas e imutáveis |

## Cálculo demonstrado

```text
producao_esperada = 10 × 100
producao_esperada = 1000 toneladas

perda_toneladas = 1000 - 850
perda_toneladas = 150 toneladas

percentual_perda = (150 / 1000) × 100
percentual_perda = 15%

prejuizo_estimado = 150 × 145
prejuizo_estimado = R$ 21.750,00
```

## Classificação

```text
Até 5%       = BAIXO
De 5% a 10%  = ATENCAO
Acima de 10% = CRITICO
```

> Os limites de classificação são critérios didáticos utilizados pelo CanaGuard e não substituem uma avaliação agronômica profissional.