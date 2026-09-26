
from manim import *
from collections import defaultdict

INTEGRANTES = [
    "Aaron Adriano Romano Castro",
    "Bruno William Garcia Lopez",
    "Sebastian Chahuara Galdos"
]

PROYECTO = "Anima tu Estructura de Datos"
SECCION = "Teo. 3 - Lab. 365"


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


class TrieVideo(Scene):

    BLUE = "#4EA5FF"
    CYAN = "#63E6BE"
    YELLOW = "#FFD166"
    RED = "#FF6B6B"
    BG = "#101827"

    def construct(self):

        self.camera.background_color = self.BG

        self.trie = Trie()
        self._last_node_circles = {}

# Presentación:

        self.section_title(
            "TRIE",
            "Árbol de prefijos",
            "CS2023 · Algoritmos y Estructuras de Datos · "
            + SECCION
            + " · "
            + PROYECTO
            + "\nIntegrantes: "
            + ", ".join(INTEGRANTES)
        )

        self.wait_until(15)

# Definición

        self.clear()

        self.section_title(
            "¿Qué es un Trie?",
            "Cada arista representa un carácter."
        )

        bullets = VGroup(
            Text(
                "• Guarda palabras compartiendo prefijos",
                font_size=27
            ),
            Text(
                "• Los nodos finales marcan palabras completas",
                font_size=27
            ),
            Text(
                "• TDA: Diccionario/Conjunto de cadenas",
                font_size=27
            ),
            Text(
                "• Útil para diccionarios y autocompletado",
                font_size=27
            )
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.26
        )

        bullets.move_to(ORIGIN)

        self.play(
            FadeIn(bullets, shift=UP * 0.15),
            run_time=2
        )

        self.wait_until(45)

# Construcción del trie

        self.clear()

        self.section_title(
            "Construimos el Trie",
            'Insertamos: "car", "casa", "caso" y "dog"'
        )

        for word in ["car", "casa", "caso", "dog"]:
            self.trie.insert(word)

        diagram = self.draw_trie(self.trie)

        self.play(
            Create(diagram),
            run_time=5
        )

        note = Text(
            "Las palabras comparten nodos cuando comparten prefijos.",
            font_size=23,
            color=self.CYAN
        )

        note.to_edge(DOWN, buff=0.35)

        self.play(
            FadeIn(note),
            run_time=1
        )

        self.wait_until(85)


# INSERCIÓN


        self.clear()

        self.section_title(
            "Operación: inserción",
            'Insertamos la palabra "cartel"'
        )

        before = self.draw_trie(self.trie)

        self.add(before)

        self.trie.insert("cartel")

        after = self.draw_trie(self.trie)

        self.play(
            Transform(before, after),
            run_time=5
        )

        caption = Text(
            "Se reutiliza c → a → r y se crean t → e → l.",
            font_size=25,
            color=self.YELLOW
        )

        caption.to_edge(DOWN, buff=0.35)

        self.play(
            FadeIn(caption),
            run_time=1
        )

        self.wait_until(120)

# Busqueda

        self.clear()

        self.section_title(
            "Operación: búsqueda",
            'Buscamos "casa" y luego "ca"'
        )

        diagram = self.draw_trie(self.trie)

        circles = self._last_node_circles

        self.play(
            Create(diagram),
            run_time=2
        )

        def highlight_word(word, color):

            keys = []
            prefix = ""

            for ch in word:
                prefix += ch
                keys.append(prefix)

            mobs = [
                circles[k]
                for k in keys
                if k in circles
            ]

            self.play(
                *[
                    c.animate
                    .set_stroke(color=color, width=5)
                    .set_fill(color=color, opacity=0.35)
                    for c, _n in mobs
                ],
                run_time=1.2
            )

            return mobs

        def revert(mobs):

            self.play(
                *[
                    c.animate
                    .set_stroke(
                        color=(self.YELLOW if n.is_end else self.BLUE),
                        width=2.5
                    )
                    .set_fill(
                        color=(self.YELLOW if n.is_end else self.BLUE),
                        opacity=0.18
                    )
                    for c, n in mobs
                ],
                run_time=0.8
            )

