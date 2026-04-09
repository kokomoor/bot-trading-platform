# Product Vision

## Mission
Provide a robust, operator-friendly trading platform that can run multiple autonomous strategies in parallel while preserving centralized execution control, risk integrity, and production observability.

## Non-goals (for this repo)
- No agentic/LLM orchestration framework.
- No strategy research notebook stack.
- No unnecessary distributed platform complexity.

## Target users
- Small trading teams deploying on Linux servers.
- Platform engineers needing reliable execution controls.
- Quant developers who need strategy isolation and repeatable runtime contracts.

## Value proposition
- Reliable OMS/execution core with clear authority boundaries.
- Fast strategy iteration without compromising production controls.
- Strong operational clarity (logs, metrics, runbooks).
- Extensible adapter model for brokers/exchanges/data providers.
