# Stage 5 Cloud Tunneling Operator Runbook

## Safety boundary

This repository does not select or provision a tunnel provider. Do not paste a
token into source, shared JSON, command history captured as evidence, an issue,
or a Pull Request. A public URL proves reachability only; authentication remains
Stage 6.

## External prerequisites

An operator must explicitly choose an available provider (the specification
lists ngrok and Localtonet as examples), approve its account/plan, install its
client, authorize firewall access, and place credentials in a private process
environment. These actions were not performed by Codex.

Supported private environment names:

- `SALAREEN_TUNNEL_PROVIDER`
- `SALAREEN_TUNNEL_TOKEN`
- `SALAREEN_OPPONENT_URL`

Response timeout, watchdog timeout, retry backoff, and retry count come from the
shared agreed JSON. Private environment values cannot override them. Annex F
defaults are 30, 60, 5, and 3 respectively; backoff and retries are minimums.

The provider token and any URL query credential must never be logged. Diagnostics
must use the endpoint redactor.

## Start and exchange

1. Start the thief FastMCP process locally on its selected loopback port.
2. Start the approved provider through a provider adapter implementing
   `TunnelProvider`; pass the local FastMCP URL.
3. Wait for `TunnelReady` and a successful provider health check.
4. Exchange the current public URLs out of band with the cop operator. Inject
   the cop URL as `SALAREEN_OPPONENT_URL`; do not commit it.
5. Validate bidirectional health before starting a match.

The exact provider adapter and out-of-band exchange channel require owner and
cop-team agreement. No discovery server or shared state is introduced.

## Failure and shutdown

DNS, TLS, timeout, disconnect, expired endpoint, provider exit, and retry
exhaustion produce typed infrastructure failures. They do not silently select a
game outcome because reconnect/resume and outage attribution remain unresolved.
On controlled exit, always await `TunnelController.stop()` or use its async
context manager. Confirm the provider reports stopped before closing the local
peer. Restart requires a new readiness check and URL exchange.

## Required external acceptance evidence

Before Stage 5 can pass, authorized operators on two independent machines must
record redacted evidence for thief-to-cop reachability, cop-to-thief reachability,
a complete remote match, tunnel restart, latency, disconnect, retry exhaustion,
watchdog behavior, clean shutdown, provider/client versions, and confirmation
that no credentials appear in logs or committed files.
