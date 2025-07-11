# DevLab Module

DevLab extends Jarvik with an experimental development pipeline. It
communicates with the Jarvik API and stores context from every
interaction. The module runs two AI models in sequence using
`pipeline.Pipeline`. Its main entry point is `dev_engine.DevEngine`.

## Purpose

* Integrate Jarvik with auxiliary models for code generation.
* Persist prompts and outputs in `dev_memory/` with default topics
  "programování" and "technologie".
* Optionally log anonymized results to `logs/` for later review.

## Development flow

1. A prompt is passed to `DevEngine.run()`.
2. The prompt is processed by the pipeline ("Command R+" -> "StrCoder").
3. The output is stored in `dev_memory/` and returned to the caller.
4. If logging is enabled, the result is also written to `logs/`.

## Using from `Jarvik_W`

The DevLab module can be imported from other applications such as
`Jarvik_W`:

```python
from devlab.dev_engine import DevEngine

engine = DevEngine()
response = engine.run("Generate hello world")
print(response)
```

The connection URL to the Jarvik API can be adjusted in
`devlab/devlab_config.json`. The same file also accepts optional keys
`memory_path` and `knowledge_path` for customizing where prompt history
and knowledge data are stored. When DevLab is installed system-wide the
defaults may point inside the read-only package directory. Edit the
configuration or pass ``--config`` to ``devlab-cli`` to use writable
locations, for example ``~/.devlab/dev_memory`` and
``~/.devlab/knowledge_db``.
