# Análisis de Riesgo: {TEMA}

**Fecha**: YYYY-MM-DD  
**Analista**: Agente Riesgo

---

## Resumen Ejecutivo

| Métrica | Valor |
|---------|-------|
| **Perfil de riesgo global** | 🟢 BAJO / 🟡 MODERADO / 🟠 ELEVADO / 🔴 CRÍTICO |
| **Riesgos críticos** | X |
| **Riesgos a monitorizar** | Y |
| **Cambio vs anterior** | ↑ Aumentado / → Estable / ↓ Reducido |

**Resumen**:  
[2-3 líneas sobre el estado de riesgo]

---

## Mapa de Riesgos

### 🔴 Riesgos Críticos

#### RC1: [Nombre del Riesgo]

| Campo | Valor |
|-------|-------|
| **Categoría** | Negocio / Financiero / Externo / Valoración |
| **Probabilidad** | ALTA |
| **Impacto** | ALTO |
| **Horizonte** | INMEDIATO / CORTO / MEDIO / LARGO |

**Descripción**:  
[Qué puede pasar y por qué es crítico]

**Señales de alerta**:
- 🚨 [Señal 1]
- 🚨 [Señal 2]

**Mitigación/Acción**:  
[Qué hacer si se materializa]

---

### ⚠️ Riesgos a Monitorizar

#### RM1: [Nombre del Riesgo]

| Campo | Valor |
|-------|-------|
| **Categoría** | Negocio / Financiero / Externo / Valoración |
| **Probabilidad** | MEDIA |
| **Impacto** | MEDIO/ALTO |
| **Horizonte** | CORTO / MEDIO / LARGO |

**Descripción**:  
[Explicación del riesgo]

**Señales de alerta**:
- ⚠️ [Señal 1]

---

#### RM2: [Nombre del Riesgo]

| Campo | Valor |
|-------|-------|
| **Categoría** | Negocio / Financiero / Externo / Valoración |
| **Probabilidad** | BAJA/MEDIA |
| **Impacto** | ALTO |
| **Horizonte** | MEDIO / LARGO |

**Descripción**:  
[Explicación del riesgo]

**Señales de alerta**:
- ⚠️ [Señal 1]

---

### 🟢 Riesgos Aceptables

| Riesgo | Prob. | Impacto | Comentario |
|--------|-------|---------|------------|
| [Riesgo 1] | BAJA | BAJO | [Nota] |
| [Riesgo 2] | BAJA | MEDIO | [Nota] |
| [Riesgo 3] | MEDIA | BAJO | [Nota] |

---

## Matriz Visual de Riesgos

```
                    IMPACTO
              Bajo    Medio    Alto
         ┌────────┬────────┬────────┐
    Alta │   RM3  │  RM1   │  RC1   │
         ├────────┼────────┼────────┤
P  Media │   RA1  │  RM2   │  RM4   │
R        ├────────┼────────┼────────┤
O  Baja  │   RA2  │  RA3   │  RM5   │
B        └────────┴────────┴────────┘

RC = Crítico (acción inmediata)
RM = Monitorizar
RA = Aceptable
```

---

## Análisis de Escenarios

### 📈 Bull Case

| Campo | Valor |
|-------|-------|
| **Probabilidad** | X% |
| **Descripción** | [Qué tiene que pasar] |
| **Impacto en valoración** | +X% |

### 📊 Base Case

| Campo | Valor |
|-------|-------|
| **Probabilidad** | X% |
| **Descripción** | [Escenario más probable] |
| **Impacto en valoración** | +/- X% |

### 📉 Bear Case

| Campo | Valor |
|-------|-------|
| **Probabilidad** | X% |
| **Trigger** | [Qué lo causaría] |
| **Descripción** | [Cómo se desarrollaría] |
| **Impacto en valoración** | -X% |

### ⚫ Tail Risk (Worst Case)

| Campo | Valor |
|-------|-------|
| **Probabilidad** | <5% |
| **Escenario** | [El peor caso razonable] |
| **Pérdida máxima** | -X% |

---

## Triggers de Acción

| Señal | Acción | Urgencia |
|-------|--------|----------|
| [Señal específica 1] | REDUCIR X% | INMEDIATA |
| [Señal específica 2] | SALIR | INMEDIATA |
| [Señal específica 3] | REVISAR TESIS | SEMANAL |
| [Señal específica 4] | AUMENTAR | OPORTUNISTA |

---

## Checklist de Monitorización

### Semanal
- [ ] Revisar noticias del sector
- [ ] Verificar precio vs niveles técnicos clave
- [ ] Comprobar calendario de eventos próximos
- [ ] Revisar posiciones de insiders

### Mensual
- [ ] Actualizar matriz de riesgos
- [ ] Revisar tesis de inversión
- [ ] Comparar con competidores

### Trimestral (Post-Earnings)
- [ ] Análisis completo de resultados
- [ ] Actualizar valoración
- [ ] Re-evaluar todos los riesgos

---

## Veto del Agente de Riesgo

| Condición | Estado | Veto Activo |
|-----------|--------|-------------|
| ≥1 riesgo CRÍTICO sin mitigación | SÍ/NO | 🔴/🟢 |
| Perfil global = CRÍTICO | SÍ/NO | 🔴/🟢 |
| Trigger de salida activado | SÍ/NO | 🔴/🟢 |

**Estado del veto**: 🟢 NO ACTIVO / 🔴 ACTIVO

**Si veto activo, razón**:  
[Explicación de por qué se veta la inversión]
