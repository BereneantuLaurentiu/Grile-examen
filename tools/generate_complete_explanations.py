#!/usr/bin/env python3
"""
Enhanced PDF Question Explanation Generator

This script extracts questions from CulegereLicenta_2025_ro.pdf and generates
explanations for correct answers only, properly parsing all sections.
"""

import re
import os
import subprocess
from typing import Dict, List, Tuple


def extract_pdf_text(pdf_path: str) -> str:
    """Extract text from PDF using pdftotext."""
    try:
        result = subprocess.run(['pdftotext', pdf_path, '-'], 
                              capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        print("Error extracting PDF. Make sure pdftotext is installed.")
        return ""


def find_answer_key_structure(text: str) -> Dict:
    """Find and parse the complete answer key structure."""
    lines = text.split('\n')
    answers = {
        "topic1": {},  # Structuri discrete și algoritmi
        "topic2": {},  # Limbaje de programare și inginerie software  
        "topic3": {}   # Sisteme de calcul
    }
    
    # Find all answer sections
    in_answers = False
    current_section = None
    
    for line in lines:
        line = line.strip()
        
        if "Răspunsuri" in line:
            in_answers = True
            continue
            
        if not in_answers:
            continue
            
        # Identify sections
        if "Algoritmi s, i structuri de date" in line or "Teoria grafurilor" in line or "Logică" in line:
            current_section = "topic1"
            continue
        elif "Limbaje de programare" in line or "Inginerie" in line or "Baze de date" in line:
            current_section = "topic2"
            continue
        elif "Arhitectura calculatoarelor" in line or "Sisteme de operare" in line or "Ret, ele de calculatoare" in line:
            current_section = "topic3"
            continue
            
        # Parse answer lines
        match = re.match(r'^(\d+)\.\s*\(([a-e,\s\)]+)\)', line)
        if match and current_section:
            q_num = match.group(1)
            answer_text = match.group(2).replace(')', '').replace(' ', '')
            if current_section not in answers:
                answers[current_section] = {}
            answers[current_section][q_num] = answer_text
    
    return answers


def extract_questions_by_topic(text: str) -> Dict:
    """Extract questions organized by topic."""
    questions = {
        "topic1": [],  # Structuri discrete și algoritmi
        "topic2": [],  # Limbaje de programare și inginerie software
        "topic3": []   # Sisteme de calcul
    }
    
    lines = text.split('\n')
    current_topic = None
    current_question = None
    question_text = []
    options = {}
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and page markers
        if not line or line.isdigit():
            continue
            
        # Identify topic sections
        if "Algoritmi s, i structuri de date" in line:
            current_topic = "topic1"
            continue
        elif ("Programare proceduală" in line or "Programarea orientată" in line or 
              "Baze de date" in line or "Ingineria software" in line):
            current_topic = "topic2"
            continue
        elif ("Arhitectura calculatoarelor" in line or "Sisteme de operare" in line or 
              "Ret, ele de calculatoare" in line):
            current_topic = "topic3"
            continue
            
        # Skip header repetitions
        if any(header in line for header in ["STRUCTURI DISCRETE", "LIMBAJE DE PROGRAMARE", "SISTEME DE CALCUL"]):
            continue
            
        # Check for question start
        question_match = re.match(r'^(\d+)\.\s*(.*)', line)
        if question_match and current_topic:
            # Save previous question
            if current_question is not None and question_text:
                questions[current_topic].append({
                    'number': current_question,
                    'text': ' '.join(question_text).strip(),
                    'options': options.copy()
                })
            
            # Start new question
            current_question = question_match.group(1)
            question_text = [question_match.group(2)]
            options = {}
            continue
            
        # Check for option
        option_match = re.match(r'^\(([a-e])\)\s*(.*)', line)
        if option_match and current_question is not None and current_topic:
            option_letter = option_match.group(1)
            option_text = option_match.group(2)
            options[option_letter] = option_text
            continue
            
        # Continue question or option text
        if current_question is not None and current_topic:
            if line and not line.startswith('def '):  # Skip function definitions on separate lines
                question_text.append(line)
    
    # Save last question
    if current_question is not None and question_text and current_topic:
        questions[current_topic].append({
            'number': current_question,
            'text': ' '.join(question_text).strip(),
            'options': options.copy()
        })
    
    return questions


def generate_enhanced_explanation(question: Dict, correct_options: List[str], topic: str) -> Dict[str, str]:
    """Generate enhanced explanations based on topic and question content."""
    explanations = {}
    
    for option in correct_options:
        if option not in question['options']:
            continue
            
        option_text = question['options'][option]
        question_text = question['text'].lower()
        option_lower = option_text.lower()
        
        # Topic-specific explanations
        if topic == "topic1":  # Structuri discrete și algoritmi
            explanation = generate_algorithms_explanation(question_text, option_text, option_lower)
        elif topic == "topic2":  # Limbaje de programare
            explanation = generate_programming_explanation(question_text, option_text, option_lower)
        elif topic == "topic3":  # Sisteme de calcul
            explanation = generate_systems_explanation(question_text, option_text, option_lower)
        else:
            explanation = "Răspunsul este corect conform principiilor teoretice din domeniu."
            
        explanations[option] = explanation
    
    return explanations


def generate_algorithms_explanation(question_text: str, option_text: str, option_lower: str) -> str:
    """Generate explanations for algorithms and data structures questions."""
    
    if "complexitate" in question_text:
        if "o(n²)" in option_lower or "o(n2)" in option_lower:
            return "Bucla exterioară și interioară determină complexitate pătratică."
        elif "o(n)" in option_lower:
            return "Algoritmul parcurge liniar structura de date, rezultând complexitate liniară."
        elif "o(log n)" in option_lower:
            return "Strategia divide-et-impera reduce spațiul de căutare la jumătate în fiecare pas."
    
    if "algoritm" in question_text and "returnează" in option_lower:
        return "Logica algoritmului corespunde cerințelor prin implementarea sa pas cu pas."
    
    if "sortare" in question_text:
        if "crescător" in option_lower:
            return "Algoritmul aranjează elementele în ordine ascendentă prin comparări succesive."
        elif "descrescător" in option_lower:
            return "Algoritmul aranjează elementele în ordine descendentă prin comparări succesive."
    
    if "graf" in question_text or "arbore" in question_text:
        return "Proprietatea este fundamentală în teoria grafurilor și structurilor arborescente."
    
    if "recursiv" in question_text:
        return "Funcția se autoapelează cu parametri reduși până la cazul de bază."
    
    return "Algoritmul respectă principiile fundamentale ale informaticii teoretice."


def generate_programming_explanation(question_text: str, option_text: str, option_lower: str) -> str:
    """Generate explanations for programming and software engineering questions."""
    
    if "orientat" in question_text and "obiect" in question_text:
        if "încapsulare" in option_lower:
            return "Încapsularea ascunde detaliile de implementare și protejează datele interne."
        elif "moștenire" in option_lower:
            return "Moștenirea permite reutilizarea codului prin extinderea claselor existente."
        elif "polimorfism" in option_lower:
            return "Polimorfismul permite tratarea uniformă a obiectelor de tipuri diferite."
    
    if "baze de date" in question_text or "sql" in question_text:
        if "normalizare" in option_lower or "normală" in option_lower:
            return "Normalizarea elimină redundanța și asigură consistența datelor."
        elif "cheie" in option_lower:
            return "Cheile asigură unicitatea și integritatea referențială în baza de date."
    
    if "java" in question_text or "python" in question_text or "c++" in question_text:
        return "Caracteristica este specifică semanticii și sintaxei limbajului de programare."
    
    if "design pattern" in question_text or "arhitectur" in question_text:
        return "Pattern-ul oferă o soluție reutilizabilă pentru o problemă comună de design."
    
    return "Principiul este fundamental în dezvoltarea software modernă."


def generate_systems_explanation(question_text: str, option_text: str, option_lower: str) -> str:
    """Generate explanations for computer systems questions."""
    
    if "protocol" in question_text or "tcp" in question_text or "osi" in question_text:
        if "tcp" in option_lower and "fiabil" in option_lower:
            return "TCP folosește mecanisme de control al erorilor și retransmisie pentru fiabilitate."
        elif "udp" in option_lower and "rapid" in option_lower:
            return "UDP oferă transmisie rapidă fără garanții, fiind eficient pentru aplicații real-time."
        return "Protocolul îndeplinește funcții specifice în arhitectura de rețea stratificată."
    
    if "cache" in question_text or "memorie" in question_text:
        return "Cache-ul îmbunătățește performanța prin păstrarea datelor frecvent accesate aproape de procesor."
    
    if "planificare" in question_text or "scheduler" in question_text:
        return "Algoritmul de planificare optimizează utilizarea CPU-ului și timpul de răspuns."
    
    if "sistem de operare" in question_text:
        return "Funcționalitatea este esențială pentru gestionarea resurselor și serviciilor sistemului."
    
    if "arhitectur" in question_text:
        return "Componenta face parte din arhitectura standard a sistemelor de calcul moderne."
    
    if "rețea" in question_text or "internet" in question_text:
        return "Conceptul este fundamental în comunicarea și organizarea rețelelor de calculatoare."
    
    return "Principiul este esențial în funcționarea sistemelor de calcul contemporane."


def create_complete_markdown(questions: Dict, answers: Dict) -> str:
    """Create comprehensive markdown with all questions and explanations."""
    
    topic_titles = {
        "topic1": "Structuri discrete și algoritmi",
        "topic2": "Limbaje de programare și inginerie software", 
        "topic3": "Sisteme de calcul"
    }
    
    markdown = "# Explicații pentru Culegerea de Licență 2025 - Informatică\n\n"
    markdown += "*Explicații pentru variantele corecte de răspuns*\n\n"
    
    for topic_key, topic_title in topic_titles.items():
        markdown += f"## Tematica {topic_key[-1]}: {topic_title}\n\n"
        
        topic_questions = questions.get(topic_key, [])
        topic_answers = answers.get(topic_key, {})
        
        for question in topic_questions:
            q_num = question['number']
            correct_answers = topic_answers.get(q_num, "")
            
            if not correct_answers:
                continue
                
            # Parse correct options
            correct_options = [opt.strip() for opt in correct_answers.split(',') if opt.strip()]
            
            markdown += f"### Întrebarea {q_num}\n"
            markdown += f"{question['text']}\n\n"
            
            # Generate explanations
            explanations = generate_enhanced_explanation(question, correct_options, topic_key)
            
            for option in correct_options:
                if option in question['options']:
                    option_text = question['options'][option]
                    markdown += f"**Varianta {option.upper()}**: {option_text}\n\n"
                    
                    if option in explanations:
                        markdown += f"*Explicație*: {explanations[option]}\n\n"
                    
            markdown += "---\n\n"
    
    return markdown


def main():
    """Main function to process the PDF and generate explanations."""
    
    # Paths
    pdf_path = "../CulegereLicenta_2025_ro.pdf"
    markdown_output = "../Explicatii_CulegereLicenta_2025_Complete.md"
    pdf_output = "../Explicatii_CulegereLicenta_2025_Complete.pdf"
    
    print("Extracting text from PDF...")
    text = extract_pdf_text(pdf_path)
    
    if not text:
        print("Failed to extract text from PDF")
        return
    
    print("Parsing answer key...")
    answers = find_answer_key_structure(text)
    
    print("Extracting questions by topic...")
    questions = extract_questions_by_topic(text)
    
    print("Generating comprehensive markdown...")
    markdown_content = create_complete_markdown(questions, answers)
    
    print("Saving markdown file...")
    with open(markdown_output, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print("Creating PDF...")
    try:
        # Fix unicode characters for LaTeX
        clean_content = markdown_content.replace('≤', '<=').replace('−', '-').replace('≥', '>=')
        clean_content = clean_content.replace('∪', 'U').replace('∩', 'I').replace('∈', 'in')
        clean_content = clean_content.replace('∀', 'for all').replace('∃', 'exists').replace('→', '->')
        clean_content = clean_content.replace('↔', '<->').replace('¬', 'NOT').replace('∧', 'AND')
        clean_content = clean_content.replace('∨', 'OR').replace('⊆', 'subset of').replace('⊇', 'superset of')
        
        with open(markdown_output, 'w', encoding='utf-8') as f:
            f.write(clean_content)
            
        result = subprocess.run([
            'pandoc', markdown_output, '-o', pdf_output,
            '--pdf-engine=pdflatex', '--variable', 'geometry:margin=2cm',
            '-V', 'mainfont="DejaVu Sans"'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"PDF generation warning: {result.stderr}")
        
    except Exception as e:
        print(f"Error creating PDF: {e}")
    
    print(f"Done! Generated files:")
    print(f"- {markdown_output}")
    if os.path.exists(pdf_output):
        print(f"- {pdf_output}")
    
    # Print summary
    total_questions = sum(len(topic_questions) for topic_questions in questions.values())
    total_with_answers = sum(len(topic_answers) for topic_answers in answers.values())
    
    print(f"\nProcessed {total_questions} questions across 3 topics.")
    print(f"Found answers for {total_with_answers} questions.")
    
    for topic_key, topic_questions in questions.items():
        topic_num = topic_key[-1]
        print(f"- Topic {topic_num}: {len(topic_questions)} questions")


if __name__ == "__main__":
    main()