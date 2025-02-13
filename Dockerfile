FROM python:latest

#COPY ./dist/         \
#  /tmp/dist/
#
#RUN pip install      \
#  /tmp/dist/*.whl    \
#&& rm -frv           \
#  /tmp/dist/
RUN pip install teamhack_rest \
&&  test -x /usr/bin/env      \
&&  command -v python

WORKDIR  /var/teamhack
VOLUME ["/var/teamhack/etc"]

ENTRYPOINT [         \
  "/usr/bin/env",    \
  "python",          \
  "-m",              \
  "teamhack_rest"    \
]

EXPOSE 5001/tcp

