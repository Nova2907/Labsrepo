import cv2
import os


def main():
    print("=== ЗАПУСК ПРОГРАММЫ (RGR Variant 8: Hardcore FPS) ===")
    print("Выберите источник видео:")
    print("1 - Веб-камера")
    print("2 - Видеофайл")

    choice = input("Введите номер (1 или 2): ").strip()

    source = None
    if choice == '1':
        print(">> Выбрана веб-камера.")
        source = 0
    elif choice == '2':
        filename = input("Введите имя файла (например, Video.mp4): ").strip()
        if not os.path.exists(filename):
            print(f"Ошибка: Файл '{filename}' не найден!")
            return
        print(f">> Выбран файл: {filename}")
        source = filename
    else:
        print("Неверный выбор.")
        return

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        print("Ошибка открытия видео.")
        return
    ret, test_frame = cap.read()
    if not ret: return

    if choice == '2':
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    original_h, original_w = test_frame.shape[:2]
    new_width = 1000
    scale_ratio = new_width / original_w
    new_height = int(original_h * scale_ratio)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('Result.avi', fourcc, 120.0, (new_width, new_height))

    mode = 'normal'

    # ---НАСТРОЙКИ СКОРОСТИ---
    # delay = 1000 / FPS
    DELAY_SLOW = 16
    DELAY_NORM = 8
    DELAY_FAST = 4

    current_delay = DELAY_NORM
    speed_text = "(Normal)"

    print("\n" + "=" * 40)
    print(" УПРАВЛЕНИЕ:")
    print("=" * 40)
    print(" [f] - Размытие")
    print(" [e] - Контрастность")
    print(" [b] - Черно-белый")
    print(" [c] - Сброс фильтров")
    print("-" * 20)
    print(" [1] - Медленно")
    print(" [2] - Норма")
    print(" [3] - Быстро")
    print("-" * 20)
    print(" [q] - Выход")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Видео закончилось.")
            break


        frame = cv2.resize(frame, (new_width, new_height))
        key = cv2.waitKey(current_delay) & 0xFF

        # --- ФИЛЬТРЫ ---
        if key == ord('f'):
            mode = 'blur'
        elif key == ord('e'):
            mode = 'contrast'
        elif key == ord('b'):
            mode = 'bw'
        elif key == ord('c'):
            mode = 'normal'

        # --- СКОРОСТЬ ---
        elif key == ord('1'):
            current_delay = DELAY_SLOW
            speed_text = "Slow"
        elif key == ord('2'):
            current_delay = DELAY_NORM
            speed_text = "Normal"
        elif key == ord('3'):
            current_delay = DELAY_FAST
            speed_text = "Fast"

        elif key == ord('q'):
            break

        # 3. Применение эффектов
        if mode == 'blur':
            frame = cv2.GaussianBlur(frame, (15, 15), 0)
        elif mode == 'contrast':
            frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=10)
        elif mode == 'bw':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        info_text = f"Mode: {mode} | {speed_text}"
        cv2.putText(frame, info_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        out.write(frame)
        cv2.imshow('RGR Player', frame)

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print("Видео сохранено.")


if __name__ == "__main__":
    main()