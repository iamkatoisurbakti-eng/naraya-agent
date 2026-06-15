# Front-end duplication checklist

Use this when a user reports a UI element appearing twice, especially when they cannot send screenshots.

## Fast triage
- Ask for the smallest useful snippet: component/HTML for the element, related CSS, and any console errors.
- If they cannot share files or images, request pasted code blocks only.
- Inspect the live DOM for duplicate elements before changing code.

## Common causes of a "double video" symptom
- The component is mounted/rendered twice.
- React StrictMode in development causes double-invocation or duplicate perceived playback.
- Two separate video elements are both visible.
- A background video and a foreground video are both enabled.
- CSS layering/positioning makes one video overlap another.

## DOM checks
- Search for `<video>` count in Elements panel.
- Compare rendered DOM tree with the component tree.
- Check whether the duplicate is actual DOM duplication or only visual overlap.
- Verify `z-index`, `position`, `opacity`, and `overflow` styles.

## Debug order
1. Confirm how many `<video>` nodes exist.
2. Identify which component renders each node.
3. Disable StrictMode or development-only wrappers as a test.
4. Check CSS layers and absolute positioning.
5. Fix the source of duplication, not just the symptom.

## Safety note
- If the user pastes API keys or secrets while debugging, advise immediate rotation/revocation and do not repeat them in the reply.
