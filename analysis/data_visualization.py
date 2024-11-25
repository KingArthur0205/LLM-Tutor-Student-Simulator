import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def plot_llm_scores_bar(df, drop_columns=["tutor_summary", "student_summary", "conversation_counter", "tutor_response_avg", "student_response_avg",
                      "LLM_Precision_Tutor", "LLM_Recall_Tutor", "BERT_Precision_Tutor", "BERT_Recall_Tutor"]):
    df = df.drop(columns=drop_columns)
    df = df.melt(id_vars="student_profile", var_name="Score_Type", value_name="Score")
    aggregated_df = df.groupby(["student_profile", "Score_Type"], as_index=False).agg(
        mean_score=("Score", "mean"),
        sem_score=("Score", lambda x: x.std() / np.sqrt(len(x)))  # Calculate standard error
    )

    student_profiles = aggregated_df["student_profile"].unique()
    score_types = aggregated_df["Score_Type"].unique()
    width = 0.5  # Width of the bars
    fig, axes = plt.subplots(nrows=1, ncols=len(student_profiles), figsize=(20, 6), sharey=True)

    # Ensure axes is always iterable
    if len(student_profiles) == 1:
        axes = [axes]

    for ax, student_profile in zip(axes, student_profiles):
        # Filter data for the specific student profile
        subset = aggregated_df[aggregated_df["student_profile"] == student_profile]

        # X positions for bars
        x = np.arange(len(score_types))
        mean_scores = subset["mean_score"].values
        sem_scores = subset["sem_score"].values

        # Plot grouped bars with error bars
        ax.bar(
            x,
            mean_scores,
            width,
            yerr=sem_scores,  # Add standard error as error bars
            capsize=5,  # Error bar cap size
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
    fig.suptitle("Scores by Student Profile and Type with Standard Error", fontsize=16)
    fig.text(0.5, 0.02, "Score Type", ha="center", fontsize=12)
    fig.text(0.04, 0.5, "Score", va="center", rotation="vertical", fontsize=12)

    # Adjust layout
    plt.tight_layout(rect=[0.03, 0.05, 1, 0.95])  # Leave space for global titles
    plt.show()

def plot_llm_scores(df, score_column="LLM_score_Student", profile_column="student_profile"):
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

def plot_heatmap(df):
    columns_to_keep = [
    "conversation_counter", "tutor_response_avg", "student_response_avg",
    "LLM_score_Tutor",
    "BERT_score_Tutor",
    "BERT_score_Student", "LLM_score_Student"
    ]

    # Filter the DataFrame to keep only the specified columns
    df_filtered = df[columns_to_keep]

    # Calculate the Pearson correlation
    correlation_matrix_filtered = df_filtered.corr(method="pearson")

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        correlation_matrix_filtered, 
        annot=True, 
        cmap="coolwarm", 
        fmt=".2f", 
        cbar=True,
        annot_kws={"size": 10}  # Adjust font size of annotations
    )

    # Adjust titles and layout to fit better
    plt.title("Pearson Correlation Heatmap", fontsize=16)
    plt.xticks(rotation=45, ha="right", fontsize=10)  # Rotate x-axis labels
    plt.yticks(fontsize=10)  # Adjust y-axis label font size
    plt.tight_layout()  # Automatically adjust layout to avoid text cutoff
    plt.show()


df = pd.read_csv("../data/cleaned_df.csv")

#plot_llm_scores(df)
#plot_llm_scores(df, score_column="LLM_score_Tutor", profile_column="student_profile")
#plot_llm_scores(df, score_column="BERT_score_Tutor", profile_column="student_profile")
#plot_llm_scores(df, score_column="BERT_score_Student", profile_column="student_profile")
#plot_llm_scores_bar(df)
#plot_heatmap(df)