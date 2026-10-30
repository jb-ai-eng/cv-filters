# Contexto para Claude

## Sobre mí
- Estoy aprendiendo Python (mi primer lenguaje) y computer vision. La sintaxis todavía me cuesta.
- Aprendo haciendo, no con videos. Meta: carrera en CV/IA y un proyecto bueno para mi portafolio.
- Siguiente proyecto después de este: detección de objetos (carros, señales de tránsito) y entrenar modelos.

## Cómo quiero que me ayudes
- Explicaciones e indicaciones en español; el código (nombres, comentarios, commits) y los términos técnicos en inglés (branch, commit, function, array...). La primera vez que aparezca un término, defínelo en español.
- Explícame qué está mal y **por qué**, y qué errores estoy cometiendo. Sé realista y directo.
- Dame pistas o fragmentos pequeños para que yo escriba la solución; código completo solo si lo pido.
- Explica la sintaxis de Python cuando aparezca algo nuevo.
- Aprendo repitiendo: guíame paso a paso, un paso a la vez, define cada término nuevo y espera mi resultado antes de seguir.

## Cómo uso las ventanas
- **VS Code (Claude Code):** aquí escribo código; Claude revisa y guía los pasos del proyecto.
- **Claude Desktop:** preguntas generales (conceptos, sintaxis, carrera). No edita archivos del proyecto.
- Comandos: `/siguiente` (próximo paso guiado), `/revisa` (revisar mi código), `/explica <tema>` (concepto + ejercicio).

## Rutina para empezar a trabajar
El proyecto está en `~/Desktop/proyecto-cv/cv-filters` (antes `cv-filtros`). GitHub: `jb-ai-eng/cv-filters`.
1. VS Code: File → Open Folder → `cv-filters`. Panel de Claude → historial para retomar el chat.
2. Terminal de la Mac:
   ```bash
   cd ~/Desktop/proyecto-cv/cv-filters
   source venv/bin/activate
   git status
   ```
3. Para trabajar: `git switch -c <branch>` → editar → `git add <archivo>` → `git commit -m "..."` → `git push` → PR en GitHub → merge.

## Norte del proyecto (decidido 2026-10-31)
Convertir la app de filtros en una **herramienta de privacidad para video**: anonimizar caras (y más adelante placas de carros) en webcam y archivos de video. Problema real: GDPR/leyes de privacidad, periodistas, cámaras de calle, videos de menores. Los filtros actuales se quedan como "modo demo". Meta: algo que un reclutador pueda probar con un enlace. Mejor pocas cosas bien terminadas que muchas a medias.

## Roadmap (en orden; una branch + PR por fase)
- [ ] **Fase 1 — Base limpia:** terminar las "Correcciones pendientes" pequeñas (`pathlib`, Canny, docstring).
- [ ] **Fase 2 — Webcam externa:** elegir cámara al ejecutar (`python filters.py --camera 1`) con `argparse`.
- [ ] **Fase 3 — Dos computadoras:** subir `.claude/` a git; instalar en Windows Git, Python, VS Code y Claude Code; venv en PowerShell (`venv\Scripts\Activate.ps1`). Regla: `git pull` al empezar, `git push` al terminar.
- [ ] **Fase 4 — Privacy tool:** procesar archivos de video completos y guardar el resultado; elegir método (blur / pixelate / black box).
- [ ] **Fase 5 — README con GIF demo** (primera versión; actualizar al final).
- [ ] **Fase 6 — Refactor:** filtros reciben sus valores como parámetros (no leen sliders dentro).
- [ ] **Fase 7 — App web:** Gradio + publicar gratis en Hugging Face Spaces (funciona también en el navegador del teléfono). Aquí se resuelve la "barra bonita".
- [ ] **Fase 8 (opcional) — Placas de carros:** puente al siguiente proyecto (detección de carros/señales).

## Dónde nos quedamos
**2026-10-31:** `anonymize()` terminada y mergeada (PR #8). Empezando **Fase 1**: corrección de `pathlib`.

**Lo que ya aprendí:**
- Slicing: `lista[inicio:fin]` (el `fin` no se incluye). `img.shape[:2]` → `(alto, ancho)`.
- En imágenes: `img[filas, columnas]` = `img[y, x]` (y primero, al revés que `cv2.rectangle`).
- Slicing para escribir: `out[y:y + fh, x:x + fw] = b` pega `b` en ese hueco.
- `=` calcula la derecha primero y la guarda en la izquierda. Python lee de arriba a abajo: crear una variable antes de usarla (error que repito).
- Flujo git: branch → commit → `git push --set-upstream origin <branch>` (1ª vez) → PR → merge → `git switch main` + `git pull`.

## Correcciones pendientes (revisión del 2026-10-29)
- [x] `anonymize()` está incompleta: no tiene `return` (devuelve `None`). Todo filtro debe devolver una imagen. Cuidado con coordenadas de cara negativas o fuera del borde. (Hecho 2026-10-31: recortar → `GaussianBlur` → pegar con `out[...] = b`.)
- [x] Ruta del modelo relativa (`"models/..."`): falla si se ejecuta desde otra carpeta. Usar `pathlib.Path(__file__).parent`. (Hecho 2026-10-31: `MODEL_PATH` + `str(MODEL_PATH)`.)
- [x] Canny: el slider llega a 255 pero el umbral alto está fijo en 200. Limitar el slider o usar `h, h * 2`. (Hecho 2026-10-31: `cv2.Canny(g, h, h * 2)`.)
- [ ] Docstring dice teclas `0-6` (falta `7`). En el README, marcar como hecha la tarea de sliders del Nivel 2.
- [x] Fijar versiones en `requirements.txt`. Ya está en main (PR #6) sin versiones; el venv tiene `mediapipe==1.2.0`, `numpy==2.5.4`, `opencv-contrib-python==5.0.0.93`. No instalar `opencv-python` (choca con `opencv-contrib-python`). Usar siempre `python -m pip`.
- [ ] No mergear commits "WIP" a `main`; usar mensajes descriptivos.
- [ ] (Más adelante) `blur`/`edges` leen el slider dentro de la función: pasar los valores como parámetros.
- [ ] (Fase 7) Interfaz más bonita: los sliders de OpenCV (`createTrackbar`) no se pueden personalizar → se resuelve con la app web de Gradio.

Al terminar una corrección, márcala con [x].
