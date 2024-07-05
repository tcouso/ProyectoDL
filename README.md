
---

# Evaluación de conocimientos de LLMs en historia y cultura latinoamericana


## Configuración

1. **Instalación de Dependencias**

   Antes de ejecutar el proyecto, asegúrate de tener todas las dependencias instaladas:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configuración de Variables de Entorno**

   Crea un archivo `.env` en el directorio raíz del proyecto y define tu clave de API de Groq:

   ```plaintext
   GROQ_API_KEY=your_api_key_here
   ```

3. **Configuración YAML**

   Asegúrate de tener un archivo `config.yaml` configurado como sigue:

   ```yaml
   base_prompt: "Responde la siguiente pregunta, exclusivamente con la letra de la respuesta que elijas. No agregues ninguna explicación."
    models:
      - "llama3-8b-8192"
      - "mixtral-8x7b-32768"
      - "gemma-7b-it"
    test_instruments:
      - name: colombia
        filename: "data/pruebas_mmlu/colombia_mmle.json"
   ```

   Donde:
   - `base_prompt`: Prompt base para cada pregunta.
   - `models`: Lista de modelos disponibles para consultar.
   - `test_instruments`: Lista de instrumentos de prueba, cada uno con un nombre y un archivo JSON asociado.

## Uso

Para ejecutar la consulta de modelos, usa el script principal `query_models.py`:

```bash
python query_models.py
```

Este script carga la configuración desde `config.yaml`, consulta cada modelo con los instrumentos de prueba definidos y guarda los resultados en el directorio `results`.

## Resultados

Los resultados de cada consulta se guardan en archivos JSON dentro del directorio `results`. Cada archivo contiene los resultados de un modelo específico y sus correspondientes instrumentos de prueba.

---

Ajusta este `README.md` según las especificaciones exactas de tu proyecto y cualquier otro detalle relevante que desees incluir.