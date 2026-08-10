# Performance matrix



Each cell: **cold / warm_min–warm_max** seconds (3 psolves in one process).
NEURON columns: psolve wall. CN columns: CoreNEURON `Solver Time`.

| Config | CPU | GPU | CN CPU | CN GPU |
|--------|-----|-----|--------|--------|
| Dentate nt1 | 2.327 / 2.27–2.292 | 2.245 / 1.885–1.896 | 0.9873 / 0.9582–1.223 | 0.6436 / 0.531–0.5319 |
| Dentate nt4 | 0.9047 / 0.8746–0.8923 | 3.547 / 3.004–3.134 | 1.042 / 1.06–1.071 | 1.048 / 0.9555–0.9629 |

Raw CSV: `/home/hines/neuron/devbench/campaigns/2026-08-06-tip-dentate/raw/wall/results.csv`

