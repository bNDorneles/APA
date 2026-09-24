# Pacote de códigos e benchmarks - TP1 (APA)

Implementações em Python 3: clássicos, referência DPES, algoritmo autoral OEBA, testes e benchmark.

## Estrutura

```text
codigo/
├── Makefile
├── README.md
└── python/
    ├── classical.py
    ├── authorial.py          # DPES (referência docente)
    ├── oeba.py               # OEBA (autoral)
    ├── metrics.py
    ├── student_template.py
    ├── test_suite.py
    ├── test_authorial.py
    └── benchmark.py
```

## Como executar

### Testes

```bash
make test
# ou:
python python/test_suite.py
python python/test_authorial.py
```

### Benchmark

```bash
make benchmark
# ou:
python python/benchmark.py --trials 3 --plot ../images/benchmark_results.png
```

Dependência: `matplotlib`.
