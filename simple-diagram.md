# Simple Working Mermaid Diagram

## Option 1: Basic Flow
```mermaid
flowchart LR
    A[CloudWatch] --> B[EventBridge]
    B --> C[Lambda]
    C --> D[NVIDIA NIM]
    D --> E{Confidence Check}
    E -->|High| F[Auto Fix]
    E -->|Low| G[Manual Review]
```

## Option 2: Detailed Flow
```mermaid
graph TD
    CW[CloudWatch Alarms] --> EB[EventBridge]
    EB --> LF[Lambda Function]
    LF --> NIM[NVIDIA NIM]
    NIM --> AI[AI Decision]
    AI --> DEC{Confidence >= 7?}
    DEC -->|Yes| SM[Systems Manager]
    DEC -->|No| MAN[Manual Investigation]
    SM --> REM[Auto Remediation]
    LF --> S3[S3 Audit Logs]
    LF --> SEC[Secrets Manager]
```

## Alternative: Use Draw.io Template

**Quick Steps:**
1. Go to https://app.diagrams.net/
2. Choose "AWS Architecture" template
3. Drag these components:
   - CloudWatch (Monitoring)
   - Lambda (Compute)
   - EventBridge (Integration)
   - S3 (Storage)
   - Add NVIDIA NIM as custom box
4. Connect with arrows
5. Export as PNG

## Or Use This ASCII (Screenshot it):
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ CloudWatch  │───▶│ EventBridge │───▶│   Lambda    │───▶│ NVIDIA NIM  │
│   Alarms    │    │   Router    │    │Orchestrator │    │ Llama-3.1   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                              │                    │
                                              ▼                    ▼
                                      ┌─────────────────────────────────┐
                                      │      AI Decision Engine         │
                                      │     Confidence Scoring          │
                                      └──────────────┬──────────────────┘
                                                     │
                                                     ▼
                                              ┌─────────────┐
                                              │Confidence   │
                                              │  >= 7/10?   │
                                              └──────┬──────┘
                                                     │
                                            ┌────────┴────────┐
                                            ▼                 ▼
                                    ┌─────────────┐   ┌─────────────┐
                                    │  Systems    │   │   Manual    │
                                    │  Manager    │   │Investigation│
                                    │ Auto-Fix    │   │   Review    │
                                    └─────────────┘   └─────────────┘
```