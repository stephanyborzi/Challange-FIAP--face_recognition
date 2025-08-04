import cv2
import os

# Nome da pessoa e caminho
nome_pessoa = "pessoa1"
pasta_dataset = "dataset"
os.makedirs(pasta_dataset, exist_ok=True)

# Definir caminho padrão da imagem
caminhoimagem = os.path.join(pasta_dataset, f"{nome_pessoa}.jpg")

# Verifica se já existe
if os.path.exists(caminhoimagem):
    print(f"Imagem {caminhoimagem} já existe.")
    caminhoimagem = os.path.join(pasta_dataset, f"{nome_pessoa}_novo.jpg")
    print(f"Usando novo caminho: {caminhoimagem}")

# Inicia a webcam
webcam = cv2.VideoCapture(0)
contador = 0

if webcam.isOpened():
    print("Webcam aberta com sucesso.")
else:
    print("Erro ao abrir a webcam.")
    exit()

while True:
    ret, frame = webcam.read()
    if not ret:
        print("Erro ao capturar imagem.")
        break

    cv2.imshow("Captura de Imagem", frame)

    # Pressione 'c' para capturar a imagem
    if cv2.waitKey(1) & 0xFF == ord('c'):
        contador += 1
        caminho_final = os.path.join(pasta_dataset, f"{nome_pessoa}_{contador}.jpg")
        cv2.imwrite(caminho_final, frame)
        print(f"Imagem {contador} capturada: {caminho_final}")

    # Encerra após 10 capturas
    if contador >= 10:
        print("10 imagens capturadas. Encerrando.")
        break

webcam.release()
cv2.destroyAllWindows()
