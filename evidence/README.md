# Thư mục Bằng chứng (Evidence) — Day 22: LangSmith + Prompt Versioning

Thư mục này chứa toàn bộ bằng chứng cho 4 nhiệm vụ của lab. Bên dưới là danh sách
file và phần **phân tích so sánh hai phiên bản prompt (V1 vs V2)** dựa trên kết quả
RAGAS thực tế.

---

## Danh sách bằng chứng

| File | Nhiệm vụ | Nội dung |
|------|----------|----------|
| `01_langsmith_traces.png`   | NV1 | Giao diện LangSmith hiển thị ≥ 50 traces |
| `01_rag_pipeline_log.txt`   | NV1 | Log console của RAG pipeline (bằng chứng bổ sung) |
| `02_prompt_hub.png`         | NV2 | Prompt Hub với 2 phiên bản prompt được đặt tên |
| `02_ab_routing_log.txt`     | NV2 | Log A/B routing tất định (nhãn v1/v2 cho từng câu) |
| `03_ragas_scores.png`       | NV3 | Bảng so sánh điểm RAGAS V1 vs V2 trên terminal |
| `03_ragas_report.json`      | NV3 | Báo cáo JSON đầy đủ điểm của cả V1 và V2 |
| `04_pii_demo_log.txt`       | NV4 | Output các test case PII Detector |
| `04_json_demo_log.txt`      | NV4 | Output các test case JSON Formatter |

---

## Phân tích kết quả: Prompt V1 vs V2

### Hai phiên bản khác nhau ở điểm gì?

| | **V1 — Ngắn gọn** | **V2 — Có cấu trúc** |
|---|---|---|
| Vai trò | Trợ lý AI thân thiện | Chuyên gia phân tích thông tin |
| Độ dài | 2–4 câu | 3–5 câu |
| Cấu trúc | Trả lời tự do, súc tích | 3 phần: (1) ý chính, (2) chi tiết trích từ context, (3) mức độ chắc chắn |

Cả hai prompt **dùng chung retriever** (FAISS, `k=3`), chỉ khác nhau ở bước sinh
câu trả lời (generation).

### Điểm RAGAS (50 cặp QA, mỗi phiên bản)

| Chỉ số | V1 | V2 | Phiên bản tốt hơn |
|--------|------|------|-------------------|
| **faithfulness**     | **0.963** | 0.892 | 🏆 V1 (+0.071) |
| **answer_relevancy** | **0.915** | 0.898 | 🏆 V1 (+0.017) |
| **context_recall**   | 1.000 | 1.000 | Hòa |
| **context_precision**| 0.945 | 0.945 | Hòa |

> Ngưỡng đạt: faithfulness ≥ 0.8 → **cả hai phiên bản đều đạt** (`target_met: true`).

### Vì sao V1 đạt điểm cao hơn?

1. **Faithfulness (V1 thắng rõ rệt, 0.963 vs 0.892).** V1 yêu cầu trả lời ngắn,
   bám sát context → ít "không gian" để mô hình thêm thông tin không có trong tài
   liệu. Ngược lại, V2 yêu cầu trình bày có cấu trúc và nêu *"mức độ chắc chắn"* →
   câu trả lời dài hơn, dễ phát sinh nhận định không được context hỗ trợ trực tiếp,
   kéo faithfulness xuống.

2. **Answer relevancy (V1 nhỉnh hơn, 0.915 vs 0.898).** Câu trả lời súc tích của V1
   tập trung thẳng vào câu hỏi; phần "chi tiết hỗ trợ" và "mức độ chắc chắn" của V2
   tuy chuyên nghiệp nhưng làm loãng độ liên quan trực tiếp với câu hỏi gốc.

3. **Context recall & precision bằng nhau (1.000 và 0.945).** Hai chỉ số này đo
   **chất lượng truy xuất**, không phụ thuộc vào prompt sinh câu trả lời. Vì cả V1
   và V2 dùng chung retriever và cùng bộ câu hỏi nên điểm giống hệt nhau — đây là
   kết quả kỳ vọng, xác nhận rằng khác biệt giữa V1/V2 hoàn toàn đến từ khâu
   generation chứ không phải retrieval.

### Kết luận

**V1 (ngắn gọn) là phiên bản tốt hơn cho bộ dữ liệu này** xét trên cả faithfulness
và answer relevancy. Bài học rút ra: với tác vụ RAG hỏi–đáp dựa trên tài liệu,
prompt yêu cầu câu trả lời súc tích và bám context thường trung thực hơn prompt
yêu cầu diễn giải dài và thêm "lớp" phân tích — vì mỗi câu thừa là một cơ hội cho
thông tin ngoài context lọt vào.
