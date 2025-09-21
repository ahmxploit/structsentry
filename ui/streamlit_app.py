import os, json, httpx, streamlit as st

BACKEND = os.getenv('BACKEND_URL', 'http://localhost:8000')
st.set_page_config(page_title='StructSentry', layout='wide')
st.title('StructSentry — Structural Data Inspector')

with st.sidebar:
    backend = st.text_input('Backend URL', BACKEND)
    prompt = st.text_area('Ask AI (optional)', placeholder='Summarize findings or suggest fixes…')

tab1, tab2 = st.tabs(['Scan', 'Chat'])

with tab1:
    st.subheader('Upload structured files (JSON/YAML/CSV) or paste text')
    up_files = st.file_uploader('Files', accept_multiple_files=True)
    text = st.text_area('Inline Text', height=200)

    if st.button('Run Scan'):
        with st.spinner('Scanning…'):
            files = []
            for f in up_files or []:
                files.append(('files', (f.name, f.getvalue(), 'text/plain')))
            r = httpx.post(f'{backend}/scan', data={'text': text or ''}, files=files, timeout=120)
            r.raise_for_status()
            res = r.json()
        st.success('Scan complete')
        st.json(res)
        if res.get('findings'):
            st.download_button('Download Findings (JSON)', data=json.dumps(res, indent=2), file_name='findings.json')

with tab2:
    st.subheader('AI Assistant')
    ctx = st.text_area('Context (paste findings JSON)', height=200)
    if st.button('Ask'):
        with st.spinner('Thinking…'):
            r = httpx.post(f'{backend}/chat', json={'prompt': prompt, 'context': ctx}, timeout=120)
            r.raise_for_status()
            ans = r.json().get('answer', '')
        st.write(ans or 'No answer.')
