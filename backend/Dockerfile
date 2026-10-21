FROM python:3.12-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN useradd --system --create-home app && chown -R app /app
USER app
EXPOSE 5065
HEALTHCHECK --interval=15s --timeout=5s --retries=5 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:5065/c30_get_current_time', timeout=4).status==200 else 1)"
# Create tables (and load the demo seed if SEED_DEMO_DATA=true), then serve
CMD ["sh", "-c", "python init_db_script.py && exec gunicorn -w 2 --threads 2 -b 0.0.0.0:5065 main_jkb_with_country:app"]
