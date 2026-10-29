"""Prepare an agent's video for the site.  Usage: python3 tools/add_video.py <LW-ref> <input-video> [--keep-check]
- Strips ALL audio (Lodgewell rule: videos are always muted).
- Shrinks to phone quality (max 720px wide, ~1 Mbps, 30 fps, max 90 s) with fast-start for streaming.
- Writes media/<ref>.mp4 and a poster media/<ref>.jpg, plus a frame sheet for the privacy check.
- Prints the new file size and the total media size against the GitHub Pages budget.
"""
import os, subprocess, sys, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ref, src = sys.argv[1].upper(), sys.argv[2]
out = os.path.join(ROOT, 'media', f'{ref}.mp4'); poster = out[:-4] + '.jpg'
os.makedirs(os.path.dirname(out), exist_ok=True)
run = lambda *a: subprocess.run(a, check=True, capture_output=True, text=True)
run('ffmpeg', '-y', '-i', src, '-an', '-t', '90',
    '-vf', "scale='min(720,iw)':-2,fps=30", '-c:v', 'libx264', '-preset', 'slow', '-crf', '28',
    '-maxrate', '1200k', '-bufsize', '2400k', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out)
dur = float(run('ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', out).stdout)
run('ffmpeg', '-y', '-ss', str(min(1.0, dur / 3)), '-i', out, '-frames:v', '1', '-q:v', '4', poster)
# frame sheet (6 frames) for checking watermarks / phone numbers before publishing
sheet = os.path.join(os.environ.get('TMPDIR', '/tmp'), f'{ref}-check.jpg')
run('ffmpeg', '-y', '-i', out, '-vf', f"fps=6/{max(dur,1):.2f},scale=240:-2,tile=6x1", '-frames:v', '1', sheet)
has_audio = run('ffprobe', '-v', 'error', '-select_streams', 'a', '-show_entries', 'stream=index', '-of', 'csv=p=0', out).stdout.strip()
assert not has_audio, 'audio stream still present'
size = os.path.getsize(out) + os.path.getsize(poster)
total = sum(os.path.getsize(os.path.join(ROOT, 'media', f)) for f in os.listdir(os.path.join(ROOT, 'media')))
n = len([f for f in os.listdir(os.path.join(ROOT, 'media')) if f.endswith('.mp4')])
print(json.dumps({'video': f'media/{ref}.mp4', 'poster': f'media/{ref}.jpg', 'seconds': round(dur, 1),
                  'mb': round(size / 1e6, 2), 'media_total_mb': round(total / 1e6, 1), 'videos': n,
                  'budget': 'OK' if total < 500e6 else ('WARN: plan move to R2' if total < 750e6 else 'MOVE TO R2 NOW'),
                  'check_sheet': sheet}))
