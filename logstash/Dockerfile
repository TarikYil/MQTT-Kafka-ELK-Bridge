# IF THE DATA WILL BE IMPORTED WITH LOGSTACHE MQTT, THESE OPERATIONS ARE DONE, IF IT WILL BE IMPORTED WITH KAFKA, THERE IS NO NEED.
FROM docker.elastic.co/logstash/logstash:7.17.9

# Install the MQTT input plugin
RUN bin/logstash-plugin install logstash-input-mqtt

# Copy Logstash pipeline configuration files
COPY pipeline/ /usr/share/logstash/pipeline/
