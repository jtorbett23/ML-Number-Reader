FROM python:3.11-slim AS base

ENV PYROOT=/PYROOTENV 
ENV PYTHONUSERBASE=$PYROOT

FROM base AS builder

RUN pip install --upgrade pip
RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

RUN PIP_USER=1 PIP_IGNORE_INSTALLED=1 pipenv install --system --deploy --ignore-pipfile

FROM base

COPY --from=builder $PYROOT/lib/ $PYROOT/lib/
COPY --from=builder $PYROOT/bin/ $PYROOT/bin/
ENV PATH="$PYROOT/bin:$PATH"

RUN pip install packaging
RUN pip install certifi

COPY api.py numberreader.h5 use_model.py ./

CMD ["fastapi", "run", "api.py", "--port", "8080"]