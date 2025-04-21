import argparse
import requests  # used for fetching content from URLs (e.g., GitHub)
import os
try:
    import pytesseract  # for OCR on images
    from PIL import Image
except ImportError:
    pytesseract = None  # handle case where OCR tools are not installed
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")

os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

if(GEMINI_API_KEY):
    print("API key is connected successfully.")

model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

test_response = model.generate_content("Hello, I am Gemini!")
print(test_response)

def parse_input_files(inputs):
    """
    Read and aggregate content from given input paths or URLs.
    Supports markdown, text, images (with OCR), and GitHub repo URLs.
    Returns a combined text string.
    """
    combined_text = ""
    for item in inputs:
        content = ""
        if item.startswith("http://") or item.startswith("https://"):
            # Handle URLs
            content = fetch_content_from_url(item)
        else:
            # Handle local file paths
            if not os.path.exists(item):
                print(f"Warning: File not found -> {item}")
                continue
            if os.path.isdir(item):
                print(f"Warning: {item} is a directory, skipping.")
                continue
            ext = os.path.splitext(item)[1].lower()
            if ext in [".md", ".markdown", ".txt"]:
                content = read_text_file(item)
            elif ext in [".png", ".jpg", ".jpeg"]:
                content = ocr_image(item)
            else:
                # Unsupported file type for now
                print(f"Note: Skipping unsupported file type {item}")
                continue
        if content:
            # Separate contents of different files for clarity
            combined_text += f"\n\n--- Content from {item} ---\n{content}"
    return combined_text.strip()

