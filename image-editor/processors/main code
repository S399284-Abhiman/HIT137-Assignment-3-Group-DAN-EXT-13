import cv2
import numpy as np
import os


def clamp_u8(img):
    return np.clip(img, 0, 255).astype(np.uint8)


def apply_brightness_contrast(img, brightness, contrast):
    b = int(brightness)
    alpha = float(contrast) / 100.0
    out = img.astype(np.float32) * alpha + b
    return clamp_u8(out)


def odd_ksize_from_intensity(intensity):
    intensity = max(0, min(int(intensity), 100))
    k = 1 + 2 * (intensity // 4)
    return min(k, 51)


def rotate_by_choice(img, choice):
    if choice == 1:
        return cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    if choice == 2:
        return cv2.rotate(img, cv2.ROTATE_180)
    if choice == 3:
        return cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img


def flip_by_choice(img, choice):
    if choice == 1:
        return cv2.flip(img, 1)
    if choice == 2:
        return cv2.flip(img, 0)
    return img


def fit_to_canvas(img, canvas_w, canvas_h):
    h, w = img.shape[:2]
    is_gray = (len(img.shape) == 2)

    if is_gray:
        canvas = np.zeros((canvas_h, canvas_w), dtype=img.dtype)
    else:
        canvas = np.zeros((canvas_h, canvas_w, img.shape[2]), dtype=img.dtype)

    if w > canvas_w:
        x0 = (w - canvas_w) // 2
        img = img[:, x0:x0 + canvas_w]
        w = canvas_w
    if h > canvas_h:
        y0 = (h - canvas_h) // 2
        img = img[y0:y0 + canvas_h, :]
        h = canvas_h

    y = (canvas_h - h) // 2
    x = (canvas_w - w) // 2
    canvas[y:y + h, x:x + w] = img
    return canvas


def window_is_open(win_name):
    try:
        return cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) >= 1
    except cv2.error:
        return False


