# KSR888 Data Member column-order change

Use this note when changing the admin Data Member table on imported PHP hosts like KSR888.

## Goal
Reorder the visible columns without changing the page design or other admin flows.

Target visible order:
1. NO
2. Username
3. Email
4. Rekening
5. No Hp
6. Refferal
7. Tanggal Daftar

## Source files
- `KSR888/site/resources/views/admin/data_member/data_member.blade.php`
- `KSR888/site/app/Http/Controllers/backoffice/DatamemberController.php`

## Steps
1. Inspect the Blade table header and DataTables column config together.
2. Update the `<th>` labels to the requested order.
3. Remove any visible `Aksi` column if the user wants a pure data listing.
4. Ensure the DataTables `columns` array matches the header order exactly.
5. Map the referral value to the actual field used by the controller, usually `ref_code`.
6. Keep `rek_details` as the composed rekening display unless the user asks otherwise.
7. Deploy and verify the live page via HTTP or container smoke check.

## Pitfalls
- Header order and DataTables config can drift if only one side is patched.
- `No HP` vs `No Hp` is a visible text-only difference; match the user's requested casing exactly.
- Avoid changing row actions or styling when the request is only about column format.
