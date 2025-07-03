from bert_similarity import BERTSimilarity

class Rubric:
    def __init__(self, name, criteria):
        self.name = name
        self.criteria = criteria  # List of dictionaries: [{'name': 'Criterion Name', 'weight': 0.X, 'scores': {0: 'Poor', 1: 'Fair', ...}}]

class KeyPoints:
    def __init__(self, topic, points):
        self.topic = topic
        self.points = points  # List of strings, each representing a key point

class EssayGrader:
    def __init__(self, bert_similarity_model):
        self.bert_sim = bert_similarity_model

    def grade_essay(self, essay_text, key_points_obj, rubric_obj):
        results = {}
        total_weighted_score = 0
        feedback_messages = []

        for criterion in rubric_obj.criteria:
            criterion_name = criterion["name"]
            criterion_weight = criterion["weight"]
            criterion_scores_map = criterion["scores"]
            
            criterion_raw_score = 0
            criterion_feedback_detail = []
            
            key_point_similarities = []
            for kp in key_points_obj.points:
                similarity = self.bert_sim.calculate_similarity(essay_text, kp)
                # Convert numpy float32 to Python float for JSON serialization
                key_point_similarities.append(float(similarity))
            
            if not key_point_similarities:
                avg_similarity = 0
            else:
                avg_similarity = sum(key_point_similarities) / len(key_point_similarities)
            
            # More granular mapping of average similarity to a score (e.g., 1-4 scale)
            if avg_similarity >= 0.9:
                criterion_raw_score = 4 # Excellent
            elif avg_similarity >= 0.7:
                criterion_raw_score = 3 # Good
            elif avg_similarity >= 0.5:
                criterion_raw_score = 2 # Fair
            else:
                criterion_raw_score = 1 # Poor

            # Get the descriptive feedback from the rubric based on the raw score
            score_description = criterion_scores_map.get(criterion_raw_score)
            if not score_description:
                score_description = criterion_scores_map.get(str(criterion_raw_score), 'No description available.')
            feedback_messages.append(f"  - {criterion_name}: {score_description} (Average Key Point Similarity: {avg_similarity:.2f})")

            # Add specific feedback for low similarity key points
            for i, sim in enumerate(key_point_similarities):
                if sim < 0.6: # Threshold for suggesting improvement
                    feedback_messages.append(f"    Suggestion: Elaborate more on key point \"{key_points_obj.points[i]}\" (Similarity: {sim:.2f})")

            total_weighted_score += criterion_raw_score * criterion_weight
            results[criterion_name] = {"score": criterion_raw_score, "avg_similarity": avg_similarity}

        results["total_score"] = float(total_weighted_score)  # Convert to Python float
        results["feedback"] = "\n".join(feedback_messages)
        return results

if __name__ == '__main__':
    # Initialize BERT Similarity Model
    bert_sim_model = BERTSimilarity()

    # Define a sample Rubric
    sample_rubric = Rubric(
        name="Essay Quality Rubric",
        criteria=[
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
    )

    # Define sample Key Points
    sample_key_points = KeyPoints(
        topic="The Importance of Renewable Energy",
        points=[
            "Renewable energy sources reduce reliance on fossil fuels.",
            "Solar power and wind power are examples of renewable energy.",
            "Renewable energy contributes to mitigating climate change.",
            "Investment in renewable energy creates new jobs and economic opportunities."
        ]
    )

    # Sample Student Essay
    student_essay_good = "Renewable energy is crucial for our future. It helps us move away from fossil fuels, which are harmful to the environment. Solar and wind energy are great examples of how we can generate clean power. By using these sources, we can significantly reduce our carbon footprint and combat climate change. Furthermore, the renewable energy sector is a growing industry, providing many new jobs and boosting the economy."
    student_essay_poor = "I think energy is important. We need to use different kinds of energy. Some energy comes from the sun. It's good for the planet. People should think about this more."

    # Initialize the Grader
    grader = EssayGrader(bert_sim_model)

    # Grade the good essay
    print("\n--- Grading Good Essay ---")
    good_essay_results = grader.grade_essay(student_essay_good, sample_key_points, sample_rubric)
    print(f"Total Weighted Score: {good_essay_results['total_score']:.2f}")
    print("Feedback:\n" + good_essay_results['feedback'])

    # Grade the poor essay
    print("\n--- Grading Poor Essay ---")
    poor_essay_results = grader.grade_essay(student_essay_poor, sample_key_points, sample_rubric)
    print(f"Total Weighted Score: {poor_essay_results['total_score']:.2f}")
    print("Feedback:\n" + poor_essay_results['feedback'])


