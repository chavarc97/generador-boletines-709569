import boto3
from fastapi import FastAPI, UploadFile, Form
import os
from dotenv import load_dotenv

load_dotenv()

expediente = "709569"
nombre_completo = "Salvador Rodriguez"

app = FastAPI(title="Practica 4")

s3_client = boto3.client("s3")
sqs_client = boto3.client("sqs")
sts_client = boto3.client("sts")

aws_account_id = sts_client.get_caller_identity()["Account"]

bucket_name = f"practica-4-{expediente}"


@app.post("/boletines")
async def crear_boletin(
    file: UploadFile, contenido: str = Form(...), correo: str = Form(...)
):
    # 1. Subir a S3
    s3_key = f"boletines/{file.filename}"
    file_content = await file.read()
    s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=file_content, ExpectedBucketOwner=aws_account_id)
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"

    # 2. Enviar a SQS
    sqs_url = os.getenv("SQS_URL")
    import json
    mensaje = json.dumps({
        "contenido": contenido,
        "correo": correo,
        "s3_url": s3_url,
    })
    sqs_client.send_message(QueueUrl=sqs_url, MessageBody=mensaje)

    # 3. Retornar mensaje de exito
    return {"mensaje": "Boletin creado exitosamente", "s3_url": s3_url}


preguntas = """
1. ¿Qué función cumple SQS dentro de esta arquitectura?
2. ¿Por qué es útil desacoplar el emisor del receptor?
3. ¿Qué ventajas ofrece SNS en este flujo?
"""

conclusiones = """
Escribe aquí tus conclusiones sobre la práctica.
"""

if __name__ == "__main__":
    print("Evaluación de la práctica 4")
    print(f"Nombre del alumno: {nombre_completo}")
    print(f"Expediente: {expediente}")
    print(preguntas)
    print(conclusiones)
