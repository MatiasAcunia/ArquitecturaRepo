# 00 — Antes de empezar | ArquitecturaRepo v1.3.0

> Manual de uso revisado para el release público v1.3.0 (17 de octubre de 2026). Conserva el contenido textual del manual original 00–07 de septiembre de 2026 con correcciones específicas. La fuente era un PDF ilustrado: los pies de figura se conservan pero esta transcripción Markdown no reproduce las imágenes. No utilizar las cifras de página como referencia del archivo renderizado.

## Actualización comprobada para v1.3.0

- Versión publicada: `v1.3.0`, commit `9c00e19b74d19c741983987b9359cb5c2ac83c55`, GitHub Release del 17/10/2026; el manual de septiembre se basó en v1.1.
- El starter ofrece instalación y control de ingeniería, no un agente general capaz de construir cualquier aplicación automáticamente. Su núcleo es portable y funciona sin modelos pagados.
- La capacidad real depende de cada adaptador. `host_dispatch.py` rechaza un host si no puede comprobar límites de escritura y costo; Codex Desktop nativo no está aceptado como integración universal.
- La entrega requiere evidencia separada de contrato/código (A) y uso real del sistema instalado (B), más los gates de producto pertinentes.
- El paquete de GitHub Container Registry ofrece un punto de entrada alternativo al scaffold, no un segundo controlador ni una autorización para ejecutar campañas.

## Contenido del manual conservado

### Página 1 de la edición original

A R Q U I T E C T U RA R E P O / C O L E C C I Ó N D E U S O




00
Antes de empezar

Alcance, autoridad y límites




Matías Acuña · ArquitecturaRepo                                Revisión de compatibilidad: 17 de octubre de 2026

### Página 2 de la edición original

Contenido

     • 1. Qué vas a instalar y qué no                                     • 6. Límites y vigencia
     • 2. Quién toma cada decisión                                        • 7. Un recorrido de extremo a extremo
     • 3. La información que debe permanecer accesible                    • 8. Decisiones habituales: qué conserva el CLIENT
     • 4. Cómo leer la colección                                          • 9. Lista de arranque: una página, no un expediente
     • 5. Preparación: decisiones que sí son tuyas                        • 10. Cómo evaluar si realmente te está ayudando




1. Qué vas a instalar y qué no

Qué ofrece el starter, y qué queda fuera
ArquitecturaRepo reúne protocolos, plantillas, perfiles, herramientas de validación y un controlador local
de campaña de referencia opcional. Su propósito es organizar la continuidad de un proyecto de software
en el que participan agentes. No es una aplicación terminada, ni una herramienta que recibe un
requerimiento y entrega automáticamente un producto validado.

La publicación del starter se identifica como v1.3.0 en VERSION y el manifest publicados. Ese estado
describe la versión del repositorio; no acredita un despliegue exitoso de cualquier proyecto que copie
sus archivos. El repositorio incluye pruebas automatizadas del starter y casos sintéticos de adopción; la
instalación de una aplicación real exige requisitos propios, ejecución efectiva, pruebas de producto y
aceptación según sus riesgos. Si una capacidad todavía no se ejercitó físicamente, debe figurar como
pendiente, no como éxito previsto.

El resultado buscado es una forma de continuidad: que una nueva sesión pueda reconstruir desde el
repositorio qué producto se construye, qué decisiones siguen vigentes, cuál es el estado real, qué trabajo
está autorizado y qué falta comprobar. Una conversación puede terminar; el proyecto no debería
depender de recordarla palabra por palabra.

La colección está orientada a quien empieza con un proyecto de software propio. Usa Windows, GitHub,
ChatGPT y Codex como recorrido ilustrativo. Son herramientas de un flujo de ejemplo, no requisitos
universales de la arquitectura. El starter también puede adaptarse a otros entornos y ejecutores.

No confundir: tener un repo público o un agente que programa no demuestra que el software generado
funcione. Las capacidades se comprueban con evidencia del candidato concreto; las decisiones de
producto y las autorizaciones externas siguen perteneciendo a la persona.




  Figura 1. Autoridad, estado y evidencia. Esquema explicativo; no acredita un proyecto de destino.

### Página 3 de la edición original

2. Quién toma cada decisión

