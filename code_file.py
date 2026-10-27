import turtle
import math
import datetime
import time

state = {
    "depth": 3,
    "current_size": 0,
    "target_size": 250,
    "thickness": 2,
    "angle": 0,
    "color_idx": 0,
    "colors": ["#00f2fe", "#ff0844", "#b066fe", "#10b981", "#f59e0b", "#ffffff"],
    "is_animating": False
}


def draw_line(t, A, B):
    t.up()
    t.setpos(A[0], A[1])
    t.down()
    t.setpos(B[0], B[1])


def split_segment(A, B):
    ax, ay = A
    bx, by = B
    p1 = (ax + (bx - ax) / 3, ay + (by - ay) / 3)
    p3 = (ax + 2 * (bx - ax) / 3, ay + 2 * (by - ay) / 3)

    dx = p3[0] - p1[0]
    dy = p3[1] - p1[1]
    angle = math.pi / 3

    p2_x = p1[0] + dx * math.cos(angle) - dy * math.sin(angle)
    p2_y = p1[1] + dx * math.sin(angle) + dy * math.cos(angle)
    return p1, (p2_x, p2_y), p3


def draw_koch(t, A, B, depth):
    if depth == 0:
        draw_line(t, A, B)
        return
    P1, P2, P3 = split_segment(A, B)
    draw_koch(t, A, P1, depth - 1)
    draw_koch(t, P1, P2, depth - 1)
    draw_koch(t, P2, P3, depth - 1)
    draw_koch(t, P3, B, depth - 1)


def get_triangle_vertices(x, y, size, rotation_deg=0):
    h = size * math.sqrt(3) / 2
    pts = [(-size / 2, h / 3), (size / 2, h / 3), (0, -2 * h / 3)]

    rad = math.radians(rotation_deg)
    rotated_pts = []
    for px, py in pts:
        rx = px * math.cos(rad) - py * math.sin(rad)
        ry = px * math.sin(rad) + py * math.cos(rad)
        rotated_pts.append((rx + x, ry + y))

    return rotated_pts[0], rotated_pts[1], rotated_pts[2]


def draw_snowflake(t, x, y, size, depth, color, pensize, rotation=0):
    t.color(color)
    t.pensize(pensize)
    A, B, C = get_triangle_vertices(x, y, size, rotation)
    draw_koch(t, A, B, depth)
    draw_koch(t, B, C, depth)
    draw_koch(t, C, A, depth)


buttons = [
    {"label": "Глиб. -1", "x": -350, "y": -330, "w": 90, "h": 36, "action": "depth_minus", "bg": "#1e293b"},
    {"label": "Глиб. +1", "x": -250, "y": -330, "w": 90, "h": 36, "action": "depth_plus", "bg": "#1e293b"},
    {"label": "Розмір -", "x": -140, "y": -330, "w": 90, "h": 36, "action": "size_minus", "bg": "#1e293b"},
    {"label": "Розмір +", "x": -40, "y": -330, "w": 90, "h": 36, "action": "size_plus", "bg": "#1e293b"},
    {"label": "Товщ. -", "x": 60, "y": -330, "w": 80, "h": 36, "action": "pen_minus", "bg": "#1e293b"},
    {"label": "Товщ. +", "x": 150, "y": -330, "w": 80, "h": 36, "action": "pen_plus", "bg": "#1e293b"},
    {"label": "КОЛІР", "x": 250, "y": -330, "w": 80, "h": 36, "action": "color_next", "bg": "#3b82f6"},
    {"label": "ЗБЕРЕГТИ", "x": 360, "y": -330, "w": 100, "h": 36, "action": "save", "bg": "#ef4444"},
]


