import os
import glob
import datetime

cutoff = datetime.datetime(2026, 11, 4, 23, 0, 0, tzinfo=datetime.timezone.utc)
print(f"Checking files modified since {cutoff} in scripts/ and repository root:")

for pattern in ["scripts/*", "*.py", "apps/portal/services/*", "apps/portal/tests/*"]:
    for p in glob.glob(pattern):
        if os.path.isfile(p):
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(p), tz=datetime.timezone.utc)
            if mtime > cutoff:
                print(f"  {mtime.isoformat()} | {os.path.getsize(p):>7} bytes | {p}")
