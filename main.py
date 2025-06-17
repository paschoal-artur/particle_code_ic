# main_tracker.py
import cv2
import time
import numpy as np # Necessário para np.array em algumas chamadas de visualização
from ball_tracker_project.config import Config
from ball_tracker_project.roi_handler import ROIHandler
from ball_tracker_project.ball_detector import detect_balls_hough
from ball_tracker_project.tracker_manager import TrackerManager
from ball_tracker_project.motion_detector import MotionDetector
import ball_tracker_project.visualization_utils as viz

def preprocess_frame(frame):
    """Aplica pré-processamentos consistentes ao frame (ex: rotação)."""
    if Config.ROTATE_VIDEO_CLOCKWISE:
        return cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    return frame

def main():
    cap = cv2.VideoCapture(Config.VIDEO_PATH)
    if not cap.isOpened():
        print(f"Erro: Não foi possível abrir o vídeo em '{Config.VIDEO_PATH}'")
        return

    ret, first_frame_raw = cap.read()
    if not ret:
        print("Erro: Não foi possível ler o primeiro frame.")
        cap.release()
        return
    
    first_frame = preprocess_frame(first_frame_raw)

    # 1. Gerenciamento da ROI
    roi_manager = ROIHandler(first_frame)
    if not roi_manager.load_roi():
        print("Nenhuma ROI salva encontrada ou falha ao carregar. Iniciando seleção manual.")
        if not roi_manager.select_roi_interactively():
            print("ROI não definida. Encerrando.")
            cap.release()
            return
        roi_manager.save_roi()
    else:
        reselect = input("ROI carregada. Deseja definir uma nova? (s/n, padrão n): ").lower()
        if reselect == 's':
            if not roi_manager.select_roi_interactively():
                print("ROI não definida após tentativa de reseleção. Encerrando.")
                cap.release()
                return
            roi_manager.save_roi()

    roi_points = roi_manager.get_points()
    roi_mask = roi_manager.get_mask(first_frame.shape)

    if roi_points is None or roi_mask is None:
        print("Falha ao obter ROI. Encerrando.")
        cap.release()
        return
    tracker_mgr = TrackerManager(tracker_type=Config.TRACKER_TYPE)
    motion_detector = MotionDetector(min_contour_area=Config.MIN_MOTION_AREA)  # Inicializa o detector de movimento
    is_tracking_active = False
    total_initial_trackers = 0

    # 2. Loop Principal (lógica de detecção e tracking agora está aqui dentro)
    print("\n--- Iniciando processamento do vídeo ---")
    frame_count = 0
    output_window_name = "Rastreamento de Bolas"
    cv2.namedWindow(output_window_name, cv2.WINDOW_NORMAL)

    # Reinicia o vídeo para começar do início
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    while True:
        ret, frame_raw = cap.read()
        if not ret:
            print("Fim do vídeo ou erro ao ler frame.")
            break

        current_frame = preprocess_frame(frame_raw)
        frame_count += 1
        start_time = time.time()
        
        display_frame = current_frame.copy()
        viz.draw_roi_on_frame(display_frame, roi_points)
        
        successful_updates = 0

        if not is_tracking_active:
            # --- ESTADO: AGUARDANDO MOVIMENTO ---
            
            # Aplica a máscara da ROI para focar a detecção de movimento
            frame_in_roi = cv2.bitwise_and(current_frame, current_frame, mask=roi_mask)
            
            if motion_detector.detect(frame_in_roi):
                print(f"[Frame {frame_count}] Movimento detectado! Tentando encontrar bolas...")
                
                # Movimento detectado, agora rode a detecção de bolas
                initial_balls, _ = detect_balls_hough(current_frame, roi_points, roi_mask)
                
                if initial_balls:
                    print(f"Bolas encontradas! Inicializando {len(initial_balls)} tracker(s).")
                    if tracker_mgr.initialize_trackers(current_frame, initial_balls):
                        is_tracking_active = True # Muda para o estado de tracking
                        total_initial_trackers = len(tracker_mgr.get_all_objects_info())
                        
                        # Desenha a detecção que iniciou o tracking
                        viz.draw_detected_balls(display_frame, initial_balls)
                    else:
                        print("Falha ao inicializar trackers, continuará procurando movimento.")
                else:
                    print("Movimento detectado, mas nenhuma bola encontrada. Continuando...")
        else:
            # --- ESTADO: RASTREAMENTO ATIVO ---
            
            # Atualiza trackers
            successful_updates = tracker_mgr.update_trackers(current_frame)
            
            # Obtém informações dos objetos rastreados (ativos e inativos)
            all_tracked_objects = tracker_mgr.get_all_objects_info()
            viz.draw_tracked_objects(display_frame, all_tracked_objects)

            # Condição para resetar: se todos os trackers forem perdidos
            if not tracker_mgr.get_tracked_objects_info():
                print("Todos os trackers perderam o objeto. Voltando a aguardar por novo movimento.")
                is_tracking_active = False # Volta para o estado de espera

        # Calcula FPS
        fps = 1.0 / (time.time() - start_time) if (time.time() - start_time) > 0 else 0
        
        # Desenha HUD
        hud_status = "Rastreando" if is_tracking_active else "Aguardando Movimento"
        viz.draw_hud(display_frame, fps, frame_count, successful_updates, total_initial_trackers, status=hud_status) # Adicione um status no HUD
        
        viz.resize_display_frame(display_frame, output_window_name)
        cv2.imshow(output_window_name, display_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Loop interrompido pelo usuário.")
            break
            
    print(f"Processamento concluído. Total de frames processados: {frame_count}")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()