def read_text_file(path):
    """Read plain text or markdown file and return its content as text."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            text = f.read()
            # Basic normalization: if markdown, we might remove certain formatting
            # Here we simply return raw text; could integrate markdown-to-text if needed.
            return text
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return ""

def ocr_image(path):
    """Extract text from an image file using OCR (pytesseract)."""
    if pytesseract is None:
        print("OCR support not available (pytesseract not installed). Skipping image:", path)
        return ""
    try:
        img = Image.open(path)
        text = pytesseract.image_to_string(img)
        # Basic cleanup of OCR output
        return text.strip()
    except Exception as e:
        print(f"Error during OCR for image {path}: {e}")
        return ""

def fetch_content_from_url(url):
    """Fetch content from a URL. Handles GitHub repository URLs specially."""
    try:
        if "github.com" in url:
            # If it's a GitHub repo URL (not raw), attempt to get README.md from default branch
            raw_url = None
            if url.endswith("/"):  # remove trailing slash
                url = url[:-1]
            if url.count('/') >= 4:
                # Assume format: https://github.com/owner/repo[/something]
                parts = url.split('/')
                owner = parts[3]
                repo = parts[4] if len(parts) > 4 else ""
                if repo:
                    # Try default branches for README
                    for branch in ["main", "master"]:
                        candidate = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/README.md"
                        resp = requests.get(candidate)
                        if resp.status_code == 200:
                            raw_url = candidate
                            break
            if raw_url is None:
                # Not a straightforward repo main page or README not found, try direct fetch
                resp = requests.get(url)
                if resp.status_code != 200:
                    print(f"Warning: Failed to fetch URL {url} (status {resp.status_code})")
                    return ""
                return resp.text
            else:
                # Fetch the raw README content
                resp = requests.get(raw_url)
                if resp.status_code == 200:
                    return resp.text
                else:
                    print(f"Warning: Failed to fetch README from {raw_url}")
                    return ""
        else:
            # Generic URL (could be raw text or other)
            resp = requests.get(url)
            if resp.status_code == 200:
                # If it's an image URL, we could download and OCR, but not implemented for remote images.
                return resp.text
            else:
                print(f"Warning: Failed to fetch URL {url} (status {resp.status_code})")
                return ""
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return ""

def detect_tech_stack_locally(text):
    """
    Basic heuristic to find tech stack keywords in the text.
    Returns a set of detected technology names.
    """
    tech_keywords = [
        "React", "Angular", "Vue", "Svelte", "JavaScript", "TypeScript",
        "Node.js", "Express", "Django", "Flask", "Ruby on Rails", "Laravel",
        "PHP", "MongoDB", "MySQL", "PostgreSQL", "Docker", "Kubernetes",
        "AWS", "Azure", "GCP", "Kotlin", "Swift", "Android", "iOS", "React Native",
        "Flutter", "Redis", "GraphQL", "REST", "GraphQL", "HTML", "CSS"
    ]
    detected = set()
    text_lower = text.lower()
    for tech in tech_keywords:
        if tech.lower() in text_lower:
            detected.add(tech)
    return detected

def evaluate_tech_stack(stack_list):
    """
    Simple evaluation of tech stack suitability.
    Returns (is_suitable, suggestions_list).
    """
    if not stack_list:
        return True, []  # no tech identified to evaluate
    suggestions = []
    # Example heuristic: suggest modern alternatives if outdated tech is found
    outdated = {"PHP": "Consider using a modern framework (e.g., Django, Node.js) for better scalability.",
                "Laravel": "Laravel is fine for many cases, but ensure to optimize for scalability or consider Node/Django for large scale.",
                "jQuery": "jQuery is outdated for complex apps – consider modern JS frameworks like React or Angular for better maintainability.",
                "Flask": "Flask is lightweight; for large apps, a more scalable framework (Django, FastAPI) or microservices might help."}
    is_suitable = True
    for tech in stack_list:
        # If any tech is in the outdated dict, mark as possibly not ideal
        if tech in outdated:
            is_suitable = False
            suggestions.append(outdated[tech])
    return is_suitable, suggestions

def breakdown_features_into_subtasks(feature_list):
    """
    Placeholder function to break features into subtasks.
    Uses dummy logic for now; in a real scenario this would call Gemini.
    Returns a dict: {feature: [(subtask_desc, story_points, reason), ...], ...}
    """
    subtasks_plan = {}
    for feature in feature_list:
        subtasks = []
        # Dummy subtasks for demonstration
        subtasks.append((f"Design/Plan: {feature}", 1, "Planning and design for this feature (minimal effort)."))
        subtasks.append((f"Implement: {feature}", 5, "Core implementation of this feature (moderate complexity)."))
        subtasks.append((f"Test & Review: {feature}", 3, "Testing and code review (some complexity)."))
        subtasks_plan[feature] = subtasks
    return subtasks_plan

# Placeholder for Gemini API calls
def call_gemini_for_features(text):
    """Simulate calling Gemini API to extract feature ideas from text."""
    # In a real implementation, we would send 'text' with a prompt to Gemini.
    # Here we just simulate by simple heuristic: treat headings or bullet points as features.
    lines = text.splitlines()
    features = []
    for line in lines:
        line_clean = line.strip("-*# ").strip()  # remove bullet or heading markers
        if not line_clean:
            continue
        # Assume lines that start with a capital letter or appear as a short sentence could be features
        if line.startswith("-") or line.startswith("*") or line.startswith("#"):
            features.append(line_clean)
    # Fallback: if none found, consider entire text as one feature (not realistic, but placeholder)
    if not features and text:
        features = [text.strip()[:60] + "..."]  # first 60 chars as a summary
    return features

import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Product Manager AI (Gemini-powered) CLI")
    parser.add_argument('--initial', help="Path to initial feature file (e.g., version 1.1)", required=True)
    parser.add_argument('--additional', help="Path to new client-requested feature file (e.g., version 1.2)", required=False)
    args = parser.parse_args()

    result = {}

    # Process initial features
    initial_text = parse_input_files([args.initial])
    initial_features = call_gemini_for_features(initial_text)
    initial_features = [f for f in initial_features if f]

    # Optionally process additional features
    additional_features = []
    if args.additional:
        additional_text = parse_input_files([args.additional])
        additional_features = call_gemini_for_features(additional_text)
        additional_features = [f for f in additional_features if f]
    else:
        additional_text = ""

    # Detect and evaluate tech stack from both files
    full_text = initial_text + "\n" + additional_text
    detected_stack = detect_tech_stack_locally(full_text)
    tech_stack_list = sorted(detected_stack)
    is_suitable, suggestions = evaluate_tech_stack(tech_stack_list)

    result["tech_stack"] = tech_stack_list
    if not is_suitable:
        result["suggested_alternatives"] = suggestions
    else:
        result["stack_status"] = "Current tech stack appears scalable and robust."

    # Merge features and mark reused ones
    combined_plan = {}
    reused_features = set(initial_features) & set(additional_features)

    # Step 1: Breakdown reused ones (with reduced points)
    for feature in reused_features:
        subtasks = [
            {"task": f"Review existing: {feature}", "points": 1, "reason": "Feature exists from version 1.1. Minor review needed."},
            {"task": f"Enhance: {feature}", "points": 2, "reason": "Build on top of existing implementation."},
            {"task": f"Retest: {feature}", "points": 1, "reason": "Ensure new changes don’t break previous release."}
        ]
        combined_plan[feature + " (updated)"] = subtasks

    # Step 2: Handle new additional features (full points)
    for feature in set(additional_features) - reused_features:
        subtasks = breakdown_features_into_subtasks([feature])[feature]
        combined_plan[feature] = [
            {"task": t, "points": p, "reason": r} for (t, p, r) in subtasks
        ]

    # Step 3: Handle initial-only features if no additional file is passed
    if not args.additional:
        for feature in initial_features:
            subtasks = breakdown_features_into_subtasks([feature])[feature]
            combined_plan[feature] = [
                {"task": t, "points": p, "reason": r} for (t, p, r) in subtasks
            ]

    result["subtasks"] = combined_plan

    # Final JSON Output
    print(json.dumps(result, indent=2))


    
if __name__ == "__main__":
    main()