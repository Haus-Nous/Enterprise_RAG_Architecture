import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

def capture_demo_assets():
    print("🚀 Initializing Playwright Screenshot Pipeline...")
    
    # Define directories
    screenshot_dir = Path("docs/assets/demo/screenshots")
    slide_dir = Path("docs/assets/demo/slides")
    
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    slide_dir.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Standard HD aspect ratio (1280x720) for slides and viewport
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()
        
        # ----------------------------------------------------
        # STEP 1: Capture Presentation Slides
        # ----------------------------------------------------
        print("📸 Capturing Presentation Slides...")
        slides_path = Path("render_slides.html").absolute().as_uri()
        page.goto(slides_path)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000) # Ensure fonts and CSS are fully rendered
        
        # Capturing Slide 1: Title
        slide1_el = page.query_selector("#slide-title")
        slide1_el.screenshot(path=str(slide_dir / "slide-01-title.png"))
        slide1_el.screenshot(path=str(screenshot_dir / "01-repository-overview.png"))
        print("✅ Saved Slide 1 (Title) & 01-repository-overview.png")
        
        # Capturing Slide 2: Problem Statement
        slide2_el = page.query_selector("#slide-problem")
        slide2_el.screenshot(path=str(slide_dir / "slide-02-problem.png"))
        print("✅ Saved Slide 2 (Problem Statement)")
        
        # Capturing Slide 3: Technical Highlights
        slide3_el = page.query_selector("#slide-highlights")
        slide3_el.screenshot(path=str(slide_dir / "slide-03-highlights.png"))
        print("✅ Saved Slide 3 (Technical Highlights)")
        
        # Capturing Slide 4: Evaluation Results
        slide4_el = page.query_selector("#slide-evaluation")
        slide4_el.screenshot(path=str(slide_dir / "slide-04-evaluation.png"))
        slide4_el.screenshot(path=str(screenshot_dir / "07-evaluation-results.png"))
        print("✅ Saved Slide 4 (Evaluation Results) & 07-evaluation-results.png")
        
        # Capturing Slide 5: Future Roadmap
        slide5_el = page.query_selector("#slide-roadmap")
        slide5_el.screenshot(path=str(slide_dir / "slide-05-roadmap.png"))
        print("✅ Saved Slide 5 (Roadmap)")
        
        # ----------------------------------------------------
        # STEP 2: Capture System Architecture Diagram
        # ----------------------------------------------------
        print("📸 Capturing System Architecture Diagram...")
        mermaid_path = Path("render_mermaid.html").absolute().as_uri()
        page.goto(mermaid_path)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(2000) # Wait for Mermaid rendering engine
        
        # Take full page capture of the diagram to prevent cutoffs
        page.screenshot(path=str(screenshot_dir / "02-system-architecture.png"), full_page=True)
        print("✅ Saved 02-system-architecture.png")
        
        # ----------------------------------------------------
        # STEP 3: Capture Application Walkthrough Experience
        # ----------------------------------------------------
        print("📸 Connecting to active React UI at http://localhost:5173...")
        page.goto("http://localhost:5173")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1000)
        
        # A. Landing Page upload action
        print("Uploading sample company documentation...")
        page.set_input_files("#fileUpload", "data/markdown/sample_company_info.md")
        page.wait_for_timeout(800) # Wait for success animation state
        page.screenshot(path=str(screenshot_dir / "03-upload-workflow.png"))
        print("✅ Saved 03-upload-workflow.png")
        
        # Trigger database indexing sync
        print("Triggering database indexing...")
        page.click('button:has-text("Re-Index Database")')
        page.wait_for_selector('button:has-text("Re-Index Database"):not([disabled])', timeout=30000)
        print("Database sync completed.")
        
        # B. Query Input Interface
        print("Entering search query in input box...")
        query = "What is the steering committee meeting frequency for Project Aegis?"
        page.fill("textarea.chat-input", query)
        page.wait_for_timeout(500)
        page.screenshot(path=str(screenshot_dir / "04-query-interface.png"))
        print("✅ Saved 04-query-interface.png")
        
        # C. Answer Generation
        print("Submitting query & generating answer...")
        page.click("button.send-button")
        
        # Wait for the local Ollama LLM stats block to render (up to 90 seconds in case of slow local CPU run)
        page.wait_for_selector(".exec-stats", timeout=90000)
        page.wait_for_timeout(1000)
        page.screenshot(path=str(screenshot_dir / "05-generated-answer.png"))
        print("✅ Saved 05-generated-answer.png")
        
        # D. Source Citation Display
        print("Expanding sources citation accordion...")
        page.click(".evidence-header")
        page.wait_for_timeout(1000) # Allow sliding animation to complete
        page.screenshot(path=str(screenshot_dir / "06-source-citations.png"))
        print("✅ Saved 06-source-citations.png")
        
        browser.close()
        print("🎉 Demo Asset Pack visual generation pipeline completed successfully!")

if __name__ == "__main__":
    capture_demo_assets()
