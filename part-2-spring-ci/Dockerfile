FROM openjdk:25-ea-21-slim

ENV JAR_FILE=demo-0.0.1-SNAPSHOT.jar

WORKDIR /app

COPY ./target/${JAR_FILE} .

RUN useradd nonroot --no-create-home && \
    chown -R nonroot:nonroot /app

USER nonroot

CMD ["sh", "-c", "java -jar /app/${JAR_FILE}"]