# ==============================================================================
# R Reproduction Script: Cross-Language Validation of Economic Divergence
#
# Research Question:
#   "How has state-wise per-capita income diverged in India since 2011?"
#
# Pipeline Stage:
#   Raw data -> Cleaning -> Analysis -> Visualization -> [R reproduction] -> Git
# ==============================================================================

# 1. Resolve relative path to processed data
data_path <- file.path("data", "processed", "per_capita_nsdp_cleaned.csv")

if (!file.exists(data_path)) {
  message("[INFO] Processed dataset not found at: ", data_path)
  message("       Run the Python cleaning pipeline first: python python/clean_data.py")
} else {
  message("[INFO] Loading cleaned data into R: ", data_path)
  
  # Read processed panel dataset
  df <- read.csv(data_path, stringsAsFactors = FALSE)
  
  # Filter out All-India aggregate row
  df_states <- df[!tolower(df$State) %in% c("all india", "all-india"), ]
  df_states <- df_states[!is.na(df_states$Per_Capita_NSDP_INR), ]
  
  # 2. Replicate Sigma (σ) Convergence - Coefficient of Variation
  years <- sort(unique(df_states$Year_Start))
  results <- data.frame(
    Year_Start = integer(),
    Financial_Year = character(),
    N_States = integer(),
    Mean_Income = numeric(),
    Std_Dev = numeric(),
    CV = numeric(),
    stringsAsFactors = FALSE
  )
  
  for (yr in years) {
    sub <- df_states[df_states$Year_Start == yr, ]
    fy <- unique(sub$Financial_Year)[1]
    mean_val <- mean(sub$Per_Capita_NSDP_INR, na.rm = TRUE)
    sd_val <- sd(sub$Per_Capita_NSDP_INR, na.rm = TRUE)
    cv_val <- sd_val / mean_val
    
    results <- rbind(results, data.frame(
      Year_Start = yr,
      Financial_Year = fy,
      N_States = nrow(sub),
      Mean_Income = round(mean_val, 2),
      Std_Dev = round(sd_val, 2),
      CV = round(cv_val, 4),
      stringsAsFactors = FALSE
    ))
  }
  
  message("[SUCCESS] R cross-validation complete. Summary preview:")
  print(head(results))
}
