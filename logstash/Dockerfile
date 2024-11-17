FROM docker.elastic.co/logstash/logstash:7.17.9

# Install the MQTT input plugin
RUN bin/logstash-plugin install logstash-input-mqtt

# Copy Logstash pipeline configuration files
COPY pipeline/ /usr/share/logstash/pipeline/
