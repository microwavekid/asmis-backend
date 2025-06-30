# ASMIS Testing Guide - Frontend/Backend Integration

## Quick Start Testing

### 1. Start the Backend
```bash
cd backend
python3 -m uvicorn app.main:app --reload --port 8000
```

### 2. Start the Frontend
```bash
cd frontend-linear
npm run dev
```

### 3. Access the Application
Open your browser to: http://localhost:3000 (or 3001/3002 if port is in use)

## Test Scenarios

### 📊 Scenario 1: View Deal Intelligence Dashboard
1. **Navigate to**: http://localhost:3000/deals
2. **Expected**: 
   - See 3 mock deals displayed in table
   - Summary metrics showing pipeline value, average health
   - Filter options working

### 🔍 Scenario 2: View MEDDPICC Analysis
1. **Action**: Click on any MEDDPICC score badge (e.g., "78%" for Enterprise SaaS)
2. **Expected**:
   - Modal opens with detailed MEDDPICC breakdown
   - Each component shows score, confidence, gaps
   - Evidence pieces displayed for each component
   - Strategic recommendations at bottom

### 📤 Scenario 3: Upload & Analyze New Content
1. **Prepare a test transcript** (save as `test_transcript.txt`):
```
Meeting Transcript - Acme Corp Deal Review
Date: 2024-06-26
Attendees: John (CTO), Sarah (VP Sales)

John: "We need to reduce our deployment costs by at least 30% this year. Our current system is costing us about $2M annually in operational overhead."

Sarah: "The CFO has approved a budget of $500K for new tooling. We need to make a decision by end of Q3."

John: "The main criteria are: ease of integration with our Jenkins pipeline, support for Kubernetes, and 99.99% uptime SLA. We can't afford any more downtime."

Sarah: "We're also looking at GitLab and CircleCI. What makes your solution different?"

John: "If we can prove 6-month ROI, I can champion this internally. The engineering team is really struggling with the current setup."
```

2. **Upload via API** (using curl or Postman):
```bash
curl -X POST "http://localhost:8000/analyze-content" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_transcript.txt"
```

3. **Expected Response**:
```json
{
  "message": "Content analyzed successfully",
  "filename": "test_transcript.txt",
  "source_type": "transcript",
  "analysis_result": {
    "meddpicc_analysis": {
      "metrics": {
        "score": 0.85,
        "confidence": 0.9,
        "details": "30% cost reduction target, $2M current costs",
        "evidence": ["reduce deployment costs by at least 30%"]
      },
      "economic_buyer": {
        "score": 0.75,
        "confidence": 0.85,
        "details": "CFO approved $500K budget",
        "evidence": ["CFO has approved a budget of $500K"]
      },
      // ... other components
    },
    "action_items": [...],
    "stakeholder_map": {...}
  }
}
```

### 🔄 Scenario 4: Test Real-time Updates
1. **Open the deals page** in your browser
2. **In another terminal**, trigger an analysis:
```bash
curl -X POST "http://localhost:8000/api/deals/d1/analyze" \
  -F "file=@test_transcript.txt"
```
3. **Expected**: The UI should update with new analysis data

### 🧪 Scenario 5: Test API Endpoints Directly

#### Get All Deals
```bash
curl http://localhost:8000/api/deals | jq
```

#### Get MEDDPICC Analysis
```bash
curl http://localhost:8000/api/deals/d1/meddpicc | jq
```

#### Get Evidence
```bash
curl http://localhost:8000/api/deals/d1/evidence | jq
```

#### Get Statistics
```bash
curl http://localhost:8000/api/deals/stats | jq
```

## 🐛 Troubleshooting

### Frontend won't load
1. Check console for errors (F12 in browser)
2. Verify backend is running: `curl http://localhost:8000/health`
3. Check CORS errors - frontend port must match backend CORS config

### API returns 404
- Ensure you're using the correct endpoint path
- Check backend logs for errors

### MEDDPICC analysis not showing
1. Check browser Network tab for API calls
2. Verify the deal ID exists in mock data
3. Check for JavaScript errors in console

### Upload fails
- Ensure file is UTF-8 text format
- Check file size (should be under 10MB)
- Verify Anthropic API key is set in backend `.env`

## 📋 Test Checklist

- [ ] Backend starts without errors
- [ ] Frontend loads deal dashboard
- [ ] Deals table displays 3 mock deals
- [ ] Clicking MEDDPICC score opens modal
- [ ] Modal shows all 8 MEDDPICC components
- [ ] Evidence is displayed for each component
- [ ] API endpoints return expected JSON
- [ ] File upload returns analysis
- [ ] No CORS errors in browser console
- [ ] Loading states display properly
- [ ] Error states handle gracefully

## 🎯 Advanced Testing

### Performance Testing
```bash
# Test API response time
time curl http://localhost:8000/api/deals

# Load test with multiple requests
for i in {1..10}; do
  curl http://localhost:8000/api/deals &
done
```

### Test with Real Meeting Transcript
1. Export a real meeting transcript from your system
2. Save as `.txt` file
3. Upload via the analyze endpoint
4. Verify MEDDPICC scores align with meeting content

### Browser Testing
Test in multiple browsers:
- Chrome/Edge
- Firefox  
- Safari

### Mobile Responsiveness
1. Open Chrome DevTools (F12)
2. Toggle device toolbar
3. Test on different screen sizes

## 📊 Expected Test Results

### Successful Integration Signs
✅ No console errors  
✅ API calls complete in <500ms  
✅ UI updates reflect backend data  
✅ MEDDPICC analysis shows realistic scores  
✅ Evidence citations match source content  

### Common Issues & Solutions
| Issue | Solution |
|-------|----------|
| CORS errors | Update backend CORS origins |
| 500 errors | Check backend logs, verify API key |
| Empty results | Ensure mock data is loaded |
| Slow loading | Check network tab for hanging requests |

---

**Pro Tip**: Keep both backend and frontend terminals visible to monitor logs during testing!