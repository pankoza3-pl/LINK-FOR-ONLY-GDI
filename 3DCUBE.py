import ctypes
from ctypes import wintypes
import math
import win32api
import time

def ddtcube():
    WIDTH, HEIGHT = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
    ANGLE_INCREMENT = 0.05
    VELOCITY_X = 2
    VELOCITY_Y = 2

    cube_vertices = [
        [-1, -1, -1],
        [1, -1, -1],
        [1, 1, -1],
        [-1, 1, -1],
        [-1, -1, 1],
        [1, -1, 1],
        [1, 1, 1],
        [-1, 1, 1]
    ]

    cube_faces = [
        [0, 1, 2, 3],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
        [0, 3, 7, 4],
        [1, 2, 6, 5]
    ]

    face_colors = [
        0xFF0000,
        0x00FF00,
        0x0000FF,
        0xFFFF00,
        0xFF00FF,
        0x00FFFF
    ]

    def rotate(point, angle_x, angle_y, angle_z):
        x, y, z = point
        y, z = y * math.cos(angle_x) - z * math.sin(angle_x), y * math.sin(angle_x) + z * math.cos(angle_x)
        x, z = x * math.cos(angle_y) + z * math.sin(angle_y), -x * math.sin(angle_y) + z * math.cos(angle_y)
        x, y = x * math.cos(angle_z) - y * math.sin(angle_z), x * math.sin(angle_z) + y * math.cos(angle_z)
        return x, y, z

    def project(point, width, height, fov, viewer_distance, offset_x, offset_y):
        x, y, z = point
        factor = fov / (viewer_distance + z)
        x = x * factor + width / 8 + offset_x
        y = -y * factor + height / 8 + offset_y
        return x, y

    class WNDCLASS(ctypes.Structure):
        _fields_ = [("style", wintypes.UINT),
                    ("lpfnWndProc", ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_ulong, ctypes.c_uint, ctypes.c_int, ctypes.c_int)),
                    ("cbClsExtra", ctypes.c_int),
                    ("cbWndExtra", ctypes.c_int),
                    ("hInstance", wintypes.HINSTANCE),
                    ("hIcon", wintypes.HICON),
                    ("hCursor", wintypes.HANDLE),
                    ("hbrBackground", wintypes.HBRUSH),
                    ("lpszMenuName", wintypes.LPCWSTR),
                    ("lpszClassName", wintypes.LPCWSTR)]

    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32

    WNDPROCTYPE = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_ulong, ctypes.c_uint, ctypes.c_int, ctypes.c_int)
    def wnd_proc(hwnd, msg, wparam, lparam):
        if msg == 2:
            ctypes.windll.user32.PostQuitMessage(0)
        return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wparam, lparam)

    hInstance = ctypes.windll.kernel32.GetModuleHandleW(None)
    wndclass = WNDCLASS()
    wndclass.lpfnWndProc = WNDPROCTYPE(wnd_proc)
    wndclass.hInstance = hInstance
    wndclass.hCursor = ctypes.windll.user32.LoadCursorW(None, 32512)
    wndclass.hbrBackground = None
    wndclass.lpszClassName = "3D Cube"

    ctypes.windll.user32.RegisterClassW(ctypes.byref(wndclass))

    hwnd = ctypes.windll.user32.CreateWindowExW(
        0,
        wndclass.lpszClassName,
        "3D Cube",
        0xCF0000,
        100, 100, WIDTH, HEIGHT,
        None, None, hInstance, None
    )

    ctypes.windll.user32.ShowWindow(hwnd, 1)
    ctypes.windll.user32.UpdateWindow(hwnd)

    hdc = ctypes.windll.user32.GetDC(hwnd)

    memdc = gdi32.CreateCompatibleDC(hdc)
    hbitmap = gdi32.CreateCompatibleBitmap(hdc, WIDTH, HEIGHT)
    gdi32.SelectObject(memdc, hbitmap)

    position_x, position_y = WIDTH // 2, HEIGHT // 2
    velocity_x, velocity_y = VELOCITY_X, VELOCITY_Y

    angle_x = angle_y = angle_z = 0
    while True:
        msg = wintypes.MSG()
        while ctypes.windll.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
            ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
            ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
            if msg.message == 0x0012:
                break
        else:
            gdi32.BitBlt(memdc, 0, 0, WIDTH, HEIGHT, None, 0, 0, 0x00000042)

            for i, face in enumerate(cube_faces):
                points = [rotate(cube_vertices[vertex], angle_x, angle_y, angle_z) for vertex in face]
                points = [project(point, WIDTH, HEIGHT, 256, 4, position_x, position_y) for point in points]
                points = [(int(x), int(y)) for x, y in points]

                if all(0 <= x <= WIDTH and 0 <= y <= HEIGHT for x, y in points):
                    polygon = (wintypes.POINT * len(points))(*[wintypes.POINT(x, y) for x, y in points])
                    brush = gdi32.CreateSolidBrush(face_colors[i])
                    gdi32.SelectObject(memdc, brush)
                    gdi32.Polygon(memdc, ctypes.byref(polygon), len(points))
                    gdi32.DeleteObject(brush)

            angle_x += ANGLE_INCREMENT
            angle_y += ANGLE_INCREMENT
            angle_z += ANGLE_INCREMENT

            position_x += velocity_x
            position_y += velocity_y

            if position_x < 0:
                position_x = 0
                velocity_x = -velocity_x
            elif position_x > WIDTH - 1:
                position_x = WIDTH - 1
                velocity_x = -velocity_x

            if position_y < 0:
                position_y = 0
                velocity_y = -velocity_y
            elif position_y > HEIGHT - 1:
                position_y = HEIGHT - 1
                velocity_y = -velocity_y

            gdi32.BitBlt(hdc, 0, 0, WIDTH, HEIGHT, memdc, 0, 0, 0x00CC0020)

            time.sleep(0.01)

            continue
        break

    gdi32.DeleteObject(hbitmap)
    gdi32.DeleteDC(memdc)
    ctypes.windll.user32.ReleaseDC(hwnd, hdc)
    ctypes.windll.user32.DestroyWindow(hwnd)

ddtcube()
