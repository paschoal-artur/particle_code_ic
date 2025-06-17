import cv2

class MotionDetector:
    def __init__(self, history=100, var_threshold=40, detect_shadows=False, min_contour_area=500):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=history, 
            varThreshold=var_threshold, 
            detectShadows=detect_shadows
        )
        self.min_contour_area = min_contour_area

    def detect(self, frame):
        fg_mask = self.bg_subtractor.apply(frame)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask_cleaned = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        
        contours, _ = cv2.findContours(fg_mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        found_motion = False
        # --- CÓDIGO DE DEPURAÇÃO ---
        # Desenha todos os contornos encontrados no frame para visualização
        frame_with_contours = cv2.cvtColor(fg_mask_cleaned, cv2.COLOR_GRAY2BGR)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                # Se for maior que o limiar, pinta de VERDE
                cv2.drawContours(frame_with_contours, [contour], -1, (0, 255, 0), 2)
                found_motion = True
                print(f"MOVIMENTO VÁLIDO DETECTADO! Área: {area:.2f} (Limiar: {self.min_contour_area})")
            else:
                # Se for menor, pinta de VERMELHO (ignorado)
                cv2.drawContours(frame_with_contours, [contour], -1, (0, 0, 255), 1)
                # Opcional: descomente para ver o ruído
                # print(f"Movimento ignorado. Área: {area:.2f}")

        # Mostra a janela de depuração
        cv2.imshow("Debug de Movimento", frame_with_contours)
        # ------------------------

        return found_motion