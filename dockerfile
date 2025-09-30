# Dockerfile: docker CLI + Python 3.12 + FastAPI (venv)
FROM docker:cli

WORKDIR /app
COPY main.py /app/

RUN apk add --no-cache python3 py3-pip \
  && python3 -V | grep -E '^Python 3\.12\.' \
  && python3 -m venv /venv \
  && . /venv/bin/activate \
  && pip install --upgrade pip \
  && pip install fastapi "uvicorn[standard]"

ENV PATH="/venv/bin:$PATH"
EXPOSE 8000
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]

