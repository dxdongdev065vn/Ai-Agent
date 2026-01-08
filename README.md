# LangGraph Planning Agent - Bài tập 1 & 5

Agent hoàn thành Bài tập 1 (Simple Chat) và Bài tập 5 (Planning Agent) về AI Agent với xử lý lỗi toàn diện.

## 📋 Mục lục

- [Bài tập](#bài-tập)
- [Tính năng](#tính-năng)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Xử lý lỗi](#xử-lý-lỗi)
- [Cấu trúc project](#cấu-trúc-project)
- [Testing](#testing)

## 🎯 Bài tập

### Bài 1: CLI Agent đơn giản với chat loop
**Yêu cầu:**
- ✅ Dự án Python
- ✅ Kết nối API LLM (Google AI)
- ✅ Chat loop nhận input người dùng
- ✅ Gửi model và hiển thị output

**File:** `bai1.py`

### Bài 5: Planner → Executor Pipeline
**Yêu cầu:**
- ✅ Planner: tạo step list
- ✅ Executor: gọi tool theo plan with retry/backoff
- ✅ Replan khi error

**File:** `bai5.py`

**Tài liệu tham khảo:**
- https://blog.langchain.com/planning-agents/
- https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/plan-execute-agent/

## ✨ Tính năng

### Bài 1 - Simple Chat Mode
- ✅ Chat loop liên tục
- ✅ Kết nối Google AI API
- ✅ Trả lời trực tiếp, không planning
- ✅ Auto reload API key

### Bài 5 - Planning Mode
- ✅ **Planner**: Phân tích và tạo kế hoạch
- ✅ **Executor**: Thực thi với retry/exponential backoff
- ✅ **Replan**: Tự động lập lại kế hoạch khi lỗi
- ✅ **Synthesis**: Tổng hợp kết quả và trả lời

### Xử lý lỗi toàn diện

#### 1. Lỗi 429 RESOURCE_EXHAUSTED
- ✅ Phát hiện tự động lỗi quota exceeded
- ✅ Retry thông minh với delay từ API
- ✅ Thông báo rõ ràng và hướng dẫn
- ✅ Fallback graceful

#### 2. Lỗi Network/Connection
- ✅ Phát hiện lỗi: getaddrinfo failed, connection error, timeout, DNS
- ✅ Retry tự động với exponential backoff
- ✅ Hướng dẫn khắc phục: internet, VPN, firewall
- ✅ Không crash app

#### 3. Lỗi JSON Parsing
- ✅ Auto clean markdown code blocks
- ✅ Smart extract JSON từ text
- ✅ Fallback plan khi parse lỗi
- ✅ Debug info chi tiết
- ✅ Luôn trả về plan hợp lệ

#### 4. Reload API Key
- ✅ Auto reload trước mỗi request
- ✅ Manual reload bằng lệnh `reload`
- ✅ Không cần restart app
- ✅ Quick switch khi gặp lỗi 429

## 🚀 Cài đặt

### 1. Clone hoặc download project

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Tạo file .env và thêm API key
```bash
# Windows
echo GOOGLE_API_KEY=your_api_key_here > .env
echo GOOGLE_MODEL=gemini-2.5-flash >> .env

# Linux/Mac
echo "GOOGLE_API_KEY=your_api_key_here" > .env
echo "GOOGLE_MODEL=gemini-2.5-flash" >> .env
```

### 4. Lấy Google AI API Key
1. Truy cập: https://makersuite.google.com/app/apikey
2. Đăng nhập với Google account
3. Click "Create API Key"
4. Copy key và paste vào file .env

## 💻 Sử dụng

### Chạy Bài 1 - Simple Chat
```bash
python bai1.py
```

**Ví dụ:**
```
👤 Bạn: Xin chào
🤖 TRỢ LÝ: Xin chào! Tôi có thể giúp gì cho bạn?

👤 Bạn: Giải thích về Python
🤖 TRỢ LÝ: Python là ngôn ngữ lập trình...
```

### Chạy Bài 5 - Planning Agent
```bash
python bai5.py
```

**Ví dụ:**
```
👤 Bạn: Tìm hiểu về AI và ứng dụng

🧠 PLANNER ĐANG SUY NGHĨ...
📋 Kế hoạch đã lập:
   1. Tìm kiếm thông tin về AI
   2. Phân tích các ứng dụng thực tế
   3. Tổng hợp và trả lời

🛠️  EXECUTOR ĐANG LÀM: Tìm kiếm thông tin về AI
   Kết quả: ✅ Đã hoàn thành...

💬 TRỢ LÝ: AI (Artificial Intelligence) là...
```

### Lệnh đặc biệt

#### Reload API key
```
👤 Bạn: reload
✅ Đã reload thành công!
```

#### Thoát
```
👤 Bạn: exit
👋 Tạm biệt! Hẹn gặp lại!
```

## 🔧 Xử lý lỗi

### Lỗi 429 - Quota Exceeded

**Triệu chứng:**
```
❌ Đã vượt quá giới hạn quota API của Google Gemini.
```

**Giải pháp nhanh:**
1. Lấy API key mới: https://makersuite.google.com/app/apikey
2. Cập nhật file .env:
   ```
   GOOGLE_API_KEY=your_new_api_key_here
   ```
3. Gõ `reload` trong chat (KHÔNG CẦN RESTART!)
4. Tiếp tục sử dụng

**Workflow tự động:**
```
   ⚠️  Lỗi 429: Vượt quá giới hạn quota API
   ⏳ API yêu cầu chờ 54.8s trước khi retry...
   🔄 Retry 1/3...
```

### Lỗi Network - getaddrinfo failed

**Triệu chứng:**
```
❌ Lỗi kết nối mạng: [Errno 11001] getaddrinfo failed
```

**Giải pháp:**
1. Kiểm tra internet:
   ```bash
   ping google.com
   ```
2. Tắt VPN/Proxy nếu có
3. Kiểm tra firewall
4. Flush DNS cache:
   ```bash
   ipconfig /flushdns
   ```
5. Đổi DNS sang Google DNS (8.8.8.8, 8.8.4.4)

**Workflow tự động:**
```
   ⚠️  Lỗi kết nối mạng
   💡 Kiểm tra: Kết nối internet, Firewall/VPN, DNS settings
   ⏳ Retry 1/3 sau 1.0s...
```

### Lỗi JSON Parsing

**Triệu chứng:**
```
⚠️  JSON parse error: Expecting value: line 2 column 13
```

**Xử lý tự động:**
- Agent tự động clean markdown code blocks
- Extract JSON từ text có thừa
- Fallback sang plan mặc định nếu cần
- **KHÔNG CẦN LÀM GÌ** - Agent tự xử lý!

**Workflow:**
```
   ⚠️  JSON parse error
   ⚠️  Không thể parse JSON, tạo plan đơn giản
   
📋 Kế hoạch đã lập:
   1. Phân tích yêu cầu
   2. Thực hiện tác vụ
   3. Tổng hợp và trả lời
```

### Quota Limits (Free tier)

| Model | Requests/Day | Requests/Minute |
|-------|--------------|-----------------|
| gemini-2.5-flash | 20 | 2 |
| gemini-1.5-flash | 1,500 | 15 |
| gemini-1.5-pro | 50 | 2 |

**Khuyến nghị:** Sử dụng `gemini-1.5-flash` cho quota cao hơn.

## 📁 Cấu trúc project

```
.
├── bai1.py                 # Bài 1: Simple Chat Agent
├── bai5.py                 # Bài 5: Planning Agent
├── common.py               # Utilities dùng chung
├── .env                    # API key configuration
├── requirements.txt        # Dependencies
├── README.md              # Documentation (file này)
│
├── test_429_handling.py   # Test xử lý lỗi 429
├── test_network_error.py  # Test xử lý lỗi network
├── test_json_parsing.py   # Test xử lý JSON parsing
└── test_reload_key.py     # Test reload API key
```

### File mô tả

#### `common.py`
Chứa các utilities dùng chung:
- `Config`: Quản lý cấu hình và reload API key
- `GoogleAIService`: Base service cho Google AI API
- `RetryConfig`: Cấu hình retry mechanism
- `retry_with_backoff()`: Retry với exponential backoff
- Error detection: `is_network_error()`, `is_quota_exceeded_error()`

#### `bai1.py`
Simple Chat Agent:
- `ChatService`: Service cho chat đơn giản
- Chat loop liên tục
- Auto reload API key
- Xử lý lỗi toàn diện

#### `bai5.py`
Planning Agent:
- `PlanningService`: Service cho planning
- `PlanningAgent`: Agent với Planner → Executor → Replan pipeline
- `AgentState`: State management
- `StepResult`: Kết quả thực thi từng bước

## 🧪 Testing

### Test xử lý lỗi 429
```bash
python test_429_handling.py
```

**Test cases:**
- ✅ Trích xuất retry delay từ error
- ✅ Phát hiện lỗi quota exceeded
- ✅ Retry với lỗi quota (thành công)
- ✅ Retry với lỗi quota vĩnh viễn

### Test xử lý lỗi network
```bash
python test_network_error.py
```

**Test cases:**
- ✅ Phát hiện lỗi network
- ✅ Retry với lỗi network (thành công)
- ✅ Retry với lỗi network vĩnh viễn
- ✅ Xử lý nhiều loại lỗi

### Test xử lý JSON parsing
```bash
python test_json_parsing.py
```

**Test cases:**
- ✅ JSON hợp lệ
- ✅ JSON trong markdown code block
- ✅ JSON với text thừa
- ✅ JSON không hợp lệ (fallback)
- ✅ JSON malformed (fallback)
- ✅ Response rỗng (fallback)
- ✅ JSON với unicode/tiếng Việt

### Test reload API key
```bash
python test_reload_key.py
```

**Test cases:**
- ✅ Reload Config từ .env
- ✅ Reload API key trong Service
- ✅ Workflow thực tế xử lý lỗi 429
- ✅ Switch giữa nhiều keys

## 💡 Tips & Best Practices

### 1. Chuẩn bị backup API keys
```env
# File .env
GOOGLE_API_KEY=key_chinh

# Backup keys (uncomment khi cần)
# GOOGLE_API_KEY=key_backup_1
# GOOGLE_API_KEY=key_backup_2
```

### 2. Workflow khi gặp lỗi 429
1. Gặp lỗi → Không panic!
2. Uncomment key backup trong .env
3. Gõ `reload` trong chat
4. Tiếp tục sử dụng
5. **Không cần restart app!**

### 3. Chọn model phù hợp
- `gemini-2.5-flash`: Mới nhất, quota thấp (20/day)
- `gemini-1.5-flash`: Nhanh, quota cao (1500/day) ⭐ Khuyến nghị
- `gemini-1.5-pro`: Chất lượng cao, quota trung bình (50/day)

### 4. Monitor usage
- Check usage: https://ai.dev/rate-limit
- Docs rate limits: https://ai.google.dev/gemini-api/docs/rate-limits
- Pricing: https://ai.google.dev/pricing

### 5. Troubleshooting nhanh

| Lỗi | Nguyên nhân | Giải pháp |
|-----|-------------|-----------|
| 429 Quota | Hết quota API | Đổi API key, gõ `reload` |
| Network Error | Không có internet/DNS | Kiểm tra kết nối, tắt VPN |
| JSON Parse | Response không đúng format | Agent tự xử lý, không cần làm gì |
| Invalid Key | API key sai | Kiểm tra key trong .env |

## 🎯 Tóm tắt

### Điểm mạnh
- ✅ **2 bài tập riêng biệt**: `bai1.py` và `bai5.py`
- ✅ **Code tối ưu**: Utilities dùng chung trong `common.py`
- ✅ **Xử lý lỗi toàn diện**: 429, Network, JSON, API Key
- ✅ **Auto reload**: Không cần restart khi đổi key
- ✅ **Retry thông minh**: Exponential backoff + API delay
- ✅ **Fallback graceful**: Không crash app
- ✅ **Debug info**: Thông báo rõ ràng, hướng dẫn chi tiết
- ✅ **Testing**: 4 test suites đầy đủ

### Workflow hoàn hảo
1. Chạy agent (`python bai1.py` hoặc `python bai5.py`)
2. Chat bình thường
3. Gặp lỗi → Agent tự động xử lý
4. Nếu cần đổi key → Edit .env → Gõ `reload`
5. Tiếp tục chat
6. Done! 🎉

### Links hữu ích
- **API Key**: https://makersuite.google.com/app/apikey
- **Rate Limits**: https://ai.google.dev/gemini-api/docs/rate-limits
- **Pricing**: https://ai.google.dev/pricing
- **Monitor Usage**: https://ai.dev/rate-limit

---

**Author:** AI Assistant  
**Date:** 2025-01-08  
**Version:** 2.0 - Optimized & Separated
