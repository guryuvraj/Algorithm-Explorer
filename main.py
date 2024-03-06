import streamlit as st
import matplotlib.pyplot as plt

def suggest_study_plan(subjects, available_hours):
    subjects_sorted = sorted(subjects.items(), key=lambda x: x[1]['mark'])
    total_hours = sum([sub['hours_studied'] for _, sub in subjects.items()])
    avg_hours = total_hours / len(subjects) if subjects else 0

    for subject, data in subjects_sorted:
        deficit_hours = max(0, avg_hours - data['hours_studied'])
        if available_hours <= 0:
            break
        allocated_hours = min(deficit_hours, available_hours)
        subjects[subject]['suggested_additional_hours'] = allocated_hours
        available_hours -= allocated_hours
    return subjects


def plot_study_distribution(subjects):
    labels = subjects.keys()
    current_hours = [data['hours_studied'] for data in subjects.values()]
    suggested_hours = [data['hours_studied'] + data['suggested_additional_hours'] for data in subjects.values()]

    fig, ax = plt.subplots(1, 2, figsize=(14, 7))
    ax[0].pie(current_hours, labels=labels, autopct='%1.1f%%', startangle=140)
    ax[0].set_title('Current Study Distribution')
    ax[1].pie(suggested_hours, labels=labels, autopct='%1.1f%%', startangle=140)
    ax[1].set_title('Suggested Study Distribution')

    return fig

def main():
    st.title("Optimal Study Plan Suggestion")
    st.caption("This project is an application of Greedy Algorithm")

    with st.form("study_plan_form"):
        subjects_input = st.text_area("Enter subjects, marks, and hours studied (comma-separated, one per line):", 
                                      "Subject1,75,10\nSubject2,80,15")
        available_hours = st.number_input("How many hours are you able to study in total for the improvement?", min_value=0.0, value=10.0)
        submit_button = st.form_submit_button("Submit")

    if submit_button:
        subjects = {}
        for line in subjects_input.split('\n'):
            parts = line.split(',')
            if len(parts) == 3:
                subjects[parts[0]] = {'mark': float(parts[1]), 'hours_studied': float(parts[2]), 'suggested_additional_hours': 0}
        
        subjects = suggest_study_plan(subjects, available_hours)
        fig = plot_study_distribution(subjects)
        st.pyplot(fig)

if __name__ == "__main__":
    main()