¿Necesitás un Master Owner separado?
En un proyecto pequeño puede haber una sola persona que use un Planner para estrategia y un ejecutor
que trabaje sobre el código. El modelo conserva las clases I1–I4, pero I1 no necesita existir como
actor separado si no hay infraestructura compartida, múltiples productos o una frontera sistémica que
gobernar. Crear un chat llamado “Master Owner” no crea automáticamente una necesidad de ese rol. El
Planner no pierde la responsabilidad sobre el producto por agregar otra conversación.

La revisión del código y el producto tampoco recaen en una sola autoridad: un revisor técnico puede
rechazar un candidato por evidencia, el Planner decide la aceptación estratégica y el CLIENT conserva las
decisiones de experiencia, negocio y acciones externas reservadas.




  Figura 2. Fronteras de decisión. Esquema explicativo; no acredita un proyecto de destino.




Participante                                   Responsable de                                 No debería resolver por rutina

CLIENT / Product Owner                         Objetivo, prioridades, reglas del              Merge conflicts, esquemas JSON,
                                               producto, preferencias de uso,                 estrategia de pruebas, reparación de
                                               autorización de publicación/gastos/            currentness.
                                               acciones destructivas y aceptación
                                               subjetiva.

I2 · Planner                                   Estrategia de capacidades,                     Hacer de controlador de cada bug o
                                               interpretación del producto, límites de        reescribir la tarea por cada fallo de test.
                                               una campaña, arquitectura técnica y
                                               aceptación estratégica.

I3 · Campaign Lead / Execution                 Ejecución táctica, depuración,                 Inventar nuevas reglas de producto o
Controller                                     integración, revisión independiente,           aceptarse a sí mismo.
                                               checkpoint y recuperación dentro de la
                                               campaña.

I4 · Equipo de ejecución                       Implementación, investigación, pruebas,        Sustituir la decisión de producto o
                                               revisión especializada y evidencia.            declarar aceptación estratégica.



En el flujo de esta colección, podés hablar con un ChatGPT que funciona como Planner y darle a Codex un
mensaje completo para ejecutar sobre el repositorio. Un mismo servicio comercial no equivale
automáticamente a uno de estos roles: el rol se define por su autoridad y sus obligaciones.

### Página 4 de la edición original

3. La información que debe permanecer accesible

Qué información vence a un resumen anterior
Para conocer el estado técnico, comenzá por el código y el entorno que realmente existen, el Product
State actual, los requisitos confirmados y la autoridad de campaña vigente. Una respuesta anterior de un
agente, incluso si dijo “PASS”, no reemplaza esos objetos. Una nueva preferencia explícita del
CLIENT sí puede cambiar el producto; el Planner debe incorporarla al registro vigente antes de
proseguir como si fuese la regla actual.

Un dato ausente se clasifica como UNKNOWN ; una contradicción material entre dos autoridades actuales
requiere detener la acción dependiente ( HOLD ) y reconciliarla. No se resuelve eligiendo el archivo que
parece más nuevo por su nombre.

El starter distingue L0 (evidencia de lo que dijo y aprobó el CLIENT), L1 (requisitos interpretados y Product
State vigentes) y L2 (código, base de datos, campañas, checkpoints, revisiones y runtime). Esta distinción
evita que una promesa en un chat se confunda con software desplegado.

Un agente nuevo debe reconstruir por lo menos el producto, los requisitos actuales, el ref de código o
runtime que puede comprobar, la campaña activa si la hay, el gate abierto, la mejor evidencia, los
desconocidos y la próxima acción permitida. Si aparecen dos verdades actuales contradictorias, el
sistema detiene lo que dependa de ellas en vez de improvisar.

Términos que vas a encontrar:

  • Scaffold: carpeta inicial .agentic-sdlc que instala el control layer; empieza deliberadamente en
    HOLD / UNTRUSTED_CONTEXT .

  • Discovery y adoption: conocer el proyecto real y convertir hechos y decisiones verificadas en estado
    de control coherente. No consiste en copiar un template a ciegas.
  • Product State: referencia canónica del estado actual del producto y sus capacidades.
  • Charter: contrato estratégico de una capacidad para el Campaign Lead.
  • Gate: comprobación definida antes de aceptar un resultado; no todos los proyectos usan los mismos
    gates.


4. Cómo leer la colección

Itinerario de lectura y comprobación
Consultá un manual cuando aparezca su problema operativo. Tras el 01 deberías poder mostrar un
control layer validado, aunque aún esté en HOLD . Tras el 02, un agente nuevo tendría que reconstruir
requisitos, estado, autoridad y siguiente paso sin recibir la conversación anterior. Tras el 06, la capacidad
examinada tendría que tener un candidato identificado y evidencia suficiente para el gate que se
pretende cerrar.

