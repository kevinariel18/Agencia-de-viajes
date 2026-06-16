# Design Thinking — TourPack Manager

## 1. ¿Qué es Design Thinking?

Design Thinking es una metodología de resolución de problemas centrada en el ser humano. Se basa en comprender profundamente a los usuarios, cuestionar supuestos y redefinir problemas para generar soluciones innovadoras que se prueban de forma iterativa.

## 2. Fundamentos

- **Empatía**: comprender las necesidades reales del usuario.
- **Colaboración**: trabajo multidisciplinario.
- **Experimentación**: prototipar antes de construir.
- **Iteración**: mejorar continuamente con retroalimentación.

## 3. Enfoque centrado en el usuario

Cada decisión de diseño parte de preguntas como: ¿Qué necesita el usuario? ¿Qué frustraciones tiene? ¿Qué tareas quiere completar más rápido?

## 4. Empatía

Se busca entender el contexto emocional y funcional del usuario, no solo sus requisitos técnicos. Herramientas: entrevistas, observación directa, mapa de empatía.

## 5. Colaboración

Equipos mixtos (diseñadores, desarrolladores, usuarios) participan en el proceso de ideación para evitar soluciones sesgadas.

## 6. Experimentación

Se construyen prototipos de baja fidelidad antes del código. Esto reduce el costo del error.

## 7. Iteración

Las soluciones se refinan con base en pruebas reales con usuarios. Cada ciclo mejora el producto.

---

## 8. Etapas del Design Thinking

### Empatizar
Investigar a los usuarios actuales de agencias de viajes. Se realizaron entrevistas con administradores de agencias pequeñas y clientes frecuentes de paquetes turísticos.

**Hallazgos:**
- Los administradores usan Excel para gestionar reservas.
- No saben en tiempo real cuántos cupos quedan.
- Los clientes abandonan el proceso porque no ven fechas disponibles claramente.

### Definir
A partir de la investigación se definió el problema central y las necesidades de cada actor.

### Idear
Se generaron ideas para digitalizar el flujo completo: catálogo → selección → reserva → confirmación.

### Prototipar
Se crearon wireframes de las pantallas clave: catálogo de paquetes, detalle de paquete, formulario de reserva, dashboard del admin.

### Evaluar
Los prototipos se validaron con usuarios reales. Se ajustó el flujo de reserva para reducirlo a 3 pasos y se simplificó el dashboard.

---

## 9. Descubrimiento de usuarios

Se identificaron dos tipos principales de usuarios con necesidades distintas.

## 10. Técnicas de descubrimiento

### Entrevistas
Se realizaron entrevistas semiestructuradas con 3 administradores de agencias turísticas y 5 clientes frecuentes.

### Encuestas
Formulario digital con 15 preguntas sobre experiencia actual al reservar paquetes turísticos.

### Observación
Se observó el proceso manual de una agencia: llamadas telefónicas, Excel compartido, confirmaciones por WhatsApp.

### Mapa de empatía
Para cada persona de usuario se construyó un mapa con: qué piensa, qué siente, qué dice, qué hace, dolores y ganancias.

### Persona de usuario
Fichas detalladas de cada arquetipo representativo.

### Mapa del recorrido (Customer Journey)
Se mapeó el camino del cliente desde que descubre un paquete hasta que recibe la confirmación de reserva.

---

## 11. Problema identificado

Las agencias turísticas pequeñas y medianas no tienen un sistema centralizado para gestionar paquetes, cupos y reservas. Esto genera pérdidas de ventas, errores de overbooking y experiencias de cliente deficientes.

---

## 12. Necesidades del administrador

- Ver en tiempo real el estado de cupos por fecha de salida.
- Crear y editar paquetes sin depender de un técnico.
- Confirmar o cancelar reservas fácilmente.
- Acceder a reportes de ingresos y ocupación.
- Recibir alertas cuando una fecha está casi llena.

## 13. Necesidades del cliente

- Explorar paquetes con filtros claros (precio, duración, destino).
- Ver fechas disponibles sin tener que llamar a la agencia.
- Reservar en pocos pasos desde cualquier dispositivo.
- Recibir confirmación inmediata con código de reserva.
- Consultar el historial de sus reservas en cualquier momento.

## 14. Puntos de dolor

