# External References

Esta carpeta separa material de estudio externo de las configuraciones activas
del repositorio. Su objetivo es permitir analizar dotfiles publicos, registrar
su procedencia y adoptar solamente ideas comprendidas, adaptadas y probadas.

Nada bajo `references/` es desplegable. Los perfiles rechazan estas rutas y los
clones completos permanecen ignorados en `references/inbox/`.

## Lifecycle

```text
collect -> inventory -> review -> adapt -> canary -> promote -> retire
```

1. **Collect**: clonar o copiar temporalmente la fuente en `inbox/`.
2. **Inventory**: registrar autor, URL, revision, fecha y licencia en un dossier.
3. **Review**: clasificar cada idea sin ejecutarla ni enlazarla.
4. **Adapt**: reescribir solo lo necesario dentro de la capa canonica propia.
5. **Canary**: probar primero en una maquina o perfil de bajo riesgo.
6. **Promote**: activar en produccion unicamente despues de validar el flujo.
7. **Retire**: eliminar el clon temporal y cerrar el dossier. La atribucion o
   licencia que siga siendo necesaria debe conservarse en la configuracion
   promovida o en documentacion de procedencia.

## Review States

| Estado | Significado |
|---|---|
| `pending-review` | Todavia no fue comprendido ni clasificado |
| `keep` | Sirve como configuracion propia, se comprende y esta validado |
| `adapt` | La idea sirve, pero nombres, teclas, rutas o dependencias deben cambiar |
| `remove` | No aporta al flujo actual o introduce una dependencia innecesaria |
| `reference-only` | Es interesante para estudiar, pero no debe estar activa |

`keep` no significa copiar sin revisar. Exige conocer la licencia, entender el
comportamiento y comprobar que la configuracion ya es apropiada para este repo.

## Directory Layout

```text
references/
  inbox/                    # clones temporales ignorados por Git
  dotfiles/                 # un dossier versionado por fuente
  templates/                # plantilla para nuevas evaluaciones
  tools/                    # utilidades de auditoria; nunca de despliegue
```

Para iniciar una evaluacion:

```sh
cp -R references/templates references/dotfiles/<owner>-<repository>
git clone <source-url> references/inbox/<owner>-<repository>
references/tools/compare-files.py references/inbox/<owner>-<repository>
```

La comparacion por contenido detecta coincidencias, no demuestra autoria ni
reemplaza una revision de licencia. Los recursos que una fuente recibio de un
tercero deben atribuirse al origen real cuando pueda identificarse.

## Boundaries

- No agregar `references/` a `profiles/*.links`.
- No ejecutar automaticamente scripts o hooks importados.
- No copiar secretos, rutas privadas, caches ni historiales Git.
- No convertir un clon externo en dependencia de runtime.
- No copiar nuevo codigo si su licencia no permite determinar las condiciones.
- Las decisiones propias viven en `shared/`, `os/`, `hardware/` o `scripts/`;
  el dossier solo conserva evidencia y razonamiento.

