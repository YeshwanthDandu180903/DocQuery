"""
IBM Knowledge RAG Assistant - Enterprise Production Interface

Professional enterprise-grade web interface for IBM's knowledge retrieval system.
Features official IBM branding, corporate design standards, and enhanced visibility.
"""

import gradio as gr
import time
import json
from datetime import datetime
from typing import Tuple, List, Optional
import os
from pathlib import Path
import base64 
# Import the RAG engine
from query_engine import IBMKnowledgeRAG

# Configuration
APP_TITLE = "IBM Knowledge RAG Assistant"
APP_DESCRIPTION = "Enterprise AI-Powered Knowledge Retrieval System"
APP_SUBTITLE = "Access IBM's comprehensive knowledge base through advanced hybrid retrieval technology"

EXAMPLE_QUESTIONS = [
    "What are IBM's current AI research priorities and focus areas?",
    "How does IBM approach trustworthy AI and responsible AI development?",
    "What workforce analytics insights can help predict employee attrition?",
    "Tell me about IBM's hybrid cloud strategy and innovations",
    "What are the key performance indicators for HR analytics?",
    "How does IBM implement data governance in AI systems?",
    "What are IBM's training methodologies for enterprise AI adoption?",
    "Explain IBM's approach to foundation models and large language models"
]

