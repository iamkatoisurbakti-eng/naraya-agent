#!/usr/bin/env bash
set -euo pipefail

docker exec nusantara-ai-saas-ksr888-web-1 php artisan tinker --execute='$r = app(App\\Services\\GameXaImageSyncService::class)->syncAll(); echo json_encode(["provider_count" => $r["provider_count"] ?? null, "provider_images" => $r["provider_images"] ?? null, "games_synced" => $r["games_synced"] ?? null, "game_images" => $r["game_images"] ?? null, "db_with_images" => $r["db_with_images"] ?? null, "db_missing_images" => $r["db_missing_images"] ?? null, "duration_seconds" => $r["duration_seconds"] ?? null]);'
