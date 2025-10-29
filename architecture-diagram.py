import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

# Create figure and axis
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# Define colors
aws_orange = '#FF9900'
nvidia_green = '#76B900'
ai_teal = '#00D4AA'
aws_dark = '#232F3E'
light_gray = '#F0F0F0'

# Title
ax.text(7, 9.5, 'IntelliNemo Agent Architecture', fontsize=20, fontweight='bold', ha='center')
ax.text(7, 9, 'AI-Powered SRE Orchestrator', fontsize=14, ha='center', style='italic')

# Step 1: CloudWatch Monitoring
cloudwatch = FancyBboxPatch((0.5, 7), 2.5, 1.2, boxstyle="round,pad=0.1", 
                           facecolor=aws_orange, edgecolor='black', linewidth=2)
ax.add_patch(cloudwatch)
ax.text(1.75, 7.6, 'CloudWatch\nAlarms', fontsize=11, fontweight='bold', ha='center', va='center')

# Step 2: EventBridge
eventbridge = FancyBboxPatch((4, 7), 2.5, 1.2, boxstyle="round,pad=0.1",
                            facecolor=aws_orange, edgecolor='black', linewidth=2)
ax.add_patch(eventbridge)
ax.text(5.25, 7.6, 'EventBridge\nRouter', fontsize=11, fontweight='bold', ha='center', va='center')

# Step 3: Lambda Function
lambda_func = FancyBboxPatch((7.5, 7), 2.5, 1.2, boxstyle="round,pad=0.1",
                            facecolor=aws_orange, edgecolor='black', linewidth=2)
ax.add_patch(lambda_func)
ax.text(8.75, 7.6, 'Lambda\nOrchestrator', fontsize=11, fontweight='bold', ha='center', va='center')

# Step 4: NVIDIA NIM
nvidia_nim = FancyBboxPatch((11, 7), 2.5, 1.2, boxstyle="round,pad=0.1",
                           facecolor=nvidia_green, edgecolor='black', linewidth=2)
ax.add_patch(nvidia_nim)
ax.text(12.25, 7.6, 'NVIDIA NIM\nLlama-3.1', fontsize=11, fontweight='bold', ha='center', va='center')

# AI Decision Engine (Center)
ai_engine = FancyBboxPatch((5.5, 4.5), 3, 1.5, boxstyle="round,pad=0.1",
                          facecolor=ai_teal, edgecolor='black', linewidth=2)
ax.add_patch(ai_engine)
ax.text(7, 5.25, 'AI Decision Engine\nConfidence Scoring', fontsize=12, fontweight='bold', ha='center', va='center')

# Decision Diamond
decision_points = np.array([[7, 3.5], [8, 2.5], [7, 1.5], [6, 2.5]])
decision = patches.Polygon(decision_points, closed=True, facecolor='yellow', edgecolor='black', linewidth=2)
ax.add_patch(decision)
ax.text(7, 2.5, 'Confidence\n≥ 7/10?', fontsize=10, fontweight='bold', ha='center', va='center')

# Systems Manager (Auto-remediation)
systems_mgr = FancyBboxPatch((9.5, 0.5), 2.5, 1.2, boxstyle="round,pad=0.1",
                            facecolor=aws_dark, edgecolor='black', linewidth=2)
ax.add_patch(systems_mgr)
ax.text(10.75, 1.1, 'Systems Manager\nAuto-Remediation', fontsize=10, fontweight='bold', 
        ha='center', va='center', color='white')

# Manual Investigation
manual_inv = FancyBboxPatch((2, 0.5), 2.5, 1.2, boxstyle="round,pad=0.1",
                           facecolor='red', edgecolor='black', linewidth=2)
ax.add_patch(manual_inv)
ax.text(3.25, 1.1, 'Manual\nInvestigation', fontsize=10, fontweight='bold', 
        ha='center', va='center', color='white')

# Supporting Services
# S3 Audit Logs
s3_audit = FancyBboxPatch((0.5, 4.5), 2, 1, boxstyle="round,pad=0.1",
                         facecolor=light_gray, edgecolor='black', linewidth=1)
ax.add_patch(s3_audit)
ax.text(1.5, 5, 'S3 Audit\nLogs', fontsize=9, ha='center', va='center')

# Secrets Manager
secrets = FancyBboxPatch((11.5, 4.5), 2, 1, boxstyle="round,pad=0.1",
                        facecolor=light_gray, edgecolor='black', linewidth=1)
ax.add_patch(secrets)
ax.text(12.5, 5, 'Secrets\nManager', fontsize=9, ha='center', va='center')

# Arrows - Main Flow
# CloudWatch to EventBridge
ax.arrow(3, 7.6, 0.8, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
# EventBridge to Lambda
ax.arrow(6.5, 7.6, 0.8, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
# Lambda to NVIDIA NIM
ax.arrow(10, 7.6, 0.8, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
# NVIDIA NIM to AI Engine
ax.arrow(12.25, 7, 0, -0.8, head_width=0.1, head_length=0.1, fc='black', ec='black')
ax.arrow(12.25, 6.2, -4, -0.5, head_width=0.1, head_length=0.1, fc='black', ec='black')
# AI Engine to Decision
ax.arrow(7, 4.5, 0, -0.8, head_width=0.1, head_length=0.1, fc='black', ec='black')
# Decision to Systems Manager (Yes)
ax.arrow(7.5, 2, 2.5, -0.8, head_width=0.1, head_length=0.1, fc='green', ec='green')
ax.text(9, 1.5, 'YES', fontsize=9, fontweight='bold', color='green')
# Decision to Manual (No)
ax.arrow(6.5, 2, -2.5, -0.8, head_width=0.1, head_length=0.1, fc='red', ec='red')
ax.text(5, 1.5, 'NO', fontsize=9, fontweight='bold', color='red')

# Supporting service connections
ax.arrow(8.75, 7, -6, -1.8, head_width=0.05, head_length=0.05, fc='gray', ec='gray', linestyle='--')
ax.arrow(8.75, 7, 3.5, -1.8, head_width=0.05, head_length=0.05, fc='gray', ec='gray', linestyle='--')

# Performance metrics box
perf_box = FancyBboxPatch((0.5, 2.5), 4, 1.5, boxstyle="round,pad=0.1",
                         facecolor='lightblue', edgecolor='black', linewidth=1)
ax.add_patch(perf_box)
ax.text(2.5, 3.6, 'Performance Metrics', fontsize=11, fontweight='bold', ha='center')
ax.text(2.5, 3.2, '• <5 sec end-to-end response', fontsize=9, ha='center')
ax.text(2.5, 2.9, '• 600x faster than manual', fontsize=9, ha='center')
ax.text(2.5, 2.6, '• $0.90/month operational cost', fontsize=9, ha='center')

# Tech stack labels
ax.text(1.75, 6.5, 'Monitoring', fontsize=9, ha='center', style='italic')
ax.text(5.25, 6.5, 'Event Router', fontsize=9, ha='center', style='italic')
ax.text(8.75, 6.5, 'Orchestration', fontsize=9, ha='center', style='italic')
ax.text(12.25, 6.5, 'AI Reasoning', fontsize=9, ha='center', style='italic')

plt.tight_layout()
plt.savefig('/Users/machine/Desktop/IntelliNemo Agent, AI-Powered SRE Orchestrator/intellinemo-architecture.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("Architecture diagram saved as 'intellinemo-architecture.png'")