def draw_rounded_rect(t, x, y, w, h, r, color):
    t.up()
    t.goto(x - w / 2 + r, y - h / 2)
    t.setheading(0)
    t.down()
    t.fillcolor(color)
    t.color(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(w - 2 * r)
        t.circle(r, 90)
        t.forward(h - 2 * r)
        t.circle(r, 90)
    t.end_fill()


def draw_ui():
    ui_t.clear()

    ui_t.up()
    ui_t.setpos(0, -290)
    ui_t.color("#94a3b8")
    status_text = f"Глибина: {state['depth']}   |   Розмір: {state['target_size']}   |   Товщина: {state['thickness']}"
    ui_t.write(status_text, align="center", font=("Segoe UI", 12, "bold"))

    for btn in buttons:
        draw_rounded_rect(ui_t, btn["x"], btn["y"], btn["w"], btn["h"], 8, btn["bg"])
        ui_t.up()
        ui_t.setpos(btn["x"], btn["y"] - 6)
        ui_t.color("white")
        ui_t.write(btn["label"], align="center", font=("Segoe UI", 10, "bold"))


# ==========================================
# Логіка GSAP-анімацій (Математичне згладжування)
# ==========================================
def ease_out_cubic(t):
    # Формула плавного уповільнення в кінці анімації (аналог ease: "power3.out" з GSAP)
    return 1 - pow(1 - t, 3)


def draw_scene():
    main_t.clear()

    draw_snowflake(main_t, -300, 240, 90, depth=1, color="#334155", pensize=2)
    draw_snowflake(main_t, 0, 240, 90, depth=2, color="#475569", pensize=2)
    draw_snowflake(main_t, 300, 240, 90, depth=3, color="#64748b", pensize=2)

    main_t.up()
    main_t.setpos(0, 150)
    main_t.color("#475569")
    main_t.write("Еталон складності (Глибина 1, 2, 3)", align="center", font=("Segoe UI", 11, "normal"))

    current_color = state["colors"][state["color_idx"]]
    s = state["current_size"]
    ang = state["angle"]

    if s > 0:
        draw_snowflake(main_t, 0, -40, s, state["depth"], current_color, state["thickness"], rotation=ang)
        draw_snowflake(main_t, 0, -40 + s * 0.57, s, state["depth"], current_color, state["thickness"], rotation=-ang)

    screen.update()


def animate_transition(start_size, end_size, start_angle, end_angle, frames=15):
    # Функція для плавного переходу розміру та кута повороту
    state["is_animating"] = True
    for i in range(1, frames + 1):
        progress = ease_out_cubic(i / frames)  # Застосовуємо математичне згладжування до кадрів
        state["current_size"] = start_size + (end_size - start_size) * progress
        state["angle"] = start_angle + (end_angle - start_angle) * progress
        draw_scene()
        time.sleep(0.01)  # Затримка для відчуття плавності
    state["is_animating"] = False


def animate_intro():
    # Анімація появи фігури (розкручування з розміру 0 до потрібного)
    draw_ui()
    animate_transition(0, state["target_size"], 180, 0, frames=25)


def on_click(x, y):
    if state["is_animating"]:
        return

    for btn in buttons:
        bx, by, bw, bh = btn["x"], btn["y"], btn["w"], btn["h"]
        if bx - bw / 2 <= x <= bx + bw / 2 and by - bh / 2 <= y <= by + bh / 2:
            action = btn["action"]

            old_size = state["target_size"]
            needs_animation = False

            if action == "depth_minus" and state["depth"] > 0:
                state["depth"] -= 1
                # Ефект відскоку (Bounce) як у GSAP при зміні глибини
                animate_transition(old_size * 1.1, old_size, 10, 0, frames=10)
            elif action == "depth_plus" and state["depth"] < 5:
                state["depth"] += 1
                # Ефект відскоку (Bounce) як у GSAP при зміні глибини
                animate_transition(old_size * 0.9, old_size, -10, 0, frames=10)
            elif action == "size_minus" and state["target_size"] > 50:
                state["target_size"] -= 40
                needs_animation = True
            elif action == "size_plus" and state["target_size"] < 350:
                state["target_size"] += 40
                needs_animation = True
            elif action == "pen_minus" and state["thickness"] > 1:
                state["thickness"] -= 1
                draw_scene()
            elif action == "pen_plus" and state["thickness"] < 8:
                state["thickness"] += 1
                draw_scene()
            elif action == "color_next":
                state["color_idx"] = (state["color_idx"] + 1) % len(state["colors"])
                draw_scene()
            elif action == "save":
                filename = f"fractal_{datetime.datetime.now().strftime('%H%M%S')}.eps"
                screen.getcanvas().postscript(file=filename)
                ui_t.up()
                ui_t.setpos(0, -380)
                ui_t.color("#10b981")
                ui_t.write(f"Успіх! Файл {filename} збережено.", align="center", font=("Segoe UI", 11, "bold"))
                return

            draw_ui()

            if needs_animation:
                # Плавне GSAP-подібне масштабування
                animate_transition(old_size, state["target_size"], 0, 0, frames=15)
            break


screen = turtle.Screen()
screen.setup(width=900, height=800)
screen.bgcolor("#0f172a")
screen.title("Преміум Фрактал (Анімація & Інтерфейс)")
screen.tracer(0)

main_t = turtle.Turtle()
main_t.hideturtle()
main_t.speed(0)

ui_t = turtle.Turtle()
ui_t.hideturtle()
ui_t.speed(0)

screen.onscreenclick(on_click)

animate_intro()

turtle.done()
