FROM apache/airflow:3.0.6

# Allow build-time override of AIRFLOW_UID; default kept in compose
ARG AIRFLOW_UID=5001

ADD requirements.txt .
RUN pip install apache-airflow==${AIRFLOW_VERSION} -r requirements.txt

# Create a dedicated tmp folder for caches that will be writable by the airflow user
ENV TMPDIR=/opt/airflow/tmp
RUN mkdir -p /opt/airflow/tmp \
	&& chown -R ${AIRFLOW_UID}:0 /opt/airflow/tmp