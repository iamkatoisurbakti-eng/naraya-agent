# SSH-backed file access failure

Observed failure signature in this environment:
- `SSH connection failed`
- `Warning: Identity file ... not accessible`
- `Permission denied (publickey,password)`

Implication:
- The failure is environmental/access-related, not necessarily a bad file path.
- It can affect multiple tools (`search_files`, `read_file`, `terminal`) at once.

Recovery pattern:
1. Stop retrying the same file query.
2. Check SSH/config prerequisites if available.
3. Use `session_search` to recover previously known paths or filenames.
4. Ask the user to upload the file or provide a direct path if access remains blocked.

Session note:
- In this session, both `search_files` and `terminal` hit the same SSH identity/publickey error when trying to inspect `/root/nusantara-ai-saas`.