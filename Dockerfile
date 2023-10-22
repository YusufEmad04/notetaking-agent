FROM public.ecr.aws/lambda/python:3.11

ARG VAR1
ARG VAR2

ENV OPENAI_API_KEY=$VAR1
ENV PINECONE_API_KEY=$VAR2

COPY requirements.txt ${LAMBDA_TASK_ROOT}
COPY main.py ${LAMBDA_TASK_ROOT}
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
RUN pip install -r requirements.txt

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_handler.lambda_handler" ]