**Administrador:**
- Datos dispersos en múltiples hojas de cálculo.
- Riesgo constante de overbooking por falta de sincronización.
- Tiempo excesivo en tareas administrativas manuales.

**Cliente:**
- Incertidumbre sobre disponibilidad real.
- Proceso de reserva largo y con intermediarios.
- Falta de transparencia en precios y fechas.

---

## 15. Personas de usuario

### Persona 1 — Administrador de agencia turística

**Nombre:** Roberto Vega  
**Edad:** 42 años  
**Cargo:** Gerente de operaciones, Agencia "Mundo Viajes"  
**Contexto:** Lleva 10 años en el sector turístico. Gestiona todo en Excel compartido con 3 asistentes.  

**Objetivos:**
- Conocer en tiempo real los cupos disponibles.
- Gestionar reservas sin errores de duplicación.
- Ver reportes de ingresos mensuales rápidamente.

**Frustraciones:**
- "Perdemos ventas porque no sabemos cuántos cupos reales tenemos."
- "Confirmar una reserva me toma 30 minutos entre correos y actualizar el Excel."
- "No tengo visibilidad de qué paquetes son los más vendidos."

**Comportamiento digital:** Usa laptop, correo electrónico y WhatsApp Business. Maneja bien Excel pero no sabe programar.

---

### Persona 2 — Cliente viajero

**Nombre:** Camila Rondón  
**Edad:** 29 años  
**Ocupación:** Diseñadora gráfica independiente  
**Contexto:** Viaja 2-3 veces al año. Prefiere paquetes que incluyan todo.

**Objetivos:**
- Comparar paquetes por precio y destino en un solo lugar.
- Reservar desde el celular en menos de 10 minutos.
- Tener un comprobante digital de su reserva.

**Frustraciones:**
- "Las páginas de agencias son confusas y no muestran precios claros."
- "No sé si hay cupo hasta que me llaman al día siguiente."
- "Quiero pagar y confirmar en el momento, no esperar."

**Comportamiento digital:** Muy activa en redes sociales. Usa principalmente el celular para buscar y reservar viajes.

---

## 16. Declaración del problema

*"Los administradores de agencias turísticas necesitan una plataforma centralizada para gestionar paquetes, cupos y reservas en tiempo real, mientras que los clientes necesitan un catálogo claro donde puedan descubrir, comparar y reservar paquetes turísticos de forma autónoma y rápida."*

---

## 17. Preguntas "¿Cómo podríamos...?"

1. ¿Cómo podríamos mostrar los cupos disponibles en tiempo real sin overbooking?
2. ¿Cómo podríamos reducir el proceso de reserva a menos de 5 pasos?
3. ¿Cómo podríamos ayudar al administrador a identificar los paquetes más populares?
4. ¿Cómo podríamos hacer que el cliente confíe en la disponibilidad mostrada?
5. ¿Cómo podríamos permitir cancelaciones sin procesos burocráticos?

---

## 18. Ideas de solución

1. Sistema web con actualización de cupos en tiempo real usando bloqueo de base de datos.
2. Flujo de reserva en 3 pasos: seleccionar fecha → ingresar personas → confirmar.
3. Dashboard con estadísticas de ocupación y paquetes más reservados.
4. Código de reserva único generado automáticamente al confirmar.
5. Cancelación directa desde el perfil del cliente sin necesidad de contactar a la agencia.

---

## 19. Prototipo seleccionado

Se seleccionó una aplicación web responsive con:
- Catálogo de paquetes con tarjetas visuales y filtros.
- Detalle de paquete con fechas disponibles y botón de reserva.
- Dashboard administrativo con métricas clave.
- Gestión completa de catálogos desde el panel admin.

**Justificación:** Cubre las necesidades de ambos usuarios, es accesible desde cualquier dispositivo y no requiere instalación.

---

## 20. Forma de evaluar el prototipo

1. **Prueba de usabilidad:** 5 usuarios reales completan una reserva sin instrucciones.
2. **Métrica de éxito:** tasa de completación de reserva > 85% en primera visita.
3. **Tiempo objetivo:** completar una reserva en menos de 3 minutos.
4. **Feedback cualitativo:** entrevistas post-uso para identificar puntos de fricción.
5. **Prueba de carga:** simular 50 reservas simultáneas y verificar que no haya overbooking.
