# File-backed secrets in tests

Session note: when verifying code that reads credentials from either env vars or files, ambient repo `.env` values can mask the branch under test.

Useful pattern:
- Create a temp directory in the test.
- Write a fixture key file there (for example `GPT-4.1 Mini.txt`).
- Point the code at that file with a test-only env var such as `OPENAI_CHAT_KEY_FILE`.
- Clear or restore env vars in `afterEach` so the branch is deterministic.

Observed pitfall:
- A test that set `process.env.OPENAI_API_KEY = 'openai-test-key'` was still overridden by an existing `.env` value in the repo runtime.
- Switching the test to the file-backed path made the assertion stable.

Related runner pitfall:
- If the repository `npm test` script chains multiple suites, `npm test -- <pattern>` may still execute extra suites. Use the dedicated suite command or invoke the underlying runner directly when you need a narrow verification target.