# Professional IBM CSS with actual hex colors
CUSTOM_CSS = """
/* IBM Professional Enterprise Styling */
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

.gradio-container {
    font-family: 'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif !important;
    background: #1a1a1a !important;
    color: #ffffff !important;
    line-height: 1.5 !important;
}

/* Header with IBM Logo */
.ibm-header {
    background: linear-gradient(135deg, #0f62fe 0%, #002d9c 100%) !important;
    color: white !important;
    padding: 3rem 2rem !important;
    border-radius: 0 !important;
    margin: 0 0 2rem 0 !important;
    position: relative !important;
    overflow: hidden !important;
}

.ibm-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="white" stroke-width="0.5" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
    opacity: 0.3;
    z-index: 1;
}

.ibm-header-content {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 2rem;
}

.ibm-logo {
    width: 80px !important;
    height: 80px !important;
    background: white !important;
    border-radius: 8px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    flex-shrink: 0 !important;
    overflow: hidden !important;
}

.ibm-logo img {
    width: 100% !important;
    height: 100% !important;
    object-fit: contain !important;
}

.ibm-header-text {
    flex: 1;
}

.ibm-header h1 {
    color: white !important;
    font-weight: 600 !important;
    font-size: 2.8rem !important;
    margin: 0 0 0.5rem 0 !important;
    letter-spacing: -0.5px !important;
}

.ibm-header p {
    color: rgba(255, 255, 255, 0.9) !important;
    font-size: 1.3rem !important;
    font-weight: 300 !important;
    margin: 0 !important;
}

.ibm-header .subtitle {
    font-size: 1rem !important;
    opacity: 0.8 !important;
    margin-top: 0.5rem !important;
}

/* Main Content Layout */
.main-content {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 0 2rem !important;
}

/* Question Input Styling */
.question-section {
    background: #2a2a2a !important;
    border: 2px solid #404040 !important;
    border-radius: 12px !important;
    padding: 2rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
}

.question-input textarea {
    border: 2px solid #404040 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    font-size: 1.1rem !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    transition: all 0.3s ease !important;
    background: #1a1a1a !important;
    color: #ffffff !important;
    min-height: 80px !important;
}

.question-input textarea:focus {
    border-color: #0f62fe !important;
    box-shadow: 0 0 0 3px rgba(15, 98, 254, 0.1) !important;
    outline: none !important;
}

/* Buttons */
.btn-primary {
    background: #0f62fe !important;
    color: white !important;
    border: none !important;
    padding: 1rem 2rem !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    text-transform: none !important;
    letter-spacing: 0.5px !important;
}

.btn-primary:hover {
    background: #002d9c !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(15, 98, 254, 0.3) !important;
}

.btn-secondary {
    background: #2a2a2a !important;
    color: #ffffff !important;
    border: 2px solid #404040 !important;
    padding: 1rem 2rem !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
}

.btn-secondary:hover {
    border-color: #0f62fe !important;
    color: #0f62fe !important;
}

/* Results Section */
.results-container {
    background: #2a2a2a !important;
    border: 2px solid #404040 !important;
    border-radius: 12px !important;
    margin-bottom: 2rem !important;
    overflow: hidden !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
}

/* Answer Display */
.answer-section {
    background: #2a2a2a !important;
    padding: 2rem !important;
    border-left: 6px solid #0f62fe !important;
    margin: 0 !important;
    min-height: 200px !important;
}

.answer-section h3 {
    color: #0f62fe !important;
    font-size: 1.4rem !important;
    font-weight: 600 !important;
    margin: 0 0 1.5rem 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

.answer-content {
    font-size: 1.1rem !important;
    line-height: 1.7 !important;
    color: #ffffff !important; 
    white-space: pre-wrap !important;
    word-wrap: break-word !important;
}

/* Sources Display */
.sources-section {
    background: #1a1a1a !important;
    padding: 1.5rem !important;
    border-top: 2px solid #404040 !important;
}

.sources-section h4 {
    color: #ffffff !important; 
    font-size: 1.2rem !important;
    font-weight: 600 !important;
    margin: 0 0 1rem 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

.sources-list {
    list-style: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.sources-list li {
    background: #3a3a3a !important;
    border: 1px solid #505050 !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    padding: 0.8rem !important;
    margin-bottom: 0.5rem !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
}

.sources-list li:hover {
    border-color: #0f62fe !important;
    transform: translateX(4px) !important;
}

/* Metrics Display */
.metrics-section {
    background: #2a2a2a !important;
    padding: 2rem !important;
    border-top: 2px solid #404040 !important;
}

.metrics-grid {
    display: grid !important;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)) !important;
    gap: 1.5rem !important;
}

.metric-card {
    text-align: center !important;
    padding: 1.5rem !important;
    background: #3a3a3a !important;
    border-radius: 8px !important;
    border: 1px solid #505050 !important;
    transition: all 0.3s ease !important;
}

.metric-card:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

.metric-label {
    font-size: 0.9rem !important;
    color: #ffffff !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 0.5rem !important;
}

.metric-value {
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #0f62fe !important;
}

/* Status Messages */
.status-success {
    background: rgba(36, 161, 72, 0.1) !important;
    color: #24a148 !important;
    padding: 1rem !important;
    border-radius: 6px !important;
    border-left: 4px solid #24a148 !important;
    font-weight: 500 !important;
    margin-bottom: 1rem !important;
}

.status-error {
    background: rgba(218, 30, 40, 0.1) !important;
    color: #da1e28 !important;
    padding: 1rem !important;
    border-radius: 6px !important;
    border-left: 4px solid #da1e28 !important;
    font-weight: 500 !important;
    margin-bottom: 1rem !important;
}

.status-info {
    background: rgba(15, 98, 254, 0.1) !important;
    color: #0f62fe !important;
    padding: 1rem !important;
    border-radius: 6px !important;
    border-left: 4px solid #0f62fe !important;
    font-weight: 500 !important;
    margin-bottom: 1rem !important;
}

/* Settings Panel */
.settings-panel {
    background: #2a2a2a !important;
    border: 2px solid #404040 !important;
    border-radius: 12px !important;
    padding: 2rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
}

.settings-panel h3 {
    color: #ffffff !important;
    font-size: 1.3rem !important;
    font-weight: 600 !important;
    margin: 0 0 1.5rem 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
}

/* Example Questions */
.examples-container {
    background: #2a2a2a !important;
    border: 2px solid #404040 !important;
    border-radius: 12px !important;
    padding: 2rem !important;
    margin-bottom: 2rem !important;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
}

.example-question {
    background: #3a3a3a !important;
    border: 1px solid #505050 !important;
    color: #ffffff !important;
    border-radius: 6px !important;
    padding: 1rem !important;
    margin-bottom: 0.8rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    font-size: 0.95rem !important;
}

.example-question:hover {
    border-color: #0f62fe !important;
    background: rgba(15, 98, 254, 0.05) !important;
    transform: translateX(4px) !important;
}

/* Footer */
.footer {
    background: #262626 !important;
    color: white !important;
    text-align: center !important;
    padding: 3rem 2rem !important;
    margin-top: 4rem !important;
    border-radius: 0 !important;
}

.footer p {
    margin: 0.5rem 0 !important;
    opacity: 0.9 !important;
}

/* Responsive Design */
@media (max-width: 768px) {
    .ibm-header {
        padding: 2rem 1rem !important;
    }
    
    .ibm-header-content {
        flex-direction: column !important;
        text-align: center !important;
    }
    
    .ibm-header h1 {
        font-size: 2rem !important;
    }
    
    .main-content {
        padding: 0 1rem !important;
    }
}
"""