Si alguno de esos resultados no existe, volvé al paso que produce esa evidencia. Leer los ocho PDF o
reunir documentos no equivale a haber instalado un sistema de desarrollo.

Manual                               Cuándo consultarlo                   Resultado que deberías poder
                                                                          comprobar

00 · Antes de empezar                Antes de instalar.                   Entendés las responsabilidades y el
                                                                          recorrido.

01 · Instalación                     Al preparar un proyecto.             Starter y repo local presentes; scaffold
                                                                          validado, todavía sin fingir adopción.

### Página 5 de la edición original

Manual                               Cuándo consultarlo                    Resultado que deberías poder
                                                                           comprobar

02 · Planner                         Antes de la primera feature.          Descubrimiento de producto, baseline,
                                                                           adopción y contexto fresco.

03 · Operación diaria                Al trabajar con Planner y Codex.      Entendés cómo se encarga, ejecuta,
                                                                           verifica y registra cada ciclo.

04 · Pedir cambios                   Al definir funciones y corregir       Pedidos con comportamiento observable
                                     decisiones.                           y límites claros.

05 · Recuperación y seguridad        Ante errores, incidentes o acciones   Conservás evidencia y evitás daño
                                     sensibles.                            adicional.

06 · Cierre de ciclos                Cuando alguien dice “terminado”.      Sabés qué evidencia habilita aceptación
                                                                           y qué sigue abierto.

07 · Club, caso guiado               Para practicar la ruta completa.      Podés seguir una capacidad de socio
                                                                           desde requisitos a aceptación.



El 01 y el 02 se leen en orden la primera vez. Los demás funcionan como referencias de trabajo: no hace
falta estudiar todas las páginas antes de empezar un proyecto sencillo.


5. Preparación: decisiones que sí son tuyas

Antes de instalar, anotá en una página: qué problema querés resolver, para quién, dónde se usará el
producto, qué datos manejará, fecha objetivo, presupuesto posible, calidad de la interfaz y qué queda
afuera. Si algo no está decidido, registralo como pregunta abierta. No hace falta elegir SQL, un
framework, una rama de Git o el mecanismo de rollback; esas son decisiones de ingeniería.


  Ejemplo: “Quiero una app local para registrar socios y cuotas de un club. La usa una persona
  administrativa. No habrá pagos online en la primera versión. Debe conservar el historial. Quiero una
  pantalla simple; el presupuesto de servicios pagos es cero”.


En proyectos con datos personales, publicación o pagos, la responsabilidad de autorizar el tratamiento y
las acciones externas no desaparece por usar agentes. El Planner debe diseñar los controles técnicos y
explicarte las decisiones relevantes en lenguaje de producto.


6. Límites y vigencia

ArquitecturaRepo publica mecanismos genéricos y ejemplos sintéticos. Sus pruebas de transferencia no
demuestran que cualquier aplicación real quede correctamente instalada o sea segura. El runtime
campaignctl.py es opcional y no ejecuta arbitrariamente agentes por sí solo. La guía explica un flujo de
uso, no certifica un proyecto.

Esta edición se contrastó con ArquitecturaRepo@9c00e19b74d1 (VERSION=1.3.0, 17/10/2026). Los controles
de UI, precios y nombres de modelos cambian; no basamos el método en una pantalla fija ni en la
obligación de pagar un plan específico. El código y los contratos vigentes del repositorio tienen prioridad
sobre capturas de un manual. El código y la documentación originales del repositorio se publican bajo
licencia MIT; el contenido de terceros requiere derechos propios.

### Página 6 de la edición original

7. Un recorrido de extremo a extremo

La arquitectura se comprende mejor siguiendo una capacidad concreta. Supongamos que una asociación
quiere registrar socios. La persona define quién puede registrar datos, qué información es obligatoria y
qué significa desactivar una ficha. El Planner convierte esas decisiones en una especificación de producto
comprobable; no supone que “desactivar” equivale a borrar. Antes de autorizar desarrollo, reconstruye lo
que realmente existe y plantea las preguntas que afectan el resultado.

Una vez confirmado el alcance, el Planner registra los requisitos actuales, el estado del producto, el
entorno técnico y un plan con fechas. Elige una capacidad que pueda entregarse y verificarse por
completo. Emite un charter: qué debe quedar disponible, qué otras partes pueden cambiarse, qué
condiciones de calidad deben demostrarse y qué cambios de alcance requieren nueva decisión.

El Campaign Lead organiza las tareas concretas. Implementa, prueba, corrige, solicita revisión
independiente y entrega un candidato identificable. El Planner comprueba la evidencia y registra
aceptación solo cuando los controles pertinentes están satisfechos. Si hay un problema ordinario dentro
del encargo, lo devuelve al mismo ciclo de ejecución; no inicia una nueva fase de planificación por cada
fallo.

El ciclo no concluye por haber generado un informe convincente. Concluye cuando el producto ofrece la
capacidad pedida y el estado que permite continuar ha quedado registrado de forma recuperable. En el
manual 07 se desarrolla este recorrido con un caso completo y datos ficticios.


8. Decisiones habituales: qué conserva el CLIENT

Situación                                                 Quién decide y cuál es la evidencia esperada

“El socio moroso no puede inscribirse”.                   CLIENT define la regla; Planner la incorpora al requisito
                                                          actual.

“¿SQLite o PostgreSQL?”.                                  Ingeniería elige según uso, concurrencia, respaldo, despliegue
                                                          y riesgos confirmados.

“¿Podemos publicar los datos reales como demo?”.          CLIENT debe autorizar el uso lícito y específico; el equipo
                                                          previene exposición por defecto.

“Un test falló tras una corrección”.                      I3 investiga y repara dentro del charter; el resultado vuelve a
                                                          verificarse.

“Quiero convertir la app local en un servicio público”.   CLIENT confirma el cambio de objetivo; Planner rediseña
                                                          alcance, red y seguridad.

“Codex dijo que todo está listo”.                         No es aceptación: se exigen candidato y pruebas pertinentes,
                                                          incluida experiencia de uso si aplica.




9. Lista de arranque: una página, no un expediente

Prepará una breve ficha de proyecto, incluso si no tenés experiencia de desarrollo. Debe permitir que el
Planner conozca el destino sin adivinar decisiones tuyas:

  • Propósito: el problema que resuelve la primera versión y quién usa el resultado.
  • Recorrido principal: qué intenta hacer una persona usuaria y cómo reconoce que funcionó.
  • Datos: qué se almacena, si incluye información personal y cuánto tiempo debe conservarse.
  • Entorno: dispositivo o lugar de uso, conectividad y si la app debe funcionar sin Internet.
  • Límites: fecha objetivo, dinero disponible, integraciones autorizadas y funciones excluidas.

### Página 7 de la edición original

• Criterio visible de calidad: legibilidad, mensajes de error, accesibilidad, rendimiento u otra condición
    importante.

No es necesario escribir una especificación técnica completa: esa es responsabilidad del sistema de
ingeniería, que debe aclarar los vacíos relevantes. Si una decisión de producto está pendiente, se registra
como abierta; no se disfraza de hecho. Conservá la ficha como entrada para la conversación del manual
02.


10. Cómo evaluar si realmente te está ayudando

Después de dos o tres ciclos, pedí una demostración breve: qué capacidad nueva podés usar, dónde está
la evidencia, qué cambió desde el ciclo anterior y cuál es el siguiente riesgo material. Si la única
respuesta es “hicimos muchos commits”, “se abrieron varios agentes” o “tenemos más documentación”,
todavía falta conectar el trabajo con el resultado del producto.

Una arquitectura así puede reducir la dependencia de conversaciones individuales, pero no vuelve
innecesarios el juicio sobre el producto, la revisión de seguridad ni la comprobación de funcionamiento.
Su utilidad se mide en continuidad, claridad de responsabilidad, resultado visible y capacidad de
recuperación, no en la cantidad de pantallas o agentes activos.

Continuar con: Manual 01, instalación.

Referencias de esta edición
Fuente: repositorio público MatiasAcunia/ArquitecturaRepo en el commit 56f04267b6a9 . Rutas verificadas:

  • README.md
  • LICENSE
  • AGENTS.md
  • docs/00_ARCHITECTURE_OVERVIEW.md
  • docs/02_RESEARCH_BASIS_AND_LIMITS.md
  • protocols/AUTHORITY_MODEL.md

Las instrucciones de este volumen describen el starter y un procedimiento de uso. Ninguna prueba de los
ejemplos sustituye la verificación del proyecto de destino.
