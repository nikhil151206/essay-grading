from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from bert_similarity import BERTSimilarity
from rubric_grader import Rubric, KeyPoints, EssayGrader

grading_bp = Blueprint('grading', __name__)

# Initialize the BERT similarity model (this could be optimized to load once)
bert_sim_model = None

def get_bert_model():
    global bert_sim_model
    if bert_sim_model is None:
        bert_sim_model = BERTSimilarity()
    return bert_sim_model

@grading_bp.route('/grade', methods=['POST'])
@cross_origin()
def grade_essay():
    try:
        data = request.get_json()
        
        # Extract data from request
        essay_text = data.get('essay_text', '')
        key_points_data = data.get('key_points', [])
        rubric_data = data.get('rubric', {})
        
        if not essay_text:
            return jsonify({'error': 'Essay text is required'}), 400
        
        if not key_points_data:
            return jsonify({'error': 'Key points are required'}), 400
        
        if not rubric_data:
            return jsonify({'error': 'Rubric is required'}), 400
        
        # Create KeyPoints object
        key_points = KeyPoints(
            topic=key_points_data.get('topic', 'Essay Topic'),
            points=key_points_data.get('points', [])
        )
        
        # Create Rubric object
        rubric = Rubric(
            name=rubric_data.get('name', 'Default Rubric'),
            criteria=rubric_data.get('criteria', [])
        )
        
        # Initialize grader and grade the essay
        bert_model = get_bert_model()
        grader = EssayGrader(bert_model)
        results = grader.grade_essay(essay_text, key_points, rubric)
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in grade_essay: {error_details}")
        return jsonify({'error': str(e), 'details': error_details}), 500

@grading_bp.route('/sample-rubric', methods=['GET'])
@cross_origin()
def get_sample_rubric():
    sample_rubric = {
        "name": "Essay Quality Rubric",
        "criteria": [
            {
                "name": "Content Accuracy",
                "weight": 0.4,
                "scores": {
                    1: "Content is largely inaccurate or irrelevant.",
                    2: "Some content is accurate, but significant inaccuracies exist.",
                    3: "Content is mostly accurate with minor inaccuracies.",
                    4: "Content is highly accurate and relevant."
                }
            },
            {
                "name": "Clarity and Cohesion",
                "weight": 0.3,
                "scores": {
                    1: "Ideas are unclear and disorganized.",
                    2: "Ideas are somewhat clear but lack cohesion.",
                    3: "Ideas are generally clear and cohesive.",
                    4: "Ideas are exceptionally clear, well-organized, and cohesive."
                }
            },
            {
                "name": "Use of Evidence",
                "weight": 0.3,
                "scores": {
                    1: "Little to no relevant evidence provided.",
                    2: "Some evidence provided, but not well-integrated or explained.",
                    3: "Evidence is mostly relevant and adequately explained.",
                    4: "Evidence is highly relevant, well-integrated, and insightful."
                }
            }
        ]
    }
    
    return jsonify(sample_rubric)

@grading_bp.route('/sample-keypoints', methods=['GET'])
@cross_origin()
def get_sample_keypoints():
    sample_keypoints = {
        "topic": "The Importance of Renewable Energy",
        "points": [
            "Renewable energy sources reduce reliance on fossil fuels.",
            "Solar power and wind power are examples of renewable energy.",
            "Renewable energy contributes to mitigating climate change.",
            "Investment in renewable energy creates new jobs and economic opportunities."
        ]
    }
    
    return jsonify(sample_keypoints)

