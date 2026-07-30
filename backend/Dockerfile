# ============================================================
# backend/Dockerfile
# ============================================================
#
# 📖 A Dockerfile is a recipe for building a container image.
# Each line is a "layer". Docker caches layers — so if only
# your app code changes, it doesn't reinstall all packages.
# This makes builds FAST after the first one.
# ============================================================

# FROM — Start from an official base image.
# "python:3.12-slim" = Python 3.12 on Debian Linux (slim = minimal OS)
# Always pin to a specific version (not "latest") for reproducibility.
FROM python:3.12-slim

# WORKDIR — Set the working directory inside the container.
# All following commands run from /app.
# Like doing `cd /app` inside the container.
WORKDIR /app

# ============================================================
# 📖 WHY COPY requirements.txt BEFORE the rest of the code?
# ============================================================
# Docker builds in layers. If requirements.txt hasn't changed,
# Docker uses its cached layer and SKIPS pip install entirely.
# This saves 2-3 minutes on every rebuild when you only edit .py files.
# This ordering trick is one of the most important Dockerfile optimizations!
# ============================================================

# COPY — Copy files from your machine INTO the container.
# Format: COPY <source-on-your-machine> <destination-in-container>
COPY requirements.txt .

# RUN — Execute a shell command during the BUILD phase.
# --no-cache-dir → Don't cache downloaded packages (saves space)
# --upgrade pip  → Get the latest pip first
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code.
# This layer changes every time you edit any .py file,
# but it's fast since it's just a file copy, not an install.
COPY . .

# EXPOSE — Document which port this container listens on.
# (This doesn't actually open the port — ports: in compose does that)
EXPOSE 8000

# CMD — The default command to run when the container starts.
# uvicorn = ASGI server for FastAPI
# app.main:app = the `app` object inside app/main.py
# --host 0.0.0.0 = listen on ALL network interfaces (not just localhost)
#                   Without this, the container can't receive external traffic!
# --port 8000 = listen on port 8000
# --reload = auto-restart when .py files change (dev mode only)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
