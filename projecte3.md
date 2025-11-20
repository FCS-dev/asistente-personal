# **Ficha Proyecto 3 – Mini asistente personal con IA**

## **Objetivo**

Crear una aplicación tipo asistente personal que registre información diaria, genere recomendaciones básicas con IA y muestre estadísticas gráficas.

## **Instrucciones por partes**

### **Parte 1 – Fundamentos (hasta 75%)**

* **Clases:** `Tarea`, `Nota`, `Evento` o similar
* **Interfaz Tkinter:** registrar tareas, notas y eventos diarios; mostrar listado; botones para añadir/eliminar
* **Persistencia:** CSV o SQLite para almacenar entradas
* **Validación:** campos obligatorios, fechas y horas correctas

### **Parte 2 – Datos y estadísticas (hasta 90%)**

* **Numpy:** calcular estadísticas de tiempo dedicado a tareas, hábitos diarios, horas de sueño, etc.
* **Pandas:** filtrar o agrupar entradas por categoría, día o prioridad
* **Matplotlib:** gráficos de evolución diaria/semanal de tareas completadas, tiempo dedicado o hábitos

### **Parte 3 – Funcionalidades avanzadas (hasta 100%)**

* **IA integrada:**
  * **Resúmenes automáticos:** la IA puede generar un resumen diario o semanal de tareas y notas.
  * **Sugerencias personalizadas:** basadas en los hábitos registrados (ej. sueño, ejercicio, agua) la IA puede dar recomendaciones simples.
  * **Preguntas y respuestas:** el usuario puede hacer preguntas sobre sus datos y la IA analiza la información para responder.
  * **Registro de prompts:** cada consulta debe guardarse en `PROMPTS.md` incluyendo el prompt enviado, el modelo usado y la respuesta recibida.
* **APIs recomendadas:**
  * OpenAI API (GPT-3/4) – [Documentación](https://platform.openai.com/docs/)
  * Hugging Face Transformers – [Documentación](https://huggingface.co/docs/transformers/index)
  * Cohere API – [Documentación](https://docs.cohere.ai/)
* **Exportación a PDF:** resúmenes diarios o semanales con gráficos y estadísticas
* **Seguridad:** almacenamiento seguro de usuarios mediante hash de contraseñas (`hashlib` o `bcrypt`) y verificación al iniciar sesión
* **Opcional:** alertas o recordatorios dentro de la aplicación

### **Entrega final**

* Código completo, modular y organizado
* Archivos de datos o base de datos utilizados
* README.md siguiendo el modelo presentado en clase
* PROMPTS.md con las consultas a IA, modelo usado y respuestas generadas
* Capturas de pantalla de la interfaz y gráficos generados

---



### 📄 Créditos

![1757054093039](img/1756889537400.png)

Última revisión: Noviembre 2025

Este dosier forma parte del curso "Algoritmia y Programación con Python", por Manu Plaza Salas para CIFO Barcelona La Violeta.

Esta obra está bajo una [licencia de Creative Commons Reconeixement-NoComercial-CompartirIgual 4.0 Internacional](http://creativecommons.org/licenses/by-nc-sa/4.0/).
