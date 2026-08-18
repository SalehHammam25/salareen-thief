# Stage 5 Cloud Tunneling Operator Runbook

## Safety boundary

The selected provider is ngrok using an account-assigned stable development
domain. Do not paste a
token into source, shared JSON, command history captured as evidence, an issue,
or a Pull Request. A public URL proves reachability only; authentication remains
Stage 6.

## External prerequisites

An operator must install/authenticate ngrok outside Git and authorize firewall
access. The public domain and opponent endpoint remain private process values.

Supported private environment names:

- `NGROK_DOMAIN` (bare account-assigned domain; ignored/private only)
- `SALAREEN_OPPONENT_URL`

The ngrok authentication token stays only in ngrok's user-level configuration.
Never pass it as an argument or inspect/copy `ngrok.yml`.

Response timeout, watchdog timeout, retry backoff, and retry count come from the
shared agreed JSON. Private environment values cannot override them. Annex F
defaults are 30, 60, 5, and 3 respectively; backoff and retries are minimums.

The provider token and any URL query credential must never be logged. Diagnostics
must use the endpoint redactor.

## Start and exchange

1. Start the thief FastMCP process locally on its selected loopback port.
2. Load `NGROK_DOMAIN` privately and start `NgrokProvider` only after the local
   `/mcp` endpoint is ready. Its subprocess is equivalent to
   `ngrok http <LOCAL_PORT> --url https://<ASSIGNED_DOMAIN>`.
3. Wait for `TunnelReady` and a successful provider health check.
4. Exchange the current public URLs out of band with the cop operator. Inject
   the cop URL as `SALAREEN_OPPONENT_URL`; do not commit it.
5. Validate bidirectional health before starting a match.

No discovery server or shared state is introduced. Stage 6 signs/authenticates
the manually exchanged endpoints.

## Failure and shutdown

DNS, TLS, timeout, disconnect, expired endpoint, provider exit, and retry
exhaustion produce typed infrastructure failures. Gameplay pauses during bounded
reconnect. Resume requires exact game, session, protocol, turn, and phase
identity. Mismatch aborts without inventing a winner.
On controlled exit, always await `TunnelController.stop()` or use its async
context manager. Confirm the provider reports stopped before closing the local
peer. Restart requires a new readiness check and the identical stable domain.

## Cop-side compatibility procedure

On a separate cop machine, start its compatible FastMCP Streamable HTTP server,
then run `ngrok http <COP_LOCAL_PORT> --url
https://<COP_ASSIGNED_DOMAIN>`. Configure the cop's private opponent URL as
`https://<THIEF_ASSIGNED_DOMAIN>/mcp` and the thief's
`SALAREEN_OPPONENT_URL` as `https://<COP_ASSIGNED_DOMAIN>/mcp`. Confirm both
`/mcp` endpoints before play. Replace placeholders only in private
shells/configuration, never Git.

## Required external acceptance evidence

Before Stage 5 can pass, authorized operators on two independent machines must
record redacted evidence for thief-to-cop reachability, cop-to-thief reachability,
a complete remote match, tunnel restart, latency, disconnect, retry exhaustion,
watchdog behavior, clean shutdown, provider/client versions, and confirmation
that no credentials appear in logs or committed files.
