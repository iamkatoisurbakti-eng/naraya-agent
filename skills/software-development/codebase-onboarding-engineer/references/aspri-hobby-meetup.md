# ASPRI Hobby Meetup

Use this reference for the ASPRI HOBBY feature in `/root/nusantara-agent/aspri-nusantara-app`.

## Purpose

ASPRI HOBBY is for arranging sports meetups for pebisnis UMKM and active community members. Current user-facing focus: Basketball, Padel, Tennis, and Gym as networking-oriented events.

## Backend additions

- feature key: `hobby`
- workflow templates:
  - `basket-run`
  - `padel-meetup`
  - `tennis-network`
  - `gym-network`
  - `sports-club`
- local fallback answer for `/feature/hobby`

## UI additions

- home grid tile: `ASPRI HOBBY`
- dedicated hobby screen for brief generation
- admin feature dropdown includes Hobby
- admin workflow template dropdown includes hobby templates
- admin template list should include `Gym Network` when the audience is expanded to gym-focused networking

## Verification

- `GET /features` includes `hobby`
- `GET /workflow/templates?feature=hobby` returns hobby templates
- `POST /feature/hobby` returns a meetup brief
- frontend/admin inline JS still passes `node --check`

## Good brief fields

- sport type
- event title
- venue / city
- target attendees
- purpose or networking goal

## Notes

- Prefer the internal key `basket-run` but show the user-facing label `Basketball` in the UI when aligning with the UMKM/networking brief.
- Keep the output oriented to real meetups: pairing, venue selection, schedule, and networking after play.
- This feature should stay lightweight; it is a community/event brief generator, not a booking engine.
