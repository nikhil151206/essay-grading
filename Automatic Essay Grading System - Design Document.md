# Automatic Essay Grading System - Design Document

## 1. Introduction
This document outlines the design for an automatic essay grading system. The system will leverage BERT for semantic understanding of text, cosine similarity for comparing student responses with key points, and a custom rubric system for generating grades and feedback.

## 2. System Architecture

### 2.1. Overview
The system will consist of the following main components:
- **Web Interface (Frontend):** For users to upload essays, define rubrics, and view grades/feedback.
- **Backend API (Flask):** To handle requests from the frontend, manage data, and orchestrate the grading process.
- **Text Processing Module:** Utilizes BERT to generate embeddings for essays and key points.
- **Similarity Calculation Module:** Computes cosine similarity between essay embeddings and key point embeddings.
- **Rubric and Grading Module:** Applies custom rubrics to similarity scores to determine grades and generate feedback.
- **Database:** Stores rubrics, key points, student essays, and grading results.

### 2.2. Component Details

#### 2.2.1. Web Interface (Frontend)
- Built using React.
- Allows users to:
    - Upload student essays (e.g., plain text, PDF).
    - Define and manage custom rubrics (criteria, weighting, scoring guidelines).
    - Input key points for specific essay prompts.
    - View graded essays with scores and detailed feedback.

#### 2.2.2. Backend API (Flask)
- Provides RESTful APIs for frontend communication.
- Handles:
    - User authentication and authorization.
    - Essay submission and storage.
    - Rubric and key point management.
    - Triggering the grading process.
    - Retrieving grading results.

#### 2.2.3. Text Processing Module
- **BERT Model:** Will use a pre-trained BERT model (e.g., `bert-base-uncased` or `sentence-transformers/bert-base-nli-mean-tokens`) to convert text (essays, key points) into high-dimensional vector embeddings.
- **Tokenization:** Text will be tokenized before being fed into the BERT model.
- **Embedding Generation:** The module will generate sentence or document embeddings suitable for similarity comparison.

#### 2.2.4. Similarity Calculation Module
- **Cosine Similarity:** This module will calculate the cosine similarity between the BERT embeddings of student essay segments and the embeddings of predefined key points.
- The output will be a similarity score (0 to 1) indicating how closely a student's response aligns with each key point.

#### 2.2.5. Rubric and Grading Module
- **Custom Rubrics:** Users will define rubrics with:
    - **Criteria:** Specific aspects of the essay to be graded (e.g., 

thesis, evidence, organization, grammar).
    - **Weighting:** Importance of each criterion.
    - **Scoring Guidelines:** Descriptors for different score levels for each criterion.
- **Grading Logic:** This module will:
    - Map the cosine similarity scores to the rubric's scoring guidelines.
    - Calculate an overall score based on criterion weighting.
    - Generate qualitative feedback based on the rubric descriptors and areas of low similarity.

#### 2.2.6. Database
- Stores:
    - User information.
    - Rubric definitions.
    - Key points for different assignments.
    - Student essays.
    - Grading results (scores, feedback, similarity details).
- PostgreSQL or SQLite will be considered for implementation.

## 3. Technologies Used
- **Backend:** Python, Flask, PyTorch/TensorFlow (for BERT), scikit-learn (for cosine similarity).
- **Frontend:** React, HTML, CSS, JavaScript.
- **Database:** PostgreSQL/SQLite.
- **Deployment:** Docker, potentially cloud platforms (AWS, GCP, Azure).

## 4. Workflow
1. **User defines assignment:** Teacher creates an assignment, uploads key points, and defines a custom rubric.
2. **Student submits essay:** Student uploads their essay through the web interface.
3. **Essay processing:** The backend receives the essay, tokenizes it, and generates BERT embeddings.
4. **Similarity calculation:** The essay embeddings are compared with key point embeddings using cosine similarity.
5. **Grading:** The rubric and grading module uses similarity scores to calculate a grade and generate feedback.
6. **Results display:** The grade and feedback are stored in the database and displayed to the teacher via the web interface.

## 5. Future Enhancements
- Support for multiple languages.
- Integration with Learning Management Systems (LMS).
- More sophisticated feedback generation using generative AI.
- Plagiarism detection.
- Real-time grading feedback.


