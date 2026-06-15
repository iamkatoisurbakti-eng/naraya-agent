# News platform separation

Use this pattern when the main SaaS app and the news product are separate surfaces.

## Rule
- Do not leave any news widget, sidebar entry, quick card, or dashboard section on the main app when news lives on a separate platform/subdomain.
- Remove both the visible navigation and the conditional render branches for the news section.
- Keep the news surface accessible only from the dedicated news app/subdomain.

## Removal checklist
1. Delete the sidebar/menu item.
2. Delete quick-create or dashboard shortcut cards.
3. Remove header title branches that mention news.
4. Remove the news render block from the main dashboard route.
5. Remove unused imports/icons/hooks only after the UI branch is gone.
6. Run a production build to catch JSX imbalance or dead-code residue.

## Verification
- Search the source for `news` and ensure only the intended news-specific files still reference it.
- Run `npm run build:web`.
- If the app ships a dedicated news subdomain, verify the main platform no longer exposes that surface.
