import cv2
import pytesseract
import numpy as np

# Configuración de ruta para Tesseract en Windows (Ajustar según sea necesario)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def process_image_with_tesseract(image_path):
    print(f"--- Iniciando OCR para: {image_path} ---")
    
    # 1. Cargar imagen inicial con OpenCV
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: No se pudo cargar la imagen {image_path}")
        return
        
    # 2. Pre-procesamiento de la imagen (OpenCV)
    # Convertir a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Aplicar un filtro de desenfoque para remover ruido
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Aplicar umbral adaptativo (Binarización para separar texto de fondo)
    thresh = cv2.adaptiveThreshold(
        blur, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, 2
    )

    # 3. Extracción de datos usando PyTesseract
    # Configuración adicional de Tesseract (ej. psm 6 asume un bloque de texto uniforme)
    custom_config = r'--oem 3 --psm 6'
    
    # Extraer texto
    extracted_text = pytesseract.image_to_string(thresh, config=custom_config, lang='spa')
    
    print("\n--- Texto Extraído ---")
    print(extracted_text)
    print("----------------------")
    
    # Extraer cajas delimitadoras (Bounding boxes) para ilustrar otra característica
    boxes = pytesseract.image_to_boxes(thresh, lang='spa')
    
    # Dibujar las cajas en la imagen original para visualización
    h, w, _ = image.shape
    for b in boxes.splitlines():
        b = b.split(' ')
        image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    # Mostrar la imagen resultante con los cuadros delimitadores
    cv2.imshow('Imagen Preprocesada y Analizada', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Ejemplo de uso (asegúrate de tener una imagen "sample.png" en el directorio)
    # process_image_with_tesseract("sample.png")
    print("Script de ejemplo Tesseract OCR + OpenCV.")
    print("Para usarlo, descomenta la última línea y provee una imagen válida.")
