library(haven)
library(dplyr)
library(tidyr)

df <- read.csv("../data/student_tutor_sim.csv")
df <- df[-1, ]
df <- df |> # Clean data
  select(-ends_with("level"), -ends_with("style"), 
         -ends_with("Precision_Student"), -ends_with("Recall_Student"),-chat_history)
df <- df[order(df$student_profile), ]
write.csv(df, "../data/cleaned_df.csv", row.names=FALSE)
