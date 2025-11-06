.. _codearc-benchmarking-reasoning-capabilities-of-llm-agents-for-inductive-program-synthesis:

CodeARC: Benchmarking Reasoning Capabilities of LLM Agents for Inductive Program Synthesis
==========================================================================================

:id: 2503.23145
:Authors: Anjiang Wei, Tarun Suresh, Jiannan Cao, Naveen Kannan, Yuheng Wu, Kai Yan, Thiago S. F. X. Teixeira, Ke Wang, Alex Aiken
:Published: 2025-03-29
:arXiv: https://arxiv.org/abs/2503.23145
:PDF: https://arxiv.org/pdf/2503.23145
:DOI: N/A
:Journal Reference: N/A
:Primary Category: cs.PL
:Categories: cs.PL, cs.AI, cs.CL, cs.LG
:Comment: N/A

:github_url: _

abstract
--------
Inductive program synthesis, or programming by example, requires synthesizing
functions from input-output examples that generalize to unseen inputs. While
large language model agents have shown promise in programming tasks guided by
natural language, their ability to perform inductive program synthesis is
underexplored. Existing evaluation protocols rely on static sets of examples
and held-out tests, offering no feedback when synthesized functions are
incorrect and failing to reflect real-world scenarios such as reverse
engineering. We propose CodeARC, the Code Abstraction and Reasoning Challenge,
a new evaluation framework where agents interact with a hidden target function
by querying it with new inputs, synthesizing candidate functions, and
iteratively refining their solutions using a differential testing oracle. This
interactive setting encourages agents to perform function calls and
self-correction based on feedback. We construct the first large-scale benchmark
for general-purpose inductive program synthesis, featuring 1114 functions.
Among 18 models evaluated, o3-mini performs best with a success rate of 52.7%,
highlighting the difficulty of this task. Fine-tuning LLaMA-3.1-8B-Instruct on
curated synthesis traces yields up to a 31% relative performance gain. CodeARC
provides a more realistic and challenging testbed for evaluating LLM-based
program synthesis and inductive reasoning. Our code, data, and models are
publicly available at https://github.com/Anjiang-Wei/CodeARC

.. include:: premise.rst

.. include:: outline.rst

.. include:: quotes.rst

.. include:: notes.rst