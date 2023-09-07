FROM python:latest

COPY ./dist/         \
  /tmp/dist/

RUN pip install      \
  /tmp/dist/*.whl    \
&& rm -frv           \
  /tmp/dist/

ENTRYPOINT[          \
  "/usr/bin/python", \
  "-m",              \
  "teamhack_db",     \
]

