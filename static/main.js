// static/js/main.js
// Aquí puedes añadir interactividad extra si lo deseas.
// Ejemplo: confirmación antes de eliminar
document.addEventListener("DOMContentLoaded", () => {
    const forms = document.querySelectorAll("form[action*='eliminar']");
    forms.forEach(f => {
      f.addEventListener("submit", (e) => {
        if (!confirm("¿Está seguro de eliminar este producto?")) {
          e.preventDefault();
        }
      });
    });
  });
  