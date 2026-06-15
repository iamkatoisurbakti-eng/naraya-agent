# Video/audio pipeline debugging notes

Use this when an ffmpeg-generated MP4 renders correctly but has no audio.

## Symptoms
- `ffprobe -show_streams` reports only a video stream.
- The output file plays silently or Telegram/YouTube rejects it as low-quality.

## Fast checks
1. Inspect the source asset:
   - `ffprobe -v error -show_streams -of json <file.mp4>`
2. Confirm whether the input already has audio.
3. If the source is silent, the fix belongs in the generation step, not the overlay step.
4. If the source has audio but the output does not, verify `ffmpeg` mapping:
   - Use `-map 0:a?` for passthrough audio when present.
   - Use `-map 1:a:0` only when you intentionally inject a synthetic audio source.

## Proven workaround for synthesized narration
- For environments with libflite enabled, `ffmpeg` can generate a narration track directly:
  - `-f lavfi -i flite=textfile=<path>:voice=kal`
- Encode the output audio explicitly, e.g. `-c:a aac -b:a 128k`.
- Add `-shortest` so the audio does not outlive the video.

## Verification
- Run `ffprobe -show_streams` on the final MP4 and confirm there is an `audio` stream.
- If reprocessing existing outputs, regenerate files that lack audio rather than marking them complete.

## Pitfall
- Reusing an existing output path can hide the fix if the script skips already-existing files. Check for a missing audio stream, not only file existence.