import os

archi1_content = """architecture-beta
    
    service user(cloud)[Usuario / Operario]
    
    group cloud(cloud)[WMS COLOGISTIC Cloud]

        service gateway(internet)[API Gateway] in cloud
        
        service wms(server)[Core WMS Spring Boot] in cloud
        service ml(server)[ML Forecast Python] in cloud
        
        service kafka(server)[Bus Kafka] in cloud
        service db(database)[PostgreSQL] in cloud

    user:B -- T:gateway
    gateway:L -- R:wms
    gateway:R -- L:ml
    
    wms:R -- L:kafka
    ml:L -- R:kafka
    
    wms:B -- T:db
    ml:B -- T:db
"""

archi2_content = """---
description: "Diagrama de Arquitectura Intermedia - WMS COLOGISTIC"
config:
  layout: elk
---
flowchart TD
    classDef frontend fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef gateway fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#000
    classDef backend fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef ml fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000
    classDef database fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#000

    subgraph Frontend_Layer [📱 Frontend]
        Dashboard[Dashboard Web<br/>Jefe Operaciones]
        AppOperario[App Móvil<br/>Operario Montacargas]
    end
    class Frontend_Layer frontend

    subgraph Gateway_Layer [🚪 Gateway]
        Gateway[API Gateway]
    end
    class Gateway_Layer gateway

    subgraph Backend_Layer [⚙️ Core WMS - Spring Boot]
        MsInventario[MS Inventario & Ubicaciones]
        MsRecepcion[MS Recepción & Despacho]
        MsUsuarios[MS Usuarios & Seguridad]
    end
    class Backend_Layer backend

    subgraph ML_Layer [🧠 Inteligencia Artificial - Python]
        MsForecasting[MS Pronóstico de Capacidad]
    end
    class ML_Layer ml

    subgraph Data_Layer [💾 Bases de Datos]
        PostgreSQL[(PostgreSQL Principal)]
    end
    class Data_Layer database

    Dashboard --> Gateway
    AppOperario --> Gateway

    Gateway --> MsUsuarios
    Gateway --> MsInventario
    Gateway --> MsRecepcion
    Gateway --> MsForecasting

    MsUsuarios --> PostgreSQL
    MsInventario --> PostgreSQL
    MsRecepcion --> PostgreSQL
    MsForecasting -->|Lectura histórico| PostgreSQL
"""

archi3_content = """---
description: "Diagrama de Arquitectura Detallada - WMS COLOGISTIC"
config:
  layout: elk
---
flowchart TD
    classDef cdn fill:#546e7a,stroke:#263238,stroke-width:2px,color:#fff
    classDef frontend fill:#e1f5fe,stroke:#01579b,stroke-width:2px,color:#000
    classDef gateway fill:#fff9c4,stroke:#fbc02d,stroke-width:2px,color:#000
    classDef backend fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000
    classDef ml fill:#f3e5f5,stroke:#6a1b9a,stroke-width:2px,color:#000
    classDef messaging fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef database fill:#ffebee,stroke:#c62828,stroke-width:2px,color:#000
    classDef external fill:#eceff1,stroke:#37474f,stroke-width:2px,color:#000

    subgraph Edge_Layer [🌐 Edge Layer]
        CDN[CDN / WAF]
    end
    class Edge_Layer cdn

    subgraph Frontend_Layer [📱 Frontend]
        Dashboard[Dashboard Web<br/>Jefe Operaciones]
        AppOperario[App Móvil<br/>Operario Montacargas]
    end
    class Frontend_Layer frontend

    subgraph Gateway_Layer [🚪 Gateway]
        Gateway[API Gateway]
        Auth[Servicio de Autenticación<br/>Spring Security JWT]
    end
    class Gateway_Layer gateway

    subgraph Backend_Layer [⚙️ Core WMS - Spring Boot]
        MsInventario[MS Inventario y Ubicaciones]
        MsRecepcion[MS Recepción y Despacho]
        MsTrazabilidad[MS Trazabilidad y Auditoría]
    end
    class Backend_Layer backend

    subgraph ML_Layer [🧠 Inteligencia Artificial - Python]
        MsForecasting[MS Pronóstico de Capacidad<br/>FastAPI / Flask]
        ModeloML([Modelo ML Entrenado])
    end
    class ML_Layer ml

    subgraph Messaging_Layer [📨 Eventos Asíncronos]
        KafkaBroker[Cluster Kafka]
    end
    class Messaging_Layer messaging

    subgraph Data_Layer [💾 Datos]
        PostgreSQL[(PostgreSQL<br/>Base de Datos WMS)]
        Redis[(Redis<br/>Caché de Ubicaciones)]
    end
    class Data_Layer database

    %% Flujos
    Dashboard --> CDN
    AppOperario --> CDN
    CDN --> Gateway
    Gateway --> Auth
    Auth -->|Valida Token| MsInventario
    Gateway --> MsInventario
    Gateway --> MsRecepcion
    Gateway --> MsTrazabilidad
    Gateway --> MsForecasting

    MsInventario --> PostgreSQL
    MsRecepcion --> PostgreSQL
    MsTrazabilidad --> PostgreSQL
    MsInventario -.->|Caché rápida| Redis

    MsRecepcion -->|Evento: Nuevo Ingreso/Salida| KafkaBroker
    KafkaBroker -->|Consume| MsTrazabilidad
    KafkaBroker -->|Consume| MsForecasting

    MsForecasting -->|Infiere predicción| ModeloML
    MsForecasting -->|Consulta Histórico| PostgreSQL
"""

er_content = """erDiagram
    %% ==========================================
    %% ESQUEMA: INVENTARIO (WMS Core)
    %% ==========================================
    UBICACION ||--o{ PALETA : "almacena"
    UBICACION {
        int id PK
        string pasillo "Ej. P-01"
        string nivel "Ej. N-03"
        string estado "DISPONIBLE, OCUPADO, BLOQUEADO"
        decimal capacidad_max_kg
    }

    PALETA ||--o| PRODUCTO : "contiene"
    PALETA {
        string codigo_lote PK
        int id_ubicacion FK
        int id_producto FK
        string estado "INGRESADO, ALMACENADO, DESPACHADO"
        timestamp fecha_ingreso
    }

    PRODUCTO {
        int id PK
        string sku
        string descripcion
        string categoria
    }

    %% ==========================================
    %% ESQUEMA: TRANSACCIONES WMS
    %% ==========================================
    MOVIMIENTO }o--|| PALETA : "registra"
    MOVIMIENTO {
        int id PK
        string codigo_lote FK
        string tipo_movimiento "RECEPCION, UBICACION, DESPACHO"
        timestamp fecha
        int usuario_operario_id
    }

    %% ==========================================
    %% ESQUEMA: ML FORECASTING
    %% ==========================================
    PRONOSTICO_CAPACIDAD {
        int id PK
        date fecha_proyeccion
        decimal porcentaje_ocupacion_estimado
        string nivel_alerta "BAJO, MEDIO, CRITICO"
        timestamp fecha_calculo
    }
"""

with open("archi.mmd", "w") as f: f.write(archi1_content)
with open("archi2.mmd", "w") as f: f.write(archi2_content)
with open("archi3.mmd", "w") as f: f.write(archi3_content)
with open("er.mmd", "w") as f: f.write(er_content)
