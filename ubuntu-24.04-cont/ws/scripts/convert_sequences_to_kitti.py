#!/usr/bin/env python3
"""
MP4 -> KITTI JPEG converter focused on numeric sequence names.

Intended workflow per your request:
- You will rename MP4 files to numeric sequence ids (e.g. 30.mp4, 31.mp4).
- Run this script to extract frames into `data/sequences_jpg/<seq>/image_<camera>/000000.jpg` ...

Features:
- Processes only video files (mp4/avi/mkv) by default.
- Detects numeric stems and can accept an explicit `--sequences` list.
- Uses `ffmpeg` if available; falls back to OpenCV if not.
- Options: overwrite existing, start index, jpeg quality.

Examples:
  python3 scripts/convert_sequences_to_kitti.py --input sequences --output data/sequences_jpg --camera 2
  python3 scripts/convert_sequences_to_kitti.py --input sequences --sequences 30,31,32 --overwrite
"""

import argparse
import shutil
import subprocess
from pathlib import Path
import re

try:
    import cv2
    _HAS_CV2 = True
except Exception:
    _HAS_CV2 = False


def run_ffmpeg_extract(video_path: Path, out_dir: Path, start_number: int = 0, quality: int = 2, overwrite: bool = True):
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-start_number", str(start_number),
    ]
    if overwrite:
        cmd.insert(1, "-y")
    # qscale 2 gives good quality; user can adjust
    cmd += ["-qscale:v", str(quality), str(out_dir / "%06d.jpg")]
    print("Running:", " ".join(cmd))
    subprocess.check_call(cmd)


def extract_with_opencv(video_path: Path, out_dir: Path, start_number: int = 0, quality: int = 95):
    if not _HAS_CV2:
        raise RuntimeError("ffmpeg not available and opencv-python not installed")
    out_dir.mkdir(parents=True, exist_ok=True)
    vid = cv2.VideoCapture(str(video_path))
    idx = start_number
    while True:
        ok, frame = vid.read()
        if not ok:
            break
        fname = out_dir / f"{idx:06d}.jpg"
        cv2.imwrite(str(fname), frame, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        idx += 1
    vid.release()


def find_numeric_videos(input_dir: Path):
    vids = []
    for p in sorted(input_dir.iterdir()):
        if p.is_file() and p.suffix.lower() in ('.mp4', '.avi', '.mkv'):
            stem = p.stem
            # accept numeric stems like '30' or '030'
            if re.fullmatch(r"\d+", stem):
                vids.append((stem, p))
    return vids


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', required=True, help='Input directory containing MP4 files (renamed to numeric ids)')
    parser.add_argument('--output', '-o', default='data/sequences_jpg', help='Output KITTI-style directory')
    parser.add_argument('--camera', '-c', default='2', help='Camera id to use in image_<camera> folder')
    parser.add_argument('--sequences', '-s', help='Comma-separated list of sequence ids to process (e.g. 30,31,32)')
    parser.add_argument('--no-ffmpeg', action='store_true', help='Do not use ffmpeg even if present')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing frames')
    parser.add_argument('--start-number', type=int, default=0, help='Start index for frame numbering (default 0)')
    parser.add_argument('--quality', type=int, default=2, help='ffmpeg qscale (lower=better), or OpenCV jpeg quality 0-100')
    args = parser.parse_args()

    input_dir = Path(args.input)
    out_root = Path(args.output)
    camera = args.camera

    if not input_dir.exists():
        raise SystemExit(f"Input directory does not exist: {input_dir}")

    use_ffmpeg = (shutil.which('ffmpeg') is not None) and (not args.no_ffmpeg)
    if use_ffmpeg:
        print('ffmpeg found - using it for video extraction')
    else:
        print('ffmpeg not used or not found - falling back to OpenCV if available')

    # collect videos
    if args.sequences:
        ids = [s.strip() for s in args.sequences.split(',') if s.strip()]
        seqs = []
        for sid in ids:
            # prefer files named <id>.mp4
            for ext in ('.mp4', '.avi', '.mkv'):
                p = input_dir / f"{sid}{ext}"
                if p.exists():
                    seqs.append((sid, p))
                    break
            else:
                print(f"Warning: sequence {sid} not found as mp4/avi/mkv in {input_dir}")
    else:
        seqs = find_numeric_videos(input_dir)

    if not seqs:
        print('No numeric MP4 sequences found in', input_dir)
        return

    for seq_name, path in seqs:
        print('Processing sequence:', seq_name, '->', path)
        target_dir = out_root / seq_name / f"image_{camera}"
        if target_dir.exists() and any(target_dir.iterdir()) and not args.overwrite:
            print('Skipping existing sequence (use --overwrite to force):', target_dir)
            continue
        # remove existing if overwrite
        if target_dir.exists() and args.overwrite:
            shutil.rmtree(target_dir)

        if use_ffmpeg:
            run_ffmpeg_extract(path, target_dir, start_number=args.start_number, quality=args.quality, overwrite=args.overwrite)
        else:
            extract_with_opencv(path, target_dir, start_number=args.start_number, quality=max(0, min(100, int(100 - args.quality))))

    print('Done. Output in', out_root)


if __name__ == '__main__':
    main()
