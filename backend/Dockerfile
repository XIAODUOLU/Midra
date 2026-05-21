FROM python:3.11-slim

WORKDIR /app

RUN sed -i 's|deb.debian.org|mirrors.ustc.edu.cn|g; s|security.debian.org|mirrors.ustc.edu.cn|g' /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       ffmpeg \
       fluidsynth \
       fluid-soundfont-gm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements_root.txt
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install --no-cache-dir -r /app/requirements_root.txt -r /app/backend/requirements.txt

COPY music_agent /app/music_agent
COPY backend /app/backend
COPY main.py /app/main.py
COPY setup.py /app/setup.py

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
