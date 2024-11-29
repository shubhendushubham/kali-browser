import streamlit as st
import markdown
from graphviz import Digraph
import pdfkit
import base64

def parse_markdown(file_content):
    html = markdown.markdown(file_content)
    return html

def create_mindmap(data):
    dot = Digraph(comment='Mindmap')
    dot.attr(bgcolor='lightyellow')
    dot.node('A', 'Root', color='red', style='filled', fillcolor='lightblue')
    dot.node('B', 'Child 1', color='green', style='filled', fillcolor='lightgreen')
    dot.node('C', 'Child 2', color='blue', style='filled', fillcolor='lightpink')
    dot.edges(['AB', 'AC'])
    return dot

def export_mindmap(dot, file_format):
    output_path = f'mindmap.{file_format}'
    dot.render(output_path, format=file_format)
    return output_path

def download_link(file_path, file_label):
    with open(file_path, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:file/{file_path.split(".")[-1]};base64,{b64}" download="{file_path}">{file_label}</a>'
    return href

st.title('Markdown to Mindmap Converter')
uploaded_file = st.file_uploader('Upload a Markdown file', type=['md'])

if uploaded_file is not None:
    file_content = uploaded_file.read().decode('utf-8')
    st.markdown('### Markdown Content')
    st.text(file_content)

    st.markdown('### Mindmap')
    html_content = parse_markdown(file_content)
    mindmap = create_mindmap(html_content)
    st.graphviz_chart(mindmap.source)

    st.markdown('### Export Mindmap')
    file_format = st.selectbox('Select file format', ['pdf', 'svg', 'html'])
    if st.button('Export'):
        output_path = export_mindmap(mindmap, file_format)
        st.markdown(download_link(output_path, f'Download {file_format.upper()}'), unsafe_allow_html=True)
