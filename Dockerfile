# Read the doc: https://huggingface.co/docs/hub/spaces-sdks-docker
FROM python:3.10-slim

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=user . /app

# Expose port 7860 as required by Hugging Face
EXPOSE 7860

CMD ["streamlit", "run", "Dashboard_儀表板.py", "--server.port=7860", "--server.address=0.0.0.0"]