import cv2
import os
import duckdb
import face_recognition
import numpy as np

#Tem que resolver o problema de importação do facial recognicion devido a versao do python
# Função para salvar os embeddings no banco
def salvar_embeddings(banco_path="face_db.duckdb"):
    criar_banco(banco_path)
    con = duckdb.connect(banco_path)

    for img_nome in os.listdir("dataset"):
        caminho_img = os.path.join("dataset", img_nome)

        # Tentativa de carregar a imagem
        imagem = face_recognition.load_image_file(caminho_img)
        rosto = face_recognition.face_encodings(imagem)

        if rosto:
            embedding = rosto[0]
            emb_bytes = embedding.tobytes()
            con.execute(
                "INSERT INTO embeddings (nome, caminho_imagem, embedding) VALUES (?, ?, ?)",
                (img_nome.split("_")[0], caminho_img, emb_bytes)
            )
    con.close()
    print("Embeddings salvos no banco com sucesso.")

# -------- CAPTURA DAS IMAGENS --------
nome_pessoa = input("Digite o nome da pessoa: ").strip()
pasta_dataset = "dataset"
os.makedirs(pasta_dataset, exist_ok=True)

webcam = cv2.VideoCapture(0)
contador = 0

if not webcam.isOpened():
    print("Erro ao abrir a webcam.")
    exit()

print("Pressione 'c' para capturar imagem. Pressione 'q' para sair.")

while True:
    ret, frame = webcam.read()
    if not ret:
        print("Erro ao capturar imagem.")
        break

    cv2.imshow("Captura de Imagem", frame)

    tecla = cv2.waitKey(1) & 0xFF

    if tecla == ord('c'):
        contador += 1
        caminho_final = os.path.join(pasta_dataset, f"{nome_pessoa}_{contador}.jpg")
        cv2.imwrite(caminho_final, frame)
        print(f"Imagem {contador} capturada: {caminho_final}")

    if contador >= 10 or tecla == ord('q'):
        print("Encerrando captura de imagens.")
        break

webcam.release()
cv2.destroyAllWindows()

# -------- SALVA OS EMBEDDINGS NO BANCO --------
salvar_embeddings()
