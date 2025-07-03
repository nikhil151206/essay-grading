import streamlit as st
from grading import get_bert_model, EssayGrader, KeyPoints, Rubric

st.title("Automatic Essay Grading System (Streamlit)")

st.header("Essay Input")
essay_text = st.text_area("Paste the student's essay here:", height=200)

topic = st.text_input("Essay Topic:")
key_points_input = st.text_area("Key Points (one per line):", height=100)
key_points = [kp.strip() for kp in key_points_input.splitlines() if kp.strip()]

st.header("Rubric Setup")
def default_rubric():
    return [
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

if "rubric" not in st.session_state:
    st.session_state["rubric"] = default_rubric()

if st.button("Reset to Default Rubric"):
    st.session_state["rubric"] = default_rubric()

rubric = st.session_state["rubric"]

for i, criterion in enumerate(rubric):
    with st.expander(f"Criterion {i+1}: {criterion['name']}"):
        criterion["name"] = st.text_input(f"Criterion Name {i+1}", value=criterion["name"], key=f"name_{i}")
        criterion["weight"] = st.slider(f"Weight {i+1}", 0.0, 1.0, float(criterion["weight"]), 0.05, key=f"weight_{i}")
        for score in range(1, 5):
            criterion["scores"][score] = st.text_area(f"Score {score} Description", value=criterion["scores"][score], key=f"score_{i}_{score}")

if st.button("Add Criterion"):
    rubric.append({"name": "New Criterion", "weight": 0.1, "scores": {1: "", 2: "", 3: "", 4: ""}})

st.session_state["rubric"] = rubric

st.header("Grade Essay")
if st.button("Grade Essay"):
    if not essay_text.strip():
        st.error("Please enter the essay text.")
    elif not key_points:
        st.error("Please enter at least one key point.")
    else:
        keypoints_obj = KeyPoints(topic=topic or "Essay Topic", points=key_points)
        rubric_obj = Rubric(name="Custom Rubric", criteria=rubric)
        bert_model = get_bert_model()
        grader = EssayGrader(bert_model)
        with st.spinner("Grading essay..."):
            results = grader.grade_essay(essay_text, keypoints_obj, rubric_obj)
        st.success("Grading complete!")
        st.subheader("Results")
        st.write(f"**Total Weighted Score:** {results['total_score']:.2f}")
        st.write("**Feedback:**")
        st.write(results['feedback']) 