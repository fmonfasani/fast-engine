<!-- ECOSYSTEM_DOCTRINE: fast-engine -->
# ⚡ Ecosystem Doctrine — Fast-Engine (CLI MVP)

Este repositorio forma parte del ecosistema **Fast-Engine / Genesis Engine / MCPturbo**.  
Su función es ser una **herramienta de línea de comandos simple**, pensada como MVP para que cualquier usuario pueda generar un proyecto funcional con una sola orden.

## ⚙️ Rol Declarado

- Tipo: **CLI minimalista**
- Nombre: `fast-engine`
- Dominio: Interfaz de entrada del usuario
- Función: Recibir la orden del usuario, delegar el trabajo a Genesis Engine, y mostrar el estado

## 🔒 Mandamientos del Proyecto

### 1. **No generarás código por tu cuenta**
`fast-engine` **nunca debe crear prompts, ni definir arquitectura, ni escribir archivos directamente**.  
Solo debe delegar la ejecución a Genesis Engine.

### 2. **No orquestarás workflows**
La CLI **no contiene lógica de ejecución de tareas ni workflows entre agentes**.  
Eso es responsabilidad de `genesis-engine` y `mcpturbo`.

### 3. **No accederás directamente a LLMs**
`fast-engine` **no puede hacer llamadas HTTP a OpenAI, Claude, DeepSeek ni ninguna API externa**.  
Toda comunicación con LLMs debe estar encapsulada en agentes de Genesis Engine.

### 4. **Tu código debe ser legible, idiomático y enfocado en UX**
Usá `Typer`, `Rich`, y convenciones estándar de CLI tools.  
Prioridad: simple, rápida y predecible para el usuario.

### 5. **No implementarás lógica empresarial**
`fast-engine` no debe tomar decisiones sobre plantillas, tecnologías ni flujos.  
Solo ofrece lo que `genesis-engine` tiene registrado y disponible.

### 6. **Todo output será delegación del motor**
`fast-engine` no genera contenido. Muestra lo que Genesis Engine produce.  
Actúa como un mostrador, no como un cocinero.

---

## 💡 Comando principal

```bash
fast-engine init my-saas-app --template=saas-basic
