import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_llm_scores_bar(df, drop_columns=["tutor_summary", "student_summary", "conversation_counter", "tutor_response_avg", "student_response_avg",
                      "LLM_Precision_Tutor", "LLM_Recall_Tutor"]):
    """
    Create subplots for scores by student profile and score type.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing scores and student profiles.
        drop_columns (list): List of column names to drop from the DataFrame before processing.
    """
    # Step 1: Drop unnecessary columns
    df = df.drop(columns=drop_columns)

    # Step 2: Reshape and aggregate data
    df = df.melt(id_vars="student_profile", var_name="Score_Type", value_name="Score")
    aggregated_df = df.groupby(["student_profile", "Score_Type"], as_index=False)["Score"].mean()

    # Unique values for subplots
    student_profiles = aggregated_df["student_profile"].unique()
    score_types = aggregated_df["Score_Type"].unique()
    width = 0.2  # Width of the bars

    # Step 3: Create subplots
    fig, axes = plt.subplots(nrows=1, ncols=len(student_profiles), figsize=(20, 6), sharey=True)

    # Ensure axes is always iterable
    if len(student_profiles) == 1:
        axes = [axes]

    for ax, student_profile in zip(axes, student_profiles):
        # Filter data for the specific student profile
        subset = aggregated_df[aggregated_df["student_profile"] == student_profile]

        # X positions for bars
        x = np.arange(len(score_types))
        scores = subset["Score"].values

        # Plot grouped bars
        ax.bar(
            x,
            scores,
            width,
            color=["lightblue", "orange", "green", "red", "purple", "brown"][:len(score_types)],
            alpha=0.8
        )

        # Customize the subplot
        ax.set_title(student_profile, fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(score_types, rotation=45, ha="right")
        ax.set_ylim(0, 1)  # Ensure consistent scale across subplots
        ax.grid(axis="y", linestyle="--", alpha=0.6)

    # Add global labels and legend
    fig.suptitle("Scores by Student Profile and Type", fontsize=16)
    fig.text(0.5, 0.02, "Score Type", ha="center", fontsize=12)
    fig.text(0.04, 0.5, "Score", va="center", rotation="vertical", fontsize=12)

    # Adjust layout
    plt.tight_layout(rect=[0.03, 0.05, 1, 0.95])  # Leave space for global titles
    plt.show()

def plot_llm_scores(df, score_column="LLM_score_Student", profile_column="student_profile"):
    """
    Plot LLM scores colored by student profile with customization.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the data.
        score_column (str): The column name for the scores (y-axis).
        profile_column (str): The column name for the student profiles (hue).
    """
    # Set a color-blind friendly palette
    sns.set_palette("colorblind")
    
    # Create the plot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        x=range(len(df)),  # Index as x-axis
        y=score_column,
        hue=profile_column,
        data=df,
        s=100  # Size of points
    )

    # Customize the plot
    plt.title(score_column, fontsize=14)
    plt.xlabel("Index", fontsize=12)
    plt.ylabel("LLM Score", fontsize=12)
    plt.legend(title="Student Profile")

    # Adjust y-axis limits with a small buffer
    y_min, y_max = df[score_column].min(), df[score_column].max()
    plt.ylim(y_min - 0.05, y_max + 0.05)  # Add a buffer of 0.05 around min and max

    plt.grid(True, linestyle="--", alpha=0.6)

    # Show the plot
    plt.tight_layout()
    plt.show()


df = pd.read_csv("../data/cleaned_df.csv")

#plot_llm_scores(df)
#plot_llm_scores(df, score_column="LLM_score_Tutor", profile_column="student_profile")
#plot_llm_scores(df, score_column="BERT_score_Tutor", profile_column="student_profile")
#plot_llm_scores(df, score_column="BERT_score_Student", profile_column="student_profile")
#plot_llm_scores_bar(df)

