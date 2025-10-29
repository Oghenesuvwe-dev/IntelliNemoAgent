# Simple ASCII Architecture (Backup)

If mermaid doesn't work, replace with this ASCII diagram:

```
┌─────────────────────────────────────────────────────────────────┐
│                    IntelliNemo Agent Architecture               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ CloudWatch  │  │   Manual    │  │   System    │
│   Alarms    │  │   Alerts    │  │  Metrics    │
└──────┬──────┘  └──────┬──────┘  └──────┬──────┘
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
                ┌─────────────┐
                │ EventBridge │
                │   Router    │
                └──────┬──────┘
                       │
                       ▼
                ┌─────────────┐
                │   Lambda    │
                │Orchestrator │
                └──────┬──────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ NVIDIA NIM  │ │  Systems    │ │ S3 Audit    │
│ AI Engine   │ │  Manager    │ │    Logs     │
└──────┬──────┘ └─────────────┘ └─────────────┘
       │
       ▼
┌─────────────┐
│ Confidence  │
│  Scoring    │
└──────┬──────┘
       │
   ┌───┴───┐
   │       │
   ▼       ▼
┌──────┐ ┌──────┐
│ Auto │ │Manual│
│ Fix  │ │Review│
└──────┘ └──────┘
```

## Or use this simple text flow:

```
CloudWatch/Alerts → EventBridge → Lambda → NVIDIA NIM → AI Decision → Auto/Manual Response
                                     ↓
                                S3 Audit Logs
```