# Buscar "casa"

        found = self.trie.search("casa")

        mobs1 = highlight_word(
            "casa",
            self.CYAN
        )

        verdict1 = Text(
            '"casa" → ' +
            ("✓ palabra encontrada" if found else "✗ no encontrada"),
            font_size=28,
            color=self.CYAN
        )

        verdict1.to_edge(DOWN, buff=0.35)

        self.play(
            FadeIn(verdict1),
            run_time=0.8
        )

        self.wait(1)

        self.play(
            FadeOut(verdict1)
        )

        revert(mobs1)

# Buscar "ca"

        prefix_only = self.trie.search("ca")

        mobs2 = highlight_word(
            "ca",
            self.YELLOW
        )

        verdict2 = Text(
            '"ca" → ' +
            ("✓ palabra completa" if prefix_only else "✗ solo es prefijo"),
            font_size=28,
            color=self.YELLOW
        )

        verdict2.to_edge(DOWN, buff=0.35)

        self.play(
            FadeIn(verdict2),
            run_time=0.8
        )

        self.wait(1)

        self.wait_until(150)

#Eliminación

        self.clear()

        self.section_title(
            "Operación: eliminación",
            'Eliminamos "cartel"'
        )

        before = self.draw_trie(self.trie)

        before_circles = self._last_node_circles

        self.add(before)

        self.trie.delete("cartel")

        after = self.draw_trie(self.trie)

        after_keys = set(
            self._last_node_circles.keys()
        )

        removed_keys = (
            set(before_circles.keys())
            - after_keys
        )

        if removed_keys:

            self.play(
                *[
                    before_circles[k][0]
                    .animate
                    .set_stroke(
                        color=self.RED,
                        width=5
                    )
                    .set_fill(
                        color=self.RED,
                        opacity=0.35
                    )
                    for k in removed_keys
                ],
                run_time=1.2
            )

            self.wait(0.5)

        self.play(
            Transform(before, after),
            run_time=4
        )

        caption = Text(
            "Se borran solo los nodos que ya no sirven a otra palabra.",
            font_size=23,
            color=self.YELLOW
        )

        caption.to_edge(DOWN, buff=0.35)

        self.play(
            FadeIn(caption),
            run_time=1
        )

        self.wait_until(180)

#Caso borde

        self.clear()

        self.section_title(
            "Caso borde: Trie vacío",
            "¿Qué pasa si buscamos una palabra?"
        )

        empty_trie = Trie()

        result = empty_trie.search("hola")

        root = Circle(
            radius=0.38,
            color=self.BLUE,
            fill_opacity=0.15
        )

        root_label = Text(
            "raíz",
            font_size=22
        )

        root_label.next_to(
            root,
            DOWN,
            buff=0.18
        )

        status = Text(
            "Buscar “hola” → "
            + ("encontrada" if result else "no encontrada"),
            font_size=30,
            color=self.RED
        )

        root_group = VGroup(
            root,
            root_label
        )

        root_group.move_to(
            ORIGIN + UP * 0.4
        )

        status.next_to(
            root_label,
            DOWN,
            buff=0.6
        )

        self.play(
            Create(root),
            FadeIn(root_label),
            run_time=2
        )

        self.play(
            Write(status),
            run_time=2
        )

        self.wait_until(205)

#Complejidad

        self.clear()

        self.section_title(
            "Complejidad temporal",
            "L = cantidad de caracteres de la palabra"
        )

        rows = VGroup(
            Text(
                "Inserción       O(L)",
                font_size=32
            ),
            Text(
                "Búsqueda        O(L)",
                font_size=32
            ),
            Text(
                "Eliminación     O(L)",
                font_size=32
            )
        ).arrange(
            DOWN,
            aligned_edge=LEFT,
            buff=0.45
        )

        rows.move_to(ORIGIN)

        self.play(
            LaggedStart(
                *[
                    FadeIn(
                        r,
                        shift=RIGHT * 0.2
                    )
                    for r in rows
                ],
                lag_ratio=0.25
            ),
            run_time=3
        )

        self.wait_until(225)

