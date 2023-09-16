FROM python:latest

#COPY ./dist/         \
#  /tmp/dist/
#
#RUN pip install      \
#  /tmp/dist/*.whl    \
#&& rm -frv           \
#  /tmp/dist/
RUN pip install teamhack_rest

ENTRYPOINT [         \
  "/usr/bin/python", \
  "-m",              \
  "teamhack_rest"    \
]

EXPOSE 5000/tcp

