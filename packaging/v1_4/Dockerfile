# Build ONLY with an extracted, byte-verified v1.4.0 public source ZIP as context.
# Never use a Git checkout, untracked source tree, or a private adopter project.
FROM python:3.12-slim
LABEL org.opencontainers.image.title="ArquitecturaRepo" \
      org.opencontainers.image.description="Portable Agentic SDLC project scaffold v1.4.0" \
      org.opencontainers.image.source="https://github.com/MatiasAcunia/ArquitecturaRepo" \
      org.opencontainers.image.version="1.4.0" \
      org.opencontainers.image.licenses="MIT"
COPY . /opt/architecturarepo/
WORKDIR /opt/architecturarepo
ENTRYPOINT ["python", "/opt/architecturarepo/tools/scaffold_project.py"]
CMD ["--help"]
