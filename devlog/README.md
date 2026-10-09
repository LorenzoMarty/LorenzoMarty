# Dev Log

Um arquivo por dia em `AAAA/AAAA-MM-DD.md`, resumo semanal em `weekly/AAAA-Www.md`.

**Rotina (2 minutos no fim do dia):** abra a entrada de hoje (o GitHub Action já criou), marque o que saiu em *Foco de hoje*, liste em *Feito* / *Aprendi* / *Bloqueios*, e deixe 1–3 itens em *Amanhã*. Todo `- [ ]` que ficar aberto vira o *Foco* do dia seguinte automaticamente.

| Quando | O que acontece |
|---|---|
| Todo dia, 05:13 (Brasília) | Cria a entrada do dia trazendo as tarefas abertas da última entrada |
| Toda execução | Atualiza o resumo da semana atual |
| Segunda-feira | Fecha o resumo da semana anterior |

O dia vira às 5h, então o que você escreve às 2h da manhã ainda conta para a noite anterior.

Localmente:

```bash
python scripts/devlog.py new          # entrada de hoje
python scripts/devlog.py week         # resumo desta semana
python scripts/devlog.py week --last  # resumo da semana passada
```

Variáveis opcionais: `DEVLOG_TZ` (padrão `America/Sao_Paulo`) e `DEVLOG_DAY_START` (padrão `5`).
