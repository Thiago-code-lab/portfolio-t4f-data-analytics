# Snapshot de origem

t4f-demo.json é uma cópia byte a byte do JSON público demonstrativo do T4F Performance, main 0216dce. Dados synthetic_demo, seed 42, sem pessoas ou contratos reais. Versionado por ser pequeno e reproduzível.

Procedência e SHA-256 em docs/fontes.json. Conferência: python -m src.ingestao. Gerador original em vendor/t4f/scripts; python -m src.gerar_demo confere igualdade byte a byte em diretório temporário. Não editar a fonte para fabricar resultados.
