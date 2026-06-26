"""
In lại bảng điểm RAGAS từ data/ragas_report.json (không cần chạy lại evaluation).
Dùng để chụp screenshot evidence/03_ragas_scores.png.

Cách dùng (từ thư mục gốc project):
    venv\\Scripts\\python src\\show_ragas_scores.py
"""
import sys
import json
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Ưu tiên data/, fallback sang evidence/
root = Path(__file__).parent.parent
for p in (root / "data" / "ragas_report.json", root / "evidence" / "03_ragas_report.json"):
    if p.exists():
        report = json.loads(p.read_text(encoding="utf-8"))
        break
else:
    print("❌ Không tìm thấy ragas_report.json — hãy chạy 03_ragas_evaluation.py trước.")
    sys.exit(1)

v1 = report["prompt_v1_scores"]
v2 = report["prompt_v2_scores"]

print("=" * 65)
print("  BẢNG ĐIỂM RAGAS — So sánh Prompt V1 vs V2")
print("=" * 65)
print(f"  {'Metric':30s}  {'V1':>8}  {'V2':>8}  Winner")
print("-" * 65)
for metric in ["faithfulness", "answer_relevancy", "context_recall", "context_precision"]:
    s1, s2 = v1[metric], v2[metric]
    winner = "← V1" if s1 > s2 else ("← V2" if s2 > s1 else "=")
    print(f"  {metric:30s}  {s1:>8.4f}  {s2:>8.4f}  {winner}")
print("=" * 65)

best = max(v1["faithfulness"], v2["faithfulness"])
status = "✅ ĐẠT" if report.get("target_met") else "⚠️  CHƯA ĐẠT"
print(f"  Mục tiêu faithfulness ≥ 0.8: {status}  (cao nhất = {best:.4f})")
print("=" * 65)
