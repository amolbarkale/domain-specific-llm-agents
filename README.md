# Math Tutor Agent - Domain-Specific LLM Implementation

## 🎯 Project Overview

A domain-specific LLM agent designed for math tutoring (Grades 6-10) using advanced prompt engineering strategies. This project demonstrates various prompting techniques and evaluates their effectiveness in educational contexts.

## 📋 Assignment Context

**Course**: Prompt Engineering Lab
**Objective**: Building and Evaluating Domain-Specific LLM Agents
**Domain**: EdTech Math Tutor for Class 6–10

## 🏗️ Project Structure

```
├── README.md (project overview, setup instructions, findings)
├── domain_analysis.md (understanding of domain tasks)
├── prompts/
│   ├── zero_shot.txt
│   ├── few_shot.txt
│   ├── cot_prompt.txt
│   └── meta_prompt.txt
├── evaluation/
│   ├── input_queries.json
│   ├── output_logs.json
│   └── analysis_report.md
├── src/
│   ├── main.py or notebook.ipynb
│   └── utils.py (optional helpers)
└── hallucination_log.md (examples of failure cases)
```

## 🚀 Setup Instructions

### Prerequisites

* Python 3.8+
* Hugging Face Transformers
* Local LLM (TinyLlama-1.1B-Chat) downloaded

### Installation

1. **Install Required Python Libraries**

   ```bash
   pip install transformers torch
   ```

2. **Ensure Local Model is Available**

   * This project uses:

     ```
     google/flan-t5-small
     ```
   * Download it beforehand via:

     ```python
     from transformers import AutoModelForCausalLM, AutoTokenizer
     tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
     model = AutoModelForCausalLM.from_pretrained("google/flan-t5-small")
     ```

3. **Run the Agent**

   ```bash
   python src/main.py
   ```

## 🌟 Domain Tasks Covered

1. **Problem Solving**: Step-by-step mathematical solutions
2. **Concept Explanation**: Breaking down math concepts for students
3. **Error Analysis**: Identifying and correcting student mistakes

## 📊 Prompt Strategies Implemented

* **Zero-shot**: Direct instruction prompting
* **Few-shot**: Example-based learning
* **Chain-of-Thought (CoT)**: Step-by-step reasoning
* **Meta-prompting**: Self-questioning approach

## 🧪 Evaluation Metrics

* **Accuracy**: Correctness of mathematical solutions
* **Reasoning Clarity**: Quality of step-by-step explanations
* **Hallucination Score**: Detection of mathematical errors
* **Consistency**: Reliability across similar problems
* **Age Appropriateness**: Grade-level suitability

## 📈 Key Findings

* Chain-of-thought prompts showed highest accuracy for complex problems
* Few-shot examples improved consistency across problem types
* Meta-prompting excelled in word problem interpretation
* Hallucinations mainly occurred in advanced geometry concepts

## 🔧 Usage

```python
from src.main import MathTutorAgent

# Initialize agent
tutor = MathTutorAgent()

# Run full evaluation
tutor.run_comprehensive_evaluation()
```

## 📁 File Descriptions

* `src/main.py`: Core agent implementation
* `prompts/`: Individual prompt strategy templates
* `evaluation/`: Test queries, results, and analysis
* `domain_analysis.md`: Detailed domain understanding
* `hallucination_log.md`: Documentation of failure cases

## 🎓 Assignment Completion

✅ Domain-specific agent (Math Tutor)
✅ Multiple prompt strategies implemented
✅ Automated evaluation framework
✅ Hallucination detection and logging
✅ Comparative analysis of prompt effectiveness
✅ Complete documentation and findings