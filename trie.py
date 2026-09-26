from manim import *
from collections import defaultdict

INTEGRANTES = ["Aaron Adriano Romano Castro", "Bruno William Garcia Lopez", "Sebastian Chahuara Galdos"]
PROYECTO = "Anima tu Estructura de Datos"
SECCION = "Teo. 3 - Lab. 365"


def mc_text(content, **kwargs):
    return Text(content, **kwargs)

def mc_text_centered(content, buff=0.12, **kwargs):
    lines = VGroup(*[Text(line, **kwargs) for line in content.split("\n")])
    lines.arrange(DOWN, buff=buff)
    return lines

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def delete(self, word):
        if not self.search(word):
            return False

        def remove(node, i):
            if i == len(word):
                node.is_end = False
                return len(node.children) == 0
            char = word[i]
            should_prune = remove(node.children[char], i + 1)
            if should_prune:
                del node.children[char]
            return (not node.is_end) and len(node.children) == 0

        remove(self.root, 0)
        return True


class TrieVideo(Scene)
    BLUE = "#3AA0FF"
    CYAN = "#39FFDF"
    YELLOW = "#FFD23F"
    RED = "#FF3B5C"      
    PURPLE = "#8C6BFF"   
    BG = "#03040A"

    def construct(self):
        self.camera.background_color = self.BG
        self.trie = Trie()
        self._last_node_circles = {}

        self.intro_slide()
        self.wait_until(15)

        self.new_scene()
        self.section_title("¿QUÉ ES UN TRIE?", "Cada arista representa un carácter")
        bullets = VGroup(
            mc_text("> Guarda palabras compartiendo prefijos", font_size=26),
            mc_text("> Los nodos finales marcan palabras completas", font_size=26),
            mc_text("> TDA: Diccionario / Conjunto de cadenas", font_size=26),
            mc_text("  (insertar, buscar, eliminar)", font_size=22, color=GRAY_B),
            mc_text("> Util para diccionarios y autocompletado", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(ORIGIN)
        for b in bullets:
            b.set_color(WHITE)
        bullets[0].set_color(self.CYAN)
        bullets[1].set_color(self.CYAN)
        bullets[2].set_color(self.YELLOW)
        bullets[4].set_color(self.CYAN)
        self.play(FadeIn(bullets, shift=UP * 0.15), run_time=2)
        self.wait_until(45)

        self.new_scene()
        self.section_title("CONSTRUIMOS EL TRIE", 'Insertamos: "car", "casa", "caso" y "dog"')
        for word in ["car", "casa", "caso", "dog"]:
            self.trie.insert(word)
        diagram = self.draw_trie(self.trie)
        self.play(Create(diagram), run_time=5)
        note = mc_text("Las palabras comparten nodos cuando comparten prefijos.",
                       font_size=22, color=self.CYAN)
        note.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(note), run_time=1)
        self.wait_until(85)

        self.new_scene()
        self.section_title("OPERACION: INSERCION", 'Insertamos la palabra "cartel"')
        before = self.draw_trie(self.trie)
        self.add(before)
        self.trie.insert("cartel")
        after = self.draw_trie(self.trie)
        self.play(Transform(before, after), run_time=5)
        caption = mc_text("Se reutiliza c -> a -> r y se crean t -> e -> l.",
                          font_size=24, color=self.YELLOW)
        caption.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(caption), run_time=1)
        self.wait_until(120)

        self.new_scene()
        self.section_title("OPERACION: BUSQUEDA", 'Buscamos "casa" y luego "ca"')
        diagram = self.draw_trie(self.trie)
        circles = self._last_node_circles  # key -> (circle, node)
        self.play(Create(diagram), run_time=2)

        def highlight_word(word, color):
            keys, prefix = [], ""
            for ch in word:
                prefix += ch
                keys.append(prefix)
            mobs = [circles[k] for k in keys if k in circles]
            self.play(
                *[c.animate.set_stroke(color=color, width=5).set_fill(color=color, opacity=0.35)
                  for c, _n in mobs],
                run_time=1.2,
            )
            return mobs

        def revert(mobs):
            self.play(
                *[c.animate.set_stroke(color=(self.YELLOW if n.is_end else self.BLUE), width=2.5)
                  .set_fill(color=(self.YELLOW if n.is_end else self.BLUE), opacity=0.18)
                  for c, n in mobs],
                run_time=0.8,
                  )

        found = self.trie.search("casa")
        mobs1 = highlight_word("casa", self.CYAN)
        verdict1 = mc_text('"casa" -> ' + ("[OK] palabra encontrada" if found else "[X] no encontrada"),
                           font_size=27, color=self.CYAN)
        verdict1.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(verdict1), run_time=0.8)
        self.wait(1)
        self.play(FadeOut(verdict1))
        revert(mobs1)

        prefix_only = self.trie.search("ca")
        mobs2 = highlight_word("ca", self.YELLOW)
        verdict2 = mc_text('"ca" -> ' + ("[OK] palabra completa" if prefix_only else "[X] solo es prefijo"),
                           font_size=27, color=self.YELLOW)
        verdict2.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(verdict2), run_time=0.8)
        self.wait(1)
        self.wait_until(150)

        self.new_scene()
        self.section_title("OPERACION: ELIMINACION", 'Eliminamos "cartel"')
        before = self.draw_trie(self.trie)
        before_circles = self._last_node_circles
        self.add(before)
        self.trie.delete("cartel")
        after = self.draw_trie(self.trie)
        after_keys = set(self._last_node_circles.keys())
        removed_keys = set(before_circles.keys()) - after_keys
        if removed_keys:
            self.play(
                *[before_circles[k][0].animate.set_stroke(color=self.RED, width=5)
                  .set_fill(color=self.RED, opacity=0.35)
                  for k in removed_keys],
                run_time=1.2,
                  )
            self.wait(0.5)
        self.play(Transform(before, after), run_time=4)
        caption = mc_text("Se borran solo los nodos que ya no sirven a otra palabra.",
                          font_size=22, color=self.YELLOW)
        caption.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(caption), run_time=1)
        self.wait_until(180)

        self.new_scene()
        self.section_title("CASO BORDE: TRIE VACIO", "Que pasa si buscamos una palabra?")
        empty_trie = Trie()
        result = empty_trie.search("hola")
        root = Circle(radius=0.38, color=self.BLUE, fill_opacity=0.15)
        root_label = mc_text("raiz", font_size=22, color=WHITE).next_to(root, DOWN, buff=0.18)
        status = mc_text('Buscar "hola" -> ' + ("encontrada" if result else "no encontrada"),
                         font_size=30, color=self.RED)
        VGroup(root, root_label).move_to(UP * 0.4)
        status.next_to(root_label, DOWN, buff=0.6)
        self.play(Create(root), FadeIn(root_label), run_time=2)
        self.play(Write(status), run_time=2)
        self.wait_until(205)

        self.new_scene()
        self.section_title("COMPLEJIDAD TEMPORAL", "L = cantidad de caracteres de la palabra")
        rows = VGroup(
            mc_text("Insercion       O(L)", font_size=32, color=self.BLUE),
            mc_text("Busqueda        O(L)", font_size=32, color=self.CYAN),
            mc_text("Eliminacion     O(L)", font_size=32, color=self.RED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        rows.move_to(ORIGIN)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.25), run_time=3)
        self.wait_until(225)

        self.new_scene()
        self.section_title("DONDE SE USA?", "Autocompletado - Diccionarios - Correctores")
        ending = mc_text_centered("El Trie organiza palabras por prefijos\nGracias!", font_size=32, color=self.CYAN)
        ending.move_to(UP * 0.3)
        credits = mc_text_centered(PROYECTO + "\n" + ", ".join(INTEGRANTES), font_size=17, color=GRAY_B)
        credits.next_to(ending, DOWN, buff=0.6)
        self.play(FadeIn(ending, scale=0.95), run_time=2)
        self.play(FadeIn(credits), run_time=1)
        self.wait_until(240)

    def hud(self):
        """Grid sutil + esquinas estilo HUD para el look futurista."""
        w, h = config.frame_width, config.frame_height
        grid = VGroup()
        for x in np.linspace(-w / 2, w / 2, 9)[1:-1]:
            grid.add(Line([x, -h / 2, 0], [x, h / 2, 0], stroke_width=0.5))
        for y in np.linspace(-h / 2, h / 2, 6)[1:-1]:
            grid.add(Line([-w / 2, y, 0], [w / 2, y, 0], stroke_width=0.5))
        grid.set_stroke(color=self.BLUE, opacity=0.06)

        corner_len = 0.55
        margin = 0.35
        corners = VGroup()
        for cx, cy, dx, dy in [
            (-w / 2 + margin, h / 2 - margin, 1, -1),
            (w / 2 - margin, h / 2 - margin, -1, -1),
            (-w / 2 + margin, -h / 2 + margin, 1, 1),
            (w / 2 - margin, -h / 2 + margin, -1, 1),
        ]:
            bracket = VGroup(
                Line([cx, cy, 0], [cx + dx * corner_len, cy, 0]),
                Line([cx, cy, 0], [cx, cy + dy * corner_len, 0]),
            )
            corners.add(bracket)
        corners.set_stroke(color=self.PURPLE, width=2, opacity=0.5)

        return VGroup(grid, corners)

    def new_scene(self):
        """Limpia la escena y vuelve a poner el fondo/HUD futurista."""
        self.clear()
        self.add(self.hud())

    def intro_slide(self):
        self.add(self.hud())

        glow = mc_text("TRIE", font_size=96, weight=BOLD, color=self.PURPLE)
        glow.set_opacity(0.35).scale(1.06)
        title = mc_text("TRIE", font_size=96, weight=BOLD, color=self.CYAN)
        title_group = VGroup(glow, title)

        accent = Line(LEFT * 2.2, RIGHT * 2.2, color=self.BLUE, stroke_width=3)
        subtitle = mc_text("Arbol de prefijos", font_size=28, color=WHITE)

        header = VGroup(title_group, accent, subtitle).arrange(DOWN, buff=0.35).move_to(UP * 0.6)

        course = mc_text(
            "CS2023 - Algoritmos y Estructuras de Datos - " + SECCION,
            font_size=18, color=GRAY_B,
            )
        proyecto = mc_text("Proyecto: " + PROYECTO, font_size=18, color=self.YELLOW)
        separator = Line(LEFT * 3, RIGHT * 3, color=self.PURPLE, stroke_width=1).set_opacity(0.5)
        integrantes = mc_text_centered("\n".join(INTEGRANTES), font_size=17, color=WHITE)
        footer = VGroup(course, proyecto, separator, integrantes).arrange(DOWN, buff=0.22)
        footer.move_to(DOWN * 2.1)

        self.play(FadeIn(glow, scale=1.1), Write(title), run_time=1.4)
        self.play(Create(accent), FadeIn(subtitle), run_time=1.0)
        self.play(FadeIn(footer, shift=UP * 0.1), run_time=1.0)

    def section_title(self, title, subtitle=""):
        heading = mc_text(title, font_size=40, weight=BOLD, color=self.CYAN)
        heading.to_edge(UP, buff=0.5)
        accent = Line(
            heading.get_left() + DOWN * 0.18,
            heading.get_right() + DOWN * 0.18,
            color=self.PURPLE, stroke_width=2.5,
            )
        self.play(Write(heading), Create(accent), run_time=1.1)
        if subtitle:
            sub = mc_text(subtitle, font_size=23, color=WHITE)
            sub.next_to(accent, DOWN, buff=0.28)
            self.play(FadeIn(sub), run_time=0.7)

    def wait_until(self, target):
        # Completa cada bloque hasta su marca temporal, para que la escena dure 4:00.
        remaining = target - self.time
        if remaining > 0:
            self.wait(remaining)

    def draw_trie(self, trie):
        # Dibuja la estructura recorriendo el Trie real y guarda una referencia
        # circle/nodo por prefijo para poder resaltar caminos (busqueda/eliminacion).
        nodes = []
        edges = []
        positions = {}
        circles = {}
        levels = defaultdict(list)

        def collect(node, prefix, depth):
            key = prefix if prefix else "ROOT"
            levels[depth].append((key, node))
            for char, child in sorted(node.children.items()):
                collect(child, prefix + char, depth + 1)

        collect(trie.root, "", 0)
        max_depth = max(levels.keys()) if levels else 0
        for depth, items in levels.items():
            count = len(items)
            for index, (key, node) in enumerate(items):
                x = (index - (count - 1) / 2) * min(1.15, 7.5 / max(count, 1))
                y = 1.9 - depth * 0.8
                positions[key] = np.array([x, y, 0])

        for depth, items in levels.items():
            for key, node in items:
                if key == "ROOT":
                    label = "raiz"
                else:
                    label = key[-1]
                color = self.YELLOW if node.is_end else self.BLUE
                circle = Circle(radius=0.25, stroke_color=color, stroke_width=2.5,
                                fill_color=color, fill_opacity=0.18).move_to(positions[key])
                txt = mc_text(label, font_size=20, color=WHITE).move_to(circle.get_center())
                nodes.extend([circle, txt])
                circles[key] = (circle, node)
                if key != "ROOT":
                    parent = key[:-1] if len(key) > 1 else "ROOT"
                    line = Line(positions[parent], positions[key], color=self.PURPLE, stroke_width=2)
                    line.set_stroke(opacity=0.6)
                    line.set_z_index(-1)
                    edges.append(line)
        self._last_node_circles = circles
        return VGroup(*edges, *nodes).scale(0.85).shift(DOWN * 0.35)