def get_logo_base64():
    """Convert logo to base64 for embedding in HTML."""
    logo_path = Path(__file__).parent / "data" / "logo" / "ibm_logo.png"
    if logo_path.exists():
        with open(logo_path, "rb") as f:
            logo_data = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{logo_data}"
    return None

class IBMRAGInterface:
    """Enterprise-grade Gradio interface for IBM Knowledge RAG."""
    
    def __init__(self):
        self.engine: Optional[IBMKnowledgeRAG] = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.query_count = 0
        
    def initialize_engine(self) -> Tuple[str, str]:
        """Initialize the RAG engine with proper error handling."""
        try:
            if self.engine is None:
                self.engine = IBMKnowledgeRAG()
            return "✅ System Initialized Successfully", "status-success"
        except Exception as e:
            error_msg = f"❌ System Initialization Failed: {str(e)}"
            if "GROQ_API_KEY" in str(e):
                error_msg = "❌ GROQ API Key Missing - Please configure your environment"
            return error_msg, "status-error"
    
    def process_question(
        self, 
        question: str, 
        vector_k: int = 5, 
        keyword_k: int = 5,
        include_debug: bool = False
    ) -> Tuple[str, str, str, str, str]:
        """Process a question through the RAG system."""
        if not question.strip():
            return "", "", "", "⚠️ Please enter a question to proceed", ""
        
        try:
            # Initialize engine if needed
            init_status, status_class = self.initialize_engine()
            if "Failed" in init_status:
                return "", "", "", init_status, ""
            
            # Update engine parameters
            self.engine.top_k_vector = vector_k
            self.engine.top_k_keyword = keyword_k
            
            # Process the question
            start_time = time.time()
            answer, sources, latency = self.engine.answer_question(question)
            processing_time = time.time() - start_time
            
            # Increment query counter
            self.query_count += 1
            
            # Format the answer
            formatted_answer = self._format_answer(answer)
            
            # Format sources
            formatted_sources = self._format_sources(sources)
            
            # Create metrics
            metrics = self._create_metrics(latency, processing_time, len(sources))
            
            # Create debug info if requested
            debug_info = ""
            if include_debug:
                debug_info = self._create_debug_info(question, vector_k, keyword_k, sources)
            
            # Status message
            status_msg = f"✅ Query {self.query_count} completed successfully • {len(sources)} sources retrieved"
            
            return formatted_answer, formatted_sources, metrics, status_msg, debug_info
            
        except Exception as e:
            error_msg = f"❌ Processing Error: {str(e)}"
            return "", "", "", error_msg, ""
    
    def _format_answer(self, answer: str) -> str:
        """Format the answer with professional styling."""
        if not answer:
            return """
            <div class="answer-section">
                <h3>📋 Answer</h3>
                <div class="answer-content">No answer generated. Please try a different question.</div>
            </div>
            """
        
        # Clean and format the answer
        formatted = answer.strip()
        formatted_with_breaks = formatted.replace('\n', '<br>')
        
        html_answer = f"""
        <div class="answer-section">
            <h3>💡 Answer</h3>
            <div class="answer-content">{formatted_with_breaks}</div>
        </div>
        """
        return html_answer
    
    def _format_sources(self, sources: List[str]) -> str:
        """Format sources with professional styling."""
        if not sources:
            return """
            <div class="sources-section">
                <h4>📚 Sources</h4>
                <p style="color: #ffffff;">No sources found for this query.</p>
            </div>
            """
        
        sources_items = ""
        for i, source in enumerate(sources[:15], 1):  # Show up to 15 sources
            sources_items += f"""
            <li>
                <strong>Source {i:02d}:</strong> {source}
            </li>
            """
        
        sources_html = f"""
        <div class="sources-section">
            <h4>📚 Sources ({len(sources)})</h4>
            <ul class="sources-list">
                {sources_items}
            </ul>
        </div>
        """
        return sources_html
    
    def _create_metrics(self, latency: float, processing_time: float, source_count: int) -> str:
        """Create professional performance metrics display."""
        metrics_html = f"""
        <div class="metrics-section">
            <h4 style="color: #ffffff; margin-bottom: 2rem; font-size: 1.3rem; font-weight: 600;">
                ⚡ Performance Analytics
            </h4>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-label">Engine Latency</div>
                    <div class="metric-value">{latency:.2f}s</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Total Processing</div>
                    <div class="metric-value">{processing_time:.2f}s</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Sources Found</div>
                    <div class="metric-value">{source_count}</div>
                </div>
                <div class="metric-card">
                    <div class="metric-label">Session Queries</div>
                    <div class="metric-value">{self.query_count}</div>
                </div>
            </div>
        </div>
        """
        return metrics_html

    def _create_debug_info(self, question: str, vector_k: int, keyword_k: int, sources: List[str]) -> str:
        """Create technical debug information."""
        debug_html = f"""
        <div style="background: #2a2a2a; border: 2px solid #404040; border-radius: 8px; padding: 2rem; margin-top: 1rem;">
            <h4 style="color: #ffffff; margin-bottom: 1rem;">🔍 Technical Debug Information</h4>
            <div style="background: #3a3a3a; color: #ffffff; padding: 1.5rem; border-radius: 6px; font-family: 'IBM Plex Mono', monospace;">
                <strong>Query:</strong> {question}<br>
                <strong>Vector Search K:</strong> {vector_k}<br>
                <strong>Keyword Search K:</strong> {keyword_k}<br>
                <strong>Sources Retrieved:</strong> {len(sources)}<br>
                <strong>Session ID:</strong> {self.session_id}<br>
                <strong>Timestamp:</strong> {datetime.now().isoformat()}<br>
                <strong>Processing Mode:</strong> Hybrid Retrieval (Vector + BM25)
            </div>
        </div>
        """
        return debug_html
    
    def create_interface(self) -> gr.Blocks:
        """Create the enterprise Gradio interface."""
        
        with gr.Blocks(
            css=CUSTOM_CSS,
            title=f"IBM Knowledge RAG • {self.session_id}",
            theme=gr.themes.Soft()
        ) as interface:
            
            # IBM Header with Logo
            logo_base64 = get_logo_base64()
            logo_html = f'<img src="{logo_base64}" alt="IBM Logo" />' if logo_base64 else 'IBM'

            gr.HTML(f"""
            <div class="ibm-header">
                <div class="ibm-header-content">
                    <div class="ibm-logo">
                        {logo_html}
                    </div>
                    <div class="ibm-header-text">
                        <h1>{APP_TITLE}</h1>
                        <p>{APP_DESCRIPTION}</p>
                        <div class="subtitle">{APP_SUBTITLE}</div>
                    </div>
                </div>
            </div>
            """)
            
            # Main Content
            with gr.Column(elem_classes=["main-content"]):
                
                # Question Input Section
                with gr.Column(elem_classes=["question-section"]):
                    question_input = gr.Textbox(
                        label="💬 Ask Your Question",
                        placeholder="Enter your question about IBM's AI research, technologies, cloud strategies, or HR analytics...",
                        lines=4,
                        elem_classes=["question-input"],
                        scale=1
                    )
                    
                    # Action Buttons
                    with gr.Row():
                        submit_btn = gr.Button(
                            "🔍 Submit Question", 
                            variant="primary",
                            elem_classes=["btn-primary"],
                            scale=2
                        )
                        clear_btn = gr.Button(
                            "🗑️ Clear", 
                            variant="secondary",
                            elem_classes=["btn-secondary"],
                            scale=1
                        )
                
                # Two Column Layout
                with gr.Row():
                    # Left Column - Settings & Examples
                    with gr.Column(scale=1):
                        # Advanced Settings
                        with gr.Accordion("⚙️ Advanced Configuration", open=False):
                            with gr.Column(elem_classes=["settings-panel"]):
                                vector_k = gr.Slider(
                                    minimum=1, maximum=20, value=5, step=1,
                                    label="Vector Search Results (K)",
                                    info="Number of semantically similar documents to retrieve"
                                )
                                keyword_k = gr.Slider(
                                    minimum=1, maximum=20, value=5, step=1,
                                    label="Keyword Search Results (K)", 
                                    info="Number of keyword-matched documents to retrieve"
                                )
                                include_debug = gr.Checkbox(
                                    label="Enable Debug Mode",
                                    value=False,
                                    info="Show technical processing details"
                                )
                        
                        # Example Questions
                        with gr.Accordion("💡 Example Questions", open=False):
                            with gr.Column(elem_classes=["examples-container"]):
                                gr.HTML("<h4 style='color: #ffffff;'>Select a sample question:</h4>")
                                example_dropdown = gr.Dropdown(
                                    choices=EXAMPLE_QUESTIONS,
                                    label="Choose Example",
                                    value=None,
                                    interactive=True
                                )
                    
                    # Right Column - Results
                    with gr.Column(scale=2):
                        # Status Display
                        status_display = gr.HTML(
                            value='<div class="status-info">💡 System ready to process your questions</div>'
                        )
                        
                        # Results Tabs
                        with gr.Tabs():
                            with gr.Tab("📋 Answer"):
                                answer_output = gr.HTML(
                                    value="",
                                    elem_classes=["results-container"]
                                )
                            
                            with gr.Tab("📚 Sources"):
                                sources_output = gr.HTML(
                                    value="",
                                    elem_classes=["results-container"]
                                )
                            
                            with gr.Tab("⚡ Metrics"):
                                metrics_output = gr.HTML(
                                    value="",
                                    elem_classes=["results-container"]
                                )
                            
                            with gr.Tab("🔍 Debug"):
                                debug_output = gr.HTML(
                                    value="",
                                    elem_classes=["results-container"]
                                )
            
            # Professional Footer
            gr.HTML(f"""
            <div class="footer">
                <p><strong>IBM Knowledge RAG Assistant</strong> • Session {self.session_id}</p>
                <p>Enterprise-grade AI knowledge retrieval powered by hybrid search technology</p>
                <p style="font-size: 0.9rem; opacity: 0.7;">
                    Built with IBM Watson principles • Secure • Scalable • Responsible AI
                </p>
            </div>
            """)
            
            # Event Handlers
            def handle_submit(question, vector_k_val, keyword_k_val, debug_flag):
                return self.process_question(question, vector_k_val, keyword_k_val, debug_flag)
            
            def handle_example_select(example):
                return example if example else ""
            
            def handle_clear():
                return "", "", "", "", '<div class="status-info">💡 Ready for your next question</div>', ""
            
            # Connect Events
            submit_btn.click(
                fn=handle_submit,
                inputs=[question_input, vector_k, keyword_k, include_debug],
                outputs=[answer_output, sources_output, metrics_output, status_display, debug_output]
            )
            
            question_input.submit(
                fn=handle_submit,
                inputs=[question_input, vector_k, keyword_k, include_debug],
                outputs=[answer_output, sources_output, metrics_output, status_display, debug_output]
            )
            
            example_dropdown.change(
                fn=handle_example_select,
                inputs=[example_dropdown],
                outputs=[question_input]
            )
            
            clear_btn.click(
                fn=handle_clear,
                outputs=[question_input, answer_output, sources_output, metrics_output, status_display, debug_output]
            )
        
        return interface

def main():
    """Launch the enterprise IBM Knowledge RAG interface."""
    print("\n" + "="*80)
    print(f"🚀 LAUNCHING {APP_TITLE}")
    print("="*80)
    print(f"📊 Enterprise Interface: http://127.0.0.1:7861")
    print(f"🔐 Session ID: {datetime.now().strftime('%Y%m%d_%H%M%S')}")
    print(f"⚡ Hybrid Search Engine: Vector Similarity + BM25 Keyword Search")
    print(f"🤖 AI Model: Groq LLaMA Integration")
    print("="*80)
    
    # Initialize the interface
    rag_interface = IBMRAGInterface()
    interface = rag_interface.create_interface()
    
    # Launch configuration for enterprise deployment
    launch_config = {
        "server_name": "127.0.0.1",
        "server_port": 7861,
        "share": True,  # Set to True for external access
        "show_error": True,
        "quiet": False,
        "max_threads": 10,
        "favicon_path": None,  # Could add IBM favicon here
    }
    
    # Launch the interface
    interface.launch(**launch_config)

if __name__ == "__main__":
    main()