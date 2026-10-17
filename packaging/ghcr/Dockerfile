FROM python:3.12-slim
LABEL org.opencontainers.image.title="ArquitecturaRepo" \
      org.opencontainers.image.description="Portable Agentic SDLC project scaffold v1.3.0" \
      org.opencontainers.image.source="https://github.com/MatiasAcunia/ArquitecturaRepo" \
      org.opencontainers.image.url="https://github.com/MatiasAcunia/ArquitecturaRepo" \
      org.opencontainers.image.version="1.3.0" \
      org.opencontainers.image.licenses="MIT"
COPY . /opt/architecturarepo/
WORKDIR /opt/architecturarepo
ENTRYPOINT ["python", "/opt/architecturarepo/tools/scaffold_project.py"]
CMD ["--help"]