# Aplicaciones y cierre

        self.clear()

        self.section_title(
            "¿Dónde se usa?",
            "Autocompletado · Diccionarios · Correctores"
        )

        ending = Text(
            "El Trie organiza palabras por prefijos\n¡Gracias!",
            font_size=34,
            line_spacing=1.2,
            color=self.CYAN
        )

        ending.move_to(
            UP * 0.3
        )

        credits = Text(
            PROYECTO
            + "\n"
            + ", ".join(INTEGRANTES),
            font_size=18,
            color=GRAY_B,
            line_spacing=1.2
        )

        credits.next_to(
            ending,
            DOWN,
            buff=0.6
        )

        credits.align_to(
            ending,
            LEFT
        )

        self.play(
            FadeIn(
                ending,
                scale=0.95
            ),
            run_time=2
        )

        self.play(
            FadeIn(credits),
            run_time=1
        )

        self.wait_until(240)


    def section_title(
        self,
        title,
        subtitle="",
        footer=""
    ):

        heading = Text(
            title,
            font_size=42,
            weight=BOLD,
            color=self.BLUE
        )

        heading.to_edge(
            UP,
            buff=0.45
        )

        self.play(
            Write(heading),
            run_time=1.2
        )

        if subtitle:

            sub = Text(
                subtitle,
                font_size=25,
                color=WHITE
            )

            sub.next_to(
                heading,
                DOWN,
                buff=0.25
            )

            self.play(
                FadeIn(sub),
                run_time=0.8
            )

        if footer:

            foot = Text(
                footer,
                font_size=16,
                color=GRAY_B,
                line_spacing=1.15
            )

            foot.to_edge(
                DOWN,
                buff=0.2
            )

            self.play(
                FadeIn(foot),
                run_time=0.5
            )


    def wait_until(self, target):

        remaining = target - self.time

        if remaining > 0:
            self.wait(remaining)


    def draw_trie(self, trie):

        nodes = []
        edges = []

        positions = {}
        circles = {}

        levels = defaultdict(list)

        def collect(
            node,
            prefix,
            depth
        ):

            key = (
                prefix
                if prefix
                else "ROOT"
            )

            levels[depth].append(
                (key, node)
            )

            for char, child in sorted(
                node.children.items()
            ):

                collect(
                    child,
                    prefix + char,
                    depth + 1
                )

        collect(
            trie.root,
            "",
            0
        )

        max_depth = (
            max(levels.keys())
            if levels
            else 0
        )

        for depth, items in levels.items():

            count = len(items)

            for index, (key, node) in enumerate(items):

                x = (
                    index
                    - (count - 1) / 2
                ) * min(
                    1.15,
                    7.5 / max(count, 1)
                )

                y = (
                    2.0
                    - depth * 0.82
                )

                positions[key] = np.array(
                    [x, y, 0]
                )

        for depth, items in levels.items():

            for key, node in items:

                if key == "ROOT":
                    label = "raíz"
                else:
                    label = key[-1]

                color = (
                    self.YELLOW
                    if node.is_end
                    else self.BLUE
                )

                circle = Circle(
                    radius=0.25,
                    stroke_color=color,
                    stroke_width=2.5,
                    fill_color=color,
                    fill_opacity=0.18
                )

                circle.move_to(
                    positions[key]
                )

                txt = Text(
                    label,
                    font_size=20,
                    color=WHITE
                )

                txt.move_to(
                    circle.get_center()
                )

                nodes.extend(
                    [
                        circle,
                        txt
                    ]
                )

                circles[key] = (
                    circle,
                    node
                )

                if key != "ROOT":

                    parent = (
                        key[:-1]
                        if len(key) > 1
                        else "ROOT"
                    )

                    line = Line(
                        positions[parent],
                        positions[key],
                        color=GRAY_B,
                        stroke_width=2
                    )

                    line.set_z_index(-1)

                    edges.append(line)

        self._last_node_circles = circles

        return VGroup(
            *edges,
            *nodes
        ).scale(
            0.88
        ).shift(
            DOWN * 0.2
        )

