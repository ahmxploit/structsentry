from __future__ import annotations
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from .models import HealthResponse, ScanResponse, ScanRequest, ChatRequest, ChatResponse, Finding
from .scanner import scan_json_text, scan_yaml_text, scan_csv_text
from .ai import summarize

VERSION = '0.1.0-py313'
app = FastAPI(title='StructSentry', version=VERSION)
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

@app.get('/health', response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status='ok', version=VERSION)

@app.post('/scan', response_model=ScanResponse)
async def scan(text: Optional[str] = Form(None), files: List[UploadFile] | None = None):
    findings = []
    # inline text: try all scanners heuristically
    if text:
        findings += [Finding(source='inline', path=path, line=line, issue=issue, severity=sev, detail=detail)
                     for (name,path,line,issue,sev) in scan_json_text('inline', text)]
        findings += [Finding(source='inline', path=path, line=line, issue=issue, severity=sev, detail=None)
                     for (name,path,line,issue,sev) in scan_yaml_text('inline', text)]
        findings += [Finding(source='inline', path=path, line=line, issue=issue, severity=sev, detail=None)
                     for (name,path,line,issue,sev) in scan_csv_text('inline', text)]
    for f in (files or []):
        try:
            content = (await f.read()).decode('utf-8', errors='ignore')
            fname = f.filename or 'uploaded'
            findings += [Finding(source=fname, path=path, line=line, issue=issue, severity=sev, detail=None)
                         for (name,path,line,issue,sev) in scan_json_text(fname, content)]
            findings += [Finding(source=fname, path=path, line=line, issue=issue, severity=sev, detail=None)
                         for (name,path,line,issue,sev) in scan_yaml_text(fname, content)]
            findings += [Finding(source=fname, path=path, line=line, issue=issue, severity=sev, detail=None)
                         for (name,path,line,issue,sev) in scan_csv_text(fname, content)]
        finally:
            await f.aclose()
    return ScanResponse(findings=findings)

@app.post('/chat', response_model=ChatResponse)
async def chat(req: ChatRequest):
    ans = summarize(req.prompt, req.context)
    return ChatResponse(answer=ans)
