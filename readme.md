# Mini-asistente Personal

## Stack Utilizado

Lenguaje de programación: Python 3.14
BD: SQLite
Lib. gráfica: Tkinter
Lib. para análisis y gráficos: NumPy, Pandas y Matplotlib

## Descripción

Aplicación para gestionar tareas, eventos y notas rápidas al usuario.
La información se almacena en una B.D. local, se gestiona a traves de una interfaz realizada en tkinder, contiene funciones administrativas; y también se incluyen algunas funciones de muestra con la integración con las librerias de tratamiento de datos.

---

## Requisitos

- Python 3.10 o superior
- Librerías:
  - `tkinter` (desarrollo de interfaz gráfica)
  - `fpdf` (para generar PDF)
  - `json` (para manipular archivos JSON)
  - `numpy` (libreria Py especializada en cálculo numérico)
  - `pandas` (libreria Py para análisis y manipulación de datos)
  - `matplotlib` (libreria Py para generación de gráficos estadísticos)

Instalación de librerias adcionales requeridas:

```bash
pip install fpdf numpy pandas matplotlib
```

SQLite, tkinter y json viene integrado en Python, no requiere instalación adicional.

---

## Uso

1. Ejecutar el archivo principal:

```bash
python main.py
```

2. La ventana principal mostrará:
   * Botones a la izquierda para  **Añadir** , **Editar** y **Borrar** contactos.
   * Listbox a la derecha mostrando los contactos.
3. **Añadir contacto** :

* Pulsa "Añadir Contacto".
* Completa  **Nombre** , **Email** y  **Teléfono** .
* Pulsa "Aceptar" para guardar.

2. **Editar contacto** :

* Selecciona un contacto en el Listbox.
* Pulsa "Editar Contacto".
* Modifica los datos y pulsa "Aceptar".

2. **Borrar contacto** :

* Selecciona un contacto en el Listbox.
* Pulsa "Borrar Contacto".

2. **Exportar a PDF** :

* Selecciona "Archivo → Exportar a PDF".
* Se genera `contacts.pdf` con todos los contactos.

2. **Salir** :

* Selecciona "Archivo → Salir" o cierra la ventana.
* La base de datos se guarda automáticamente.

---

## Diferencias entre versiones

| Característica              | JSON                                  | SQLite                                                         |
| ---------------------------- | ------------------------------------- | -------------------------------------------------------------- |
| Persistencia de datos        | Archivo `contacts.json`             | Base de datos `agenda.db`                                    |
| Estructura de almacenamiento | Lista de diccionarios                 | Tabla SQL `contactos`                                        |
| Escalabilidad                | Limitada, puede corromperse           | Robusta, permite búsquedas y consultas complejas              |
| Dependencia                  | solo Python + fpdf                    | Python + sqlite3 + fpdf                                        |
| Código de acceso a datos    | Lectura/escritura con `json`        | Consultas SQL (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) |
| Ejemplo de iteración        | `for c in self.contacts: c['name']` | `for _, nombre, email, telefono in self.contacts`            |

---

## Estructura de la Base de Datos

SQLite crea un archivo `agenda.db` con la tabla `contactos`:

| id | nombre | email | telefono |
| -- | ------ | ----- | -------- |
| PK | TEXT   | TEXT  | TEXT     |

* `id` es la clave primaria y se autoincrementa.
* `nombre`, `email` y `telefono` son obligatorios.

---

## Explicación del Código

1. **`ContactDialog`**
   * Subclase de `simpledialog.Dialog`.
   * Permite introducir o editar datos de contacto.
   * Devuelve un diccionario con `name`, `email` y `phone`.
2. **`ContactManager`**
   * Clase principal que maneja la interfaz y la base de datos.
   * Métodos principales:
     * `create_table()` → crea la tabla si no existe.
     * `load_contacts()` → carga los contactos desde SQLite.
     * `add_contact()` → añade un contacto.
     * `edit_contact()` → edita un contacto seleccionado.
     * `delete_contact()` → elimina un contacto seleccionado.
     * `update_listbox()` → refresca el Listbox con los contactos.
     * `export_to_pdf()` → genera un PDF con todos los contactos.
     * `on_closing()` → cierra la base de datos y la ventana.
3. **Ejecución principal**
   * Se crea la ventana raíz `Tk()`.
   * Se instancia `ContactManager`.
   * Se ejecuta el bucle principal `root.mainloop()`.

---

## Mejoras Visibles (Propuestas)

* Añadir **mantenimiento de tags (etiquetas)** vía menú "Administrador".
* Generar mas gráficos estadisticos, cuando la la muestra de información sea mayor.
* Incluir campos que podrían ser importantes (hora, imágenes).
* Mejorar el PDF con  **cabecera, tabla y estilos**.
* Exportar a **Excel (xlsx)**.
* Buscar mejor integración con la I.A. para facilitar aún más el uso de la app al usuario.
---

## 📄 Licencia

![1763545883932](image/readme/1763545883932.png)

Última revisión: Noviembre 2025

Desarrollo y maquetación por Franco Calderón Sánchez.

Esta obra está bajo una [licencia de Creative Commons Reconocimiento-NoComercial-CompartirIgual 4.0 Internacional](http://creativecommons.org/licenses/by-nc-sa/4.0/).
