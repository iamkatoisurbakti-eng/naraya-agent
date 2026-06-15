# Landing feature-only studio cards + VIP pricing alignment

Session pattern from Nusantara AI SaaS:

- User disliked visible model/provider lists on the public landing studio cards: remove model names/logos from customer-facing landing cards when they ask for “fitur saja, model tidak perlu.”
- Important correction: keep or restore model visibility inside the authenticated dashboard Studio when the user says users should still see available models after login. Use a clear label like `Model Tersedia`, and keep result provider/model labels there if useful.
- Replace model/provider badges with benefit/feature chips such as:
  - Voice Agent: Medical Office, Restaurant Host, Help Desk, Custom Agent
  - Images: Text to Image, Style Control, Aspect Ratio, Variation
  - Video: Text to Video, Keyframe, Reference Media, Native Audio
  - Music: Voice Over, Audio Prompt, Narration, Browser Player
  - Chat: AI Chat, Reasoning, Writing, Research
- Put strategic features first in the landing grid when the user wants users to notice them; e.g. move `Voice Agent` before Images/Video/Music.
- If removing model visibility from the actual authenticated Studio is explicitly requested, hide the model dropdown and avoid printing provider/model names in result cards. Keep backend selection automatic with existing state/default model fallback. If the user clarifies that the dashboard should show available models, restore those controls and restrict feature-only cleanup to the public landing.
- When changing VIP plan credits/prices, update both:
  - frontend landing copy/cards
  - backend payment plan response and checkout grant amount
- Verify compiled production bundle/source does not contain unwanted customer-facing model strings (`Gemini`, `Grok`, `Claude`, `DeepSeek`, etc.) after build/deploy.
- Do not confuse “hapus model yang terlihat” with removing backend model catalog or provider routes; the likely intent is visual cleanup only.
