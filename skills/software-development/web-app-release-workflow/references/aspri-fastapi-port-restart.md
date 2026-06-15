# ASPRI FastAPI port-restart note

When restarting an ASPRI FastAPI app on a fixed port (for example 8090), an immediate `uvicorn ... --port 8090` can fail with `Errno 98 address already in use` if an older background server is still listening.

Reusable fix:
1. Check the listener:
   - `ss -ltnp '( sport = :8090 )'`
2. Identify the process:
   - `ps -fp <pid>`
3. Stop the old listener cleanly when appropriate:
   - `kill <pid>`
4. Start the server again in background mode and wait for it to bind.
5. Verify:
   - `curl http://127.0.0.1:8090/health`
   - `ss -ltnp '( sport = :8090 )'`

Notes:
- A foreground `uvicorn` command will not be useful if the port is already occupied; always inspect the live listener first.
- Prefer a clean restart over piling up duplicate server processes.
