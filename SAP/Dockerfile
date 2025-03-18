FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libaio1 \
        wget \
        unzip \
        gcc \
        g++ \
        libc6-dev \
        libsqlite3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# SDK SAP NW RFC
COPY nwrfcsdk.zip /tmp/
RUN unzip /tmp/nwrfcsdk.zip -d /usr/local/sap && rm /tmp/nwrfcsdk.zip

ENV SAPNWRFC_HOME=/usr/local/sap/nwrfcsdk
ENV LD_LIBRARY_PATH=${SAPNWRFC_HOME}/lib

WORKDIR /app

# Installation préliminaire
RUN pip install --upgrade pip setuptools wheel cython

# Copie du wheel pyrfc téléchargé manuellement
COPY pyrfc-3.3.1-cp39-cp39-linux_x86_64.whl .

# Installation pyrfc depuis le wheel local
RUN pip install pyrfc-3.3.1-cp39-cp39-linux_x86_64.whl

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