def main():
    path = input("Enter image path: ").strip().strip('"')
    if not os.path.exists(path):
        return

    original = cv2.imread(path, cv2.IMREAD_COLOR)
    if original is None:
        return

    orig_h, orig_w = original.shape[:2]
    MAX_W = max(50, orig_w * 3)
    MAX_H = max(50, orig_h * 3)

    window = "OpenCV GUI Image Processor"
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window, 1600, 900)

    L = 28
    def label(s): return f"{s:<{L}}"

    TB_LOCK_ASP     = label("Lock Aspect Ratio")
    TB_FREE_STRETCH = label("Free Stretch")
    TB_WIDTH        = label("Width (px)")
    TB_HEIGHT       = label("Height (px)")
    TB_GRAY         = label("Grayscale")
    TB_BLUR         = label("Blur")
    TB_EDGES        = label("Edges")
    TB_CANNY_LOW    = label("Canny Low")
    TB_CANNY_HIGH   = label("Canny High")
    TB_BRIGHT       = label("Brightness")
    TB_CONTRAST     = label("Contrast")
    TB_ROTATE       = label("Rotate")
    TB_FLIP         = label("Flip")
    TB_KEEP_SIZE    = label("Keep Size")

    cv2.createTrackbar(TB_LOCK_ASP, window, 1, 1, lambda v: None)
    cv2.createTrackbar(TB_FREE_STRETCH, window, 0, 1, lambda v: None)
    cv2.createTrackbar(TB_WIDTH, window, orig_w, MAX_W, lambda v: None)
    cv2.createTrackbar(TB_HEIGHT, window, orig_h, MAX_H, lambda v: None)
    cv2.createTrackbar(TB_GRAY, window, 0, 1, lambda v: None)
    cv2.createTrackbar(TB_BLUR, window, 0, 100, lambda v: None)
    cv2.createTrackbar(TB_EDGES, window, 0, 1, lambda v: None)
    cv2.createTrackbar(TB_CANNY_LOW, window, 50, 255, lambda v: None)
    cv2.createTrackbar(TB_CANNY_HIGH, window, 150, 255, lambda v: None)
    cv2.createTrackbar(TB_BRIGHT, window, 100, 200, lambda v: None)
    cv2.createTrackbar(TB_CONTRAST, window, 100, 200, lambda v: None)
    cv2.createTrackbar(TB_ROTATE, window, 0, 3, lambda v: None)
    cv2.createTrackbar(TB_FLIP, window, 0, 2, lambda v: None)
    cv2.createTrackbar(TB_KEEP_SIZE, window, 1, 1, lambda v: None)

    def reset_sliders():
        cv2.setTrackbarPos(TB_LOCK_ASP, window, 1)
        cv2.setTrackbarPos(TB_FREE_STRETCH, window, 0)
        cv2.setTrackbarPos(TB_WIDTH, window, orig_w)
        cv2.setTrackbarPos(TB_HEIGHT, window, orig_h)
        cv2.setTrackbarPos(TB_GRAY, window, 0)
        cv2.setTrackbarPos(TB_BLUR, window, 0)
        cv2.setTrackbarPos(TB_EDGES, window, 0)
        cv2.setTrackbarPos(TB_CANNY_LOW, window, 50)
        cv2.setTrackbarPos(TB_CANNY_HIGH, window, 150)
        cv2.setTrackbarPos(TB_BRIGHT, window, 100)
        cv2.setTrackbarPos(TB_CONTRAST, window, 100)
        cv2.setTrackbarPos(TB_ROTATE, window, 0)
        cv2.setTrackbarPos(TB_FLIP, window, 0)
        cv2.setTrackbarPos(TB_KEEP_SIZE, window, 1)

    reset_sliders()
    cv2.imshow(window, original)
    cv2.waitKey(1)

    last_processed = original.copy()

    while True:
        if not window_is_open(window):
            break

        try:
            gray_on = cv2.getTrackbarPos(TB_GRAY, window)
            blur_int = cv2.getTrackbarPos(TB_BLUR, window)
            edges_on = cv2.getTrackbarPos(TB_EDGES, window)
            canny_low = cv2.getTrackbarPos(TB_CANNY_LOW, window)
            canny_high = cv2.getTrackbarPos(TB_CANNY_HIGH, window)
            brightness = cv2.getTrackbarPos(TB_BRIGHT, window) - 100
            contrast = cv2.getTrackbarPos(TB_CONTRAST, window)
            rotate_choice = cv2.getTrackbarPos(TB_ROTATE, window)
            flip_choice = cv2.getTrackbarPos(TB_FLIP, window)
            lock_aspect = cv2.getTrackbarPos(TB_LOCK_ASP, window)
            free_stretch = cv2.getTrackbarPos(TB_FREE_STRETCH, window)
            new_w = max(1, cv2.getTrackbarPos(TB_WIDTH, window))
            new_h = max(1, cv2.getTrackbarPos(TB_HEIGHT, window))
            keep_display = cv2.getTrackbarPos(TB_KEEP_SIZE, window)
        except cv2.error:
            break

        img = original.copy()
        img = apply_brightness_contrast(img, brightness, contrast)
        img = rotate_by_choice(img, rotate_choice)
        img = flip_by_choice(img, flip_choice)

        if free_stretch == 0 and lock_aspect == 1:
            aspect = orig_w / orig_h
            new_h = max(1, int(round(new_w / aspect)))
            if new_h > MAX_H:
                new_h = MAX_H
                new_w = max(1, int(round(new_h * aspect)))
            cv2.setTrackbarPos(TB_HEIGHT, window, new_h)
            cv2.setTrackbarPos(TB_WIDTH, window, new_w)

        interp = cv2.INTER_AREA if (new_w < orig_w or new_h < orig_h) else cv2.INTER_CUBIC
        img = cv2.resize(img, (new_w, new_h), interpolation=interp)

        k = odd_ksize_from_intensity(blur_int)
        if k > 1:
            img = cv2.GaussianBlur(img, (k, k), 0)

        if gray_on == 1 and len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        if edges_on == 1:
            g = img if len(img.shape) == 2 else cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            lo, hi = sorted((int(canny_low), int(canny_high)))
            img = cv2.Canny(g, lo, hi)

        last_processed = img
        display_img = fit_to_canvas(img, orig_w, orig_h) if keep_display else img
        cv2.imshow(window, display_img)

        key = cv2.waitKey(10) & 0xFF
        if key in (27, ord('q')):
            break
        if key == ord('r'):
            reset_sliders()
        if key == ord('s'):
            cv2.imwrite("output.png", last_processed)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

