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

## Dónde nos quedamos (2026-10-30)
**Hecho:**
- Aprendí slicing: `lista[inicio:fin]` (el `fin` no se incluye). `img.shape[:2]` → `(alto, ancho)`.
- En imágenes: `img[filas, columnas]` = `img[y, x]` (y primero, al revés que `cv2.rectangle`).
- `anonymize()`: moví `roi = out[y:y + fh, x:x + fw]` debajo del `max()` (antes usaba `x`, `y` antes de crearlas).
- `face_box()`: borré la línea rota `cv2.rezice(...)`.
- Funciona sin errores al pulsar `8`, pero la cara todavía no sale borrosa.

**2026-10-31:** `anonymize()` terminada y funcionando (tecla `8`). Falta commit + PR + merge.
Siguiente corrección: ruta del modelo con `pathlib`.

**Comandos para retomar mañana** (Terminal de la Mac):
```bash
cd ~/Desktop/proyecto-cv/cv-filters
source venv/bin/activate
git status                 # comprobar que estoy en mi branch, no en main
python filters.py          # probar; pulsar 8 para Anonymize, q para salir
```

**Comandos para guardar al terminar:**
```bash
git add filters.py
git commit -m "Blur faces in anonymize filter"
git push
```
Cuando `anonymize` funcione: abrir PR en GitHub → merge a `main` → marcar la corrección de abajo con [x].

## Correcciones pendientes (revisión del 2026-10-29)
- [x] `anonymize()` está incompleta: no tiene `return` (devuelve `None`). Todo filtro debe devolver una imagen. Cuidado con coordenadas de cara negativas o fuera del borde. (Hecho 2026-10-31: recortar → `GaussianBlur` → pegar con `out[...] = b`.)
- [ ] Ruta del modelo relativa (`"models/..."`): falla si se ejecuta desde otra carpeta. Usar `pathlib.Path(__file__).parent`.
- [ ] Canny: el slider llega a 255 pero el umbral alto está fijo en 200. Limitar el slider o usar `h, h * 2`.
- [ ] Docstring dice teclas `0-6` (falta `7`). En el README, marcar como hecha la tarea de sliders del Nivel 2.
- [x] Fijar versiones en `requirements.txt`. Ya está en main (PR #6) sin versiones; el venv tiene `mediapipe==1.2.0`, `numpy==2.5.4`, `opencv-contrib-python==5.0.0.93`. No instalar `opencv-python` (choca con `opencv-contrib-python`). Usar siempre `python -m pip`.
- [ ] No mergear commits "WIP" a `main`; usar mensajes descriptivos.
- [ ] (Más adelante) `blur`/`edges` leen el slider dentro de la función: pasar los valores como parámetros.
- [ ] (Al final del proyecto) Interfaz más bonita: los sliders de OpenCV (`createTrackbar`) no se pueden personalizar. Opciones: dibujar sliders propios con `cv2` o pasar a una interfaz web (Streamlit/Gradio). Hacerlo después de pasar los valores como parámetros (punto anterior).

Al terminar una corrección, márcala con [x].
