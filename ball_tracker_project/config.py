# config.py

# --- Configurações de Vídeo e ROI ---
class Config:
    def __init__(
        self,
        HOUGH_GRAY_BLUR_KERNEL=(9,9),
        HOUGH_GRAY_BLUR_SIGMA_X=0.0,
        HOUGH_DP=1.5,
        HOUGH_MIN_DIST=15,
        HOUGH_PARAM1=20,
        HOUGH_PARAM2=25,
        HOUGH_MIN_RADIUS=15,
        HOUGH_MAX_RADIUS=20
    ):
        self.VIDEO_PATH = 'video_partículasArtur/videoTesteEdited.mp4' # Coloque o vídeo na pasta 'videos/'
        self.ROI_CONFIG_FILE = "roi_config.json"
        self.ROTATE_VIDEO_CLOCKWISE = False # Defina como True se o vídeo precisar ser rotacionado 90 graus no sentido horário

        self.MIN_MOTION_AREA = 350         # Área mínima em pixels para considerar movimento válido. Ajuste conforme necessário.

        # --- Configurações de Detecção de Bolas (HoughCircles) ---
        self.HOUGH_GRAY_BLUR_KERNEL = HOUGH_GRAY_BLUR_KERNEL
        self.HOUGH_GRAY_BLUR_SIGMA_X = HOUGH_GRAY_BLUR_SIGMA_X
        self.HOUGH_DP = HOUGH_DP            # Relação inversa da resolução do acumulador.
        self.HOUGH_MIN_DIST = HOUGH_MIN_DIST           # Distância mínima entre centros de círculos detectados.
        self.HOUGH_PARAM1 = HOUGH_PARAM1             # Limite superior para Canny.
        self.HOUGH_PARAM2 = HOUGH_PARAM2             # Limiar do acumulador para centros de círculos.
        self.HOUGH_MIN_RADIUS = HOUGH_MIN_RADIUS         # Raio mínimo do círculo.
        self.HOUGH_MAX_RADIUS = HOUGH_MAX_RADIUS         # Raio máximo do círculo.

        # --- Configurações de Tracking ---
        self.TRACKER_TYPE = "CSRT"         # Opções: "CSRT", "KCF", "MOSSE" (MOSSE é do cv2.legacy)

        # --- Configurações de Visualização ---
        self.ROI_COLOR = (255, 0, 0)       # Azul para ROI
        self.BALL_DETECT_COLOR = (0, 255, 0) # Verde para detecção inicial
        self.BALL_DETECT_CENTER_COLOR = (0, 0, 255) # Vermelho para centro da detecção
        self.TRAJECTORY_LINE_THICKNESS = 2
        self.BOUNDING_BOX_THICKNESS = 2
        self.HUD_TEXT_COLOR = (0, 0, 255)  # Vermelho para informações na tela (FPS, etc.)
        self.WINDOW_MAX_HEIGHT = 720       # Altura máxima para as janelas de exibição
    # --- Configurações de Vídeo e ROI ---
Config = Config()
#Config = Config((15, 15),0.7,2.9,1000,25,40,5,40) # Exemplo de como criar uma instância com parâmetros